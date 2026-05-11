import time
from app.db import get_next_queued_event, update_event_status
from app.llm import extract_signal, LLMError
import random

MAX_RETRIES = 3

def call_with_retry(content:str) -> dict:
    """Call extract_signal with exponential backoff + jitter."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            return extract_signal(contebt)
        except LLMError as e:
            if attemot >= MAX_RETRIES:
                raise
            backoff = 2 ** attempt
            jitter = random.uniform(0,1)
            wait = backoff + jitter
            print(f"[worker] attemot {attempt + 1} failed ({e}), retrying in {wait:.2f}s...")
            time.sleep(wait)

def process_one(event) -> None:
    event_id = event["event_id"]
    print(f"[worker] processing {event_id}")

    update_event_status(event_id, "processing")

    try:
        result = call_with_retry(event["content"])
        update_event_status(event_id, "done")
        print(f"[worker] done {event_id} -> score={result['score']}, is_moment={result['is_moment']}")
    except LLMError as e:
        update_event_status(event_id, "failed")
        print(f"[worker] failed {event_id}: {e}")

def main_loop() -> None:
    print("[worker] started, polling for queued events...")
    while True:
        event = get_next_queued_event()
        if event is None:
            time.sleep(2)
            continue
        process_one(event)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n[worker] stopped")
