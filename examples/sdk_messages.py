"""Live: basic Messages, token counting and streaming. Makes two generation requests.

API reference: https://platform.claude.com/docs/en/api/sdks/python
"""

from examples.common import client, model_id


def main():
    with client() as api:
        model = model_id()
        messages = [
            {"role": "user", "content": "Explain one benefit of a deterministic policy gate."}
        ]
        count = api.messages.count_tokens(model=model, messages=messages)
        print("Estimated input tokens:", count.input_tokens)
        message = api.messages.create(model=model, max_tokens=250, messages=messages)
        if message.stop_reason != "end_turn":
            raise RuntimeError(f"Incomplete generation: {message.stop_reason}")
        print("".join(b.text for b in message.content if b.type == "text"))
        print("Usage:", message.usage)
        with api.messages.stream(model=model, max_tokens=250, messages=messages) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
            final = stream.get_final_message()
        print("\nStream status:", final.stop_reason, "usage:", final.usage)
        if final.stop_reason != "end_turn":
            raise RuntimeError("Stream did not produce a complete answer")


if __name__ == "__main__":
    main()
