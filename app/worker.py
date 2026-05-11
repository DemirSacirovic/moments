import time
from app.db import get_next_queued_event, update_event_status
from app.llm import extract_signal, LLMError

def process_one(event) -> None:
    event_id = event["event_id"]
    print(f"[worker] processing {event_id}")

    update_event_status(event_id, "processing")

    try:
        result = extract_signal(event["content"])
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
