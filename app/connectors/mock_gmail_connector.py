import json
from pathlib import Path

import requests

API_URL = "http://127.0.0.1:8000/onboard"
FIXTURE_PATH = Path(__file__).parent.parent.parent / "fixtures" / "gmail_emails.json"


def transform_to_canonical(email:dict) -> dict:
    """Gmail email -> Sophie canonical event."""
    return {
        "event_id": f"gmail-{email['gmail_id']}",
        "tenant_id": email["advisor_id"],
        "client_id": email["from"],
        "event_type": "email",
        "occurred_at": email["received_at"],
        "content": f"Subject: {email['subject']}\n\n{email['body']}",
        "metadata": {
            "source": "gmail",
            "from": email["from"],
            "subject": email["subject"],
        },
    }

def load_fixtures() -> list[dict]:
    with open(FIXTURE_PATH) as f:
        return json.load(f)


def run():
    print(f"[gmail-connector] loading fixtures from {FIXTURE_PATH.name}")
    emails = load_fixtures()
    print(f"[gmail-connector] loaded {len(emails)} emails")

    events = [transform_to_canonical(e) for e in emails]

    print(f"[gmail-connector] POSTing {len(events)} events to Sophie...")
    response = requests.post(API_URL, json={"events": events})

    if response.ok:
        print(f"[gmail-connector] response: {response.json()}")
    else:
        print(f"[gmail-connector] ERROR: {response.status_code} {response.text}")

if __name__ == "__main__":
    run()
