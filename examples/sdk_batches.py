"""Live opt-in batch submit OR one status/results check. No hidden polling.

https://platform.claude.com/docs/en/build-with-claude/batch-processing
"""

import argparse
import json

from examples.common import client, model_id


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--submit", action="store_true")
    action.add_argument("--check", metavar="BATCH_ID")
    args = parser.parse_args()
    # Disable automatic submission retries: a lost create response has an unknown outcome.
    with client().with_options(max_retries=0) as api:
        if args.submit:
            batch = api.messages.batches.create(
                requests=[
                    {
                        "custom_id": f"doc-{i}",
                        "params": {
                            "model": model_id(),
                            "max_tokens": 200,
                            "messages": [
                                {"role": "user", "content": f"Summarize this text: {text}"}
                            ],
                        },
                    }
                    for i, text in enumerate(
                        ["An order lookup is read-only.", "A refund is a write."]
                    )
                ]
            )
            print("Save this batch ID:", batch.id)
            return
        batch = api.messages.batches.retrieve(args.check)
        print("Status:", batch.processing_status, "counts:", batch.request_counts)
        if batch.processing_status == "ended":
            for item in api.messages.batches.results(args.check):
                print(json.dumps(item.model_dump(mode="json")))
        else:
            print("Check again later with the same ID. Do not submit a replacement batch.")


if __name__ == "__main__":
    main()
