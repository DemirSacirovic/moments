from uuid import uuid4

from fastapi import FastAPI

from app.db import init_db, find_event, insert_event
from app.schemas import EventIn, JobAccepted, BulkOnboardRequest, BulkOnboardResponse


app = FastAPI(title="moments")
init_db()


@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/event", response_model=JobAccepted)
def submit_event(event: EventIn) -> JobAccepted:
    existing = find_event(event.event_id)
    if existing is not None:
        return JobAccepted(
            job_id =existing["job_id"],
            event_id=existing["event_id"],
            status=existing["status"],
        )
    job_id = str(uuid4())
    insert_event(
        event_id=event.event_id,
        job_id=job_id,
        tenant_id=event.tenant_id,
        client_id=event.client_id,
        event_type=event.event_type.value,
        occurred_at=event.occurred_at.isoformat(),
        content=event.content,
    )
    return JobAccepted(job_id=job_id, event_id=event.event_id)


@app.post("/onboard", response_model=BulkOnboardResponse)
def bulkonboard(req: BulkOnboardRequest) -> BulkOnboardResponse:
    new_inserts = 0
    duplicates = 0
    errors = []

    for event in req.events:
        try:
            existing = find_event(event.event_id)
            if existing is not None:
                duplicates += 1
                continue

            job_id = str(uuid4())
            insert_event(
                event_id=event.event_id,
                job_id=job_id,
                tenant_id=event.tenant_id,
                client_id=event.client_id,
                event_type=event.event_type.value,
                occurred_at=event.occurred_at.isoformat(),
                content=event.content,
            )
            new_inserts += 1
        except Exception as e:
            errors.append({"event_id": event.event_id, "error": str(e)})

    return BulkOnboardResponse(
        submitted=len(req.events),
        new_inserts=new_inserts,
        duplicates=duplicates,
        errors=errors,
    )
