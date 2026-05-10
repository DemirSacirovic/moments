from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class EventType(str, Enum):
    EMAIL = "email"
    CALENDAR = "calendar"
    TRANSACTION = "transaction"

class EventIn(BaseModel):
    """Event coming in from a tenant's source system"""

    event_id: str = Field(..., description="Source-system ID, used for idempotency")
    tenant_id: str = Field(..., description="Which advisor/firm thid belongs to")
    client_id: str = Field(..., description="Which client this is about")
    event_type : EventType
    occurred_at: datetime
    content: str = Field(..., min_length=1, max_length =10_000)
    metadata: dict = Field(default_factory=dict)

class JobAccepted(BaseModel):
    """Returned after we accept an event for processing"""
    job_id: str
    event_id: str
    status: str = "queued"
