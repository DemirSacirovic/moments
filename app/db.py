import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "moments.db"


def get_connection() -> sqlite3.Connection:
    """Open a SQLite connecetion. Caller must close it."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Create tables if they don't exist. Idempotent - safe to call on every startup."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_id    TEXT PRIMARY KEY,
                job_id      TEXT NOT NULL,
                tenant_id   TEXT NOT NULL,
                client_id   TEXT NOT NULL,
                event_type  TEXT NOT NULL,
                occurred_at TEXT NOT NULL,
                content     TEXT NOT NULL,
                status      TEXT NOT NULL DEFAULT 'queued',
                created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def find_event(event_id: str) -> sqlite3.Row | None:
    """Return the event row if it exists, else None."""
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT * FROM events WHERE event_id = ?",
            (event_id,),
        )
        return cursor.fetchone()

def insert_event(
    event_id: str,
    job_id: str,
    tenant_id: str,
    client_id: str,
    event_type: str,
    occurred_at: str,
    content: str,
) -> None:
    """Insert a new event now"""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO events
                (event_id, job_id, tenant_id, client_id, event_type, occurred_at, content)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (event_id, job_id, tenant_id, client_id, event_type, occurred_at, content),
        )
        conn.commit()

def get_next_queued_event() -> sqlite3.Row | None:
    """Return the oldest queued event, or None if queue id empty."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT * FROM events
            WHERE status = 'queued'
            ORDER BY created_at ASC
            LIMIT 1
            """
        )
        return cursor.fetchone()

def update_event_status(event_id: str, status: str) -> None:
    """Update an event's status."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE events SET status = ? WHERE event_id = ?",
            (status, event_id),
        )
        conn.commit()
