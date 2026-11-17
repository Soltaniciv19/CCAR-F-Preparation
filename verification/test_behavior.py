"""Meaningful offline checks for protocol, authority, unknown outcomes and evidence."""

import json
import subprocess
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from capstone.solution import Case, SupportApplication
from ccarf.architecture import Order, RefundService, run_loop, uncovered
from ccarf.extraction import correlate_batch, evidence_matches, money, validate_invoice
from ccarf.reliability import (
    Claim,
    build_context,
    compare_claims,
    load_manifest,
    route_case,
    save_manifest,
    stratified_sample,
)
from ccarf.tools import dispatcher, failure, lookup_order, retry_read
from ccarf.workflows import new_findings, run_review


def response(reason, *blocks):
    return {"stop_reason": reason, "content": list(blocks)}


class LoopTests(unittest.TestCase):
    def test_text_does_not_hide_multiple_calls_or_error(self):
        messages = iter(
            [
                response(
                    "tool_use",
                    {"type": "text", "text": "Done? Not yet."},
                    {
                        "type": "tool_use",
                        "id": "a",
                        "name": "lookup_order",
                        "input": {"order_id": "O-100"},
                    },
                    {"type": "tool_use", "id": "b", "name": "unknown", "input": {}},
                ),
                response("end_turn", {"type": "text", "text": "Final"}),
            ]
        )
        observed = []

        def request(history):
            observed.append(history)
            return next(messages)

        result = run_loop(request, dispatcher({"O-100": {"customer_id": "C-7"}}, "C-7"), "task")
        self.assertEqual(result.status, "complete")
        results = observed[1][-1]["content"]
        self.assertEqual([r["tool_use_id"] for r in results], ["a", "b"])
        self.assertFalse(results[0]["is_error"])
        self.assertTrue(results[1]["is_error"])
        self.assertEqual(len(observed[1][1]["content"]), 3)

    def test_truncation_is_incomplete(self):
        result = run_loop(
            lambda _: response("max_tokens", {"type": "text", "text": "{"}), lambda *_: {}, "task"
        )
        self.assertEqual(result.status, "incomplete:max_tokens")

    def test_budget_not_success(self):
        result = run_loop(
            lambda _: response(
                "tool_use", {"type": "tool_use", "id": "a", "name": "read", "input": {}}
            ),
            lambda *_: {"ok": True, "data": []},
            "task",
            max_turns=2,
        )
        self.assertEqual(result.status, "budget_exhausted")

    def test_duplicate_ids_rejected(self):
        block = {"type": "tool_use", "id": "a", "name": "read", "input": {}}
        with self.assertRaises(ValueError):
            run_loop(lambda _: response("tool_use", block, block), lambda *_: {}, "task")

    def test_completed_tasks_do_not_imply_coverage(self):
        missing = uncovered(
            {"price", "privacy"},
            [
                {"status": "complete", "covered_topics": ["price"]},
                {"status": "failed", "covered_topics": ["privacy"]},
            ],
        )
        self.assertEqual(missing, {"privacy"})


class RefundTests(unittest.TestCase):
    def setUp(self):
        self.service = RefundService({"O-100": Order("C-7", 12000)})
        self.args = dict(
            authenticated_customer="C-7", order_id="O-100", amount_cents=2000, idempotency_key="one"
        )

    def test_replay_one_effect(self):
        first = self.service.refund(**self.args)
        self.assertEqual(first, self.service.refund(**self.args))
        self.assertEqual(self.service.refunded["O-100"], 2000)

    def test_key_payload_conflict(self):
        self.service.refund(**self.args)
        with self.assertRaises(ValueError):
            self.service.refund(**{**self.args, "amount_cents": 3000})

    def test_unverified_and_wrong_owner_blocked(self):
        for principal in (None, "C-other"):
            with self.assertRaises(PermissionError):
                self.service.refund(**{**self.args, "authenticated_customer": principal})
        self.assertEqual(self.service.refunded, {})

    def test_invalid_amounts(self):
        for amount in (True, 2.5, -1, 0, 13000):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                self.service.refund(**{**self.args, "amount_cents": amount})

    def test_concurrent_limit(self):
        def invoke(key):
            try:
                self.service.refund(**{**self.args, "amount_cents": 8000, "idempotency_key": key})
                return True
            except ValueError:
                return False

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(invoke, ["first", "second"]))
        self.assertEqual(sum(results), 1)
        self.assertEqual(self.service.refunded["O-100"], 8000)

    def test_policy_gate(self):
        service = RefundService({"O-100": Order("C-7", 12000, refundable=False)})
        with self.assertRaises(PermissionError):
            service.refund(**self.args)


class ToolTests(unittest.TestCase):
    def test_read_recovery_metadata(self):
        count = 0

        def operation():
            nonlocal count
            count += 1
            if count < 3:
                raise TimeoutError
            return {"ok": True, "data": []}

        delays = []
        result = retry_read(operation, sleep=delays.append)
        self.assertEqual(result["attempts"], 3)
        self.assertTrue(result["ok"])
        self.assertEqual(delays, [0.1, 0.2])

    def test_permission_failure_not_retried(self):
        result = retry_read(lambda: failure("authorization", "DENIED", False, "denied"))
        self.assertEqual(result["attempts"], 1)

    def test_timeout_not_empty_success(self):
        def operation():
            raise TimeoutError

        result = retry_read(operation, attempts=2, sleep=lambda _: None)
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "TIMEOUT")

    def test_no_match_and_private_record_do_not_leak(self):
        orders = {"O-private": {"customer_id": "C-other", "paid_cents": 9000}}
        results = [
            lookup_order({"order_id": identifier}, customer_id="C-7", orders=orders)
            for identifier in ["O-private", "O-missing"]
        ]
        self.assertEqual(results, [{"ok": True, "data": None}] * 2)

    def test_model_cannot_supply_authentication_flag(self):
        result = lookup_order({"order_id": "O-100", "verified": True}, customer_id=None, orders={})
        self.assertFalse(result["ok"])


class ExtractionTests(unittest.TestCase):
    def record(self, total="12.00"):
        return {
            "items": [{"quantity": 3, "unit_price": "4.00"}],
            "stated_total": total,
            "po_number": None,
            "evidence": {"stated_total": {"start": 7, "end": 12, "quote": total}},
        }

    def test_validated_arithmetic_and_evidence(self):
        self.assertEqual(validate_invoice(self.record(), "Total: 12.00")["status"], "validated")

    def test_contradiction_preserved(self):
        outcome = validate_invoice(self.record("13.00"), "Total: 13.00")
        self.assertEqual(outcome["status"], "human_review")
        self.assertEqual(outcome["stated_total"], "13.00")
        self.assertEqual(outcome["computed_total"], "12.00")

    def test_bad_evidence_requires_review(self):
        self.assertEqual(validate_invoice(self.record(), "Total: 99.00")["status"], "human_review")

    def test_boolean_quantity_is_not_an_integer_quantity(self):
        record = self.record()
        record["items"][0]["quantity"] = True
        self.assertEqual(validate_invoice(record, "Total: 12.00")["status"], "retry")

    def test_money_validation(self):
        self.assertEqual(money("0.10") + money("0.20"), Decimal("0.30"))
        for value in (True, 0.1, "NaN", "Infinity", "-1", "1.001", "bad"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                money(value)

    def test_source_offsets(self):
        self.assertTrue(evidence_matches("α12", {"start": 1, "end": 3, "quote": "12"}))
        self.assertFalse(evidence_matches("α12", {"start": True, "end": 3, "quote": "12"}))

    def test_batch_order_not_assumed(self):
        indexed = correlate_batch(
            {"a", "b"},
            [
                {"custom_id": "b", "result": {"type": "expired"}},
                {"custom_id": "a", "result": {"type": "succeeded"}},
            ],
        )
        self.assertEqual(indexed["a"]["type"], "succeeded")
        self.assertEqual(indexed["b"]["type"], "expired")

    def test_missing_duplicate_unknown_batch_ids(self):
        for results in (
            [],
            [{"custom_id": "b", "result": {}}],
            [{"custom_id": "a", "result": {}}] * 2,
        ):
            with self.assertRaises(ValueError):
                correlate_batch({"a"}, results)


class WorkflowTests(unittest.TestCase):
    def test_cli_envelope_payload_and_no_shell(self):
        def fake(command, **kwargs):
            self.assertIsInstance(command, list)
            self.assertIn("-p", command)
            self.assertNotIn("shell", kwargs)
            self.assertEqual(kwargs["input"], "untrusted `text` $(no-shell)")
            self.assertTrue(kwargs["check"])
            return SimpleNamespace(
                stdout=json.dumps(
                    {"subtype": "success", "is_error": False, "structured_output": {"findings": []}}
                )
            )

        result = run_review("untrusted `text` $(no-shell)", Path("."), runner=fake)
        self.assertEqual(result, {"findings": []})

    def test_failed_or_missing_payload_not_clean_review(self):
        for envelope in (
            {"subtype": "error", "is_error": True},
            {"subtype": "success", "result": "looks good"},
        ):
            with self.assertRaises((RuntimeError, ValueError)):
                run_review(
                    "task",
                    Path("."),
                    runner=lambda *a, value=envelope, **kw: SimpleNamespace(
                        stdout=json.dumps(value)
                    ),
                )

    def test_process_failure_propagates(self):
        def fake(*a, **kw):
            raise subprocess.TimeoutExpired("claude", 180)

        with self.assertRaises(subprocess.TimeoutExpired):
            run_review("task", Path("."), runner=fake)

    def test_line_movement_not_new_finding(self):
        first = {"path": "a.py", "line": 2, "category": "units", "evidence": "qty * price"}
        moved = {**first, "line": 20}
        self.assertEqual(new_findings([moved], [first]), [])
        self.assertEqual(len(new_findings([moved, moved], [])), 1)


class ReliabilityTests(unittest.TestCase):
    def setUp(self):
        self.claim = Claim(
            "sites",
            "4200",
            "sites",
            "2025",
            "registered",
            "register",
            "agency",
            "2026-03-01",
            "page 19",
        )

    def test_comparison_dimensions(self):
        self.assertEqual(
            compare_claims(self.claim, replace(self.claim, period="2026")),
            "not_directly_comparable",
        )
        self.assertEqual(
            compare_claims(self.claim, replace(self.claim, value="4300")),
            "conflict_requires_verification",
        )
        self.assertEqual(compare_claims(self.claim, self.claim), "consistent")

    def test_summary_does_not_overwrite_fact_block(self):
        context = build_context(
            facts={"amount_cents": 1200}, claims=[self.claim], summary="amount is 2100"
        )
        self.assertEqual(context["case_facts"]["amount_cents"], 1200)
        self.assertEqual(context["evidence"][0]["published"], "2026-03-01")

    def test_manifest_revision_and_pending(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            save_manifest(path, commit="a", completed=["map"], pending=["trace"])
            self.assertFalse(load_manifest(path, "a")["needs_revalidation"])
            changed = load_manifest(path, "b")
            self.assertTrue(changed["needs_revalidation"])
            self.assertEqual(changed["pending"], ["trace"])
            self.assertEqual(len(list(Path(directory).iterdir())), 1)

    def test_route_priorities(self):
        self.assertEqual(
            route_case(wants_human=True, ambiguous_identity=True), "escalate_requested"
        )
        self.assertEqual(route_case(ambiguous_identity=True), "clarify_identity")
        self.assertEqual(route_case(policy_exception=True), "escalate_policy")
        self.assertEqual(route_case(recovery_exhausted=True), "escalate_with_partial_findings")
        self.assertEqual(route_case(), "resolve_within_policy")

    def test_high_confidence_strata_sampled_reproducibly(self):
        records = [
            {
                "id": f"{kind}-{confidence}-{i}",
                "document_type": kind,
                "field": "total",
                "confidence_band": confidence,
            }
            for kind in ["typed", "scan"]
            for confidence in ["high", "low"]
            for i in range(5)
        ]
        sample = stratified_sample(records, per_stratum=1, seed=7)
        self.assertEqual(sample, stratified_sample(records, per_stratum=1, seed=7))
        self.assertEqual(len(sample), 4)
        self.assertEqual(sum(r["confidence_band"] == "high" for r in sample), 2)


class CapstoneTests(unittest.TestCase):
    def test_model_cannot_change_confirmed_order(self):
        app = SupportApplication()
        app.billing.orders["O-200"] = Order("C-7", 12000)
        case = Case("C", "C-7", ["billing"])
        result = app.execute_refund(
            case,
            {"order_id": "O-200", "amount_cents": 1200},
            confirmed_order_id="O-100",
            confirmed_amount=1200,
            operation_key="op",
        )
        self.assertFalse(result["ok"])
        self.assertEqual(app.billing.refunded, {})

    def test_model_cannot_change_confirmed_amount_or_identity(self):
        app = SupportApplication()
        case = Case("C", "C-7", ["billing"])
        result = app.execute_refund(
            case,
            {"order_id": "O-100", "amount_cents": 2100},
            confirmed_order_id="O-100",
            confirmed_amount=1200,
            operation_key="op",
        )
        self.assertFalse(result["ok"])
        result = app.execute_refund(
            case,
            {"order_id": "O-100", "amount_cents": 1200, "authenticated_customer": "C-7"},
            confirmed_order_id="O-100",
            confirmed_amount=1200,
            operation_key="op",
        )
        self.assertFalse(result["ok"])
        self.assertEqual(app.billing.refunded, {})

    def test_replay_handoff_contains_one_receipt(self):
        app = SupportApplication()
        case = Case("C", "C-7", ["billing", "delivery"])
        args = {"order_id": "O-100", "amount_cents": 1200}
        first = app.execute_refund(
            case, args, confirmed_order_id="O-100", confirmed_amount=1200, operation_key="op"
        )
        second = app.execute_refund(
            case, args, confirmed_order_id="O-100", confirmed_amount=1200, operation_key="op"
        )
        self.assertEqual(first, second)
        packet = app.handoff(case, "delivery_unavailable", [], ["delivery"])
        self.assertEqual(len(packet["confirmed_operations"]), 1)
        self.assertEqual(packet["pending"], ["delivery"])


if __name__ == "__main__":
    unittest.main()
