"""SQLite-backed append-only storage for exception-desk events.

Events use a deliberately small JSONL-compatible contract::

    {"event_id": "...", "type": "order_created",
     "observed_at": "2027-01-02T03:04:05Z", "occurred_at": "...",
     "data": { ... event-specific fields ... }}

Event-specific fields may also be at the top level.  This makes hand-authored
fixtures pleasant while keeping the persisted payload lossless.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Iterable, Mapping


class InvalidEvent(ValueError):
    """Raised when an event does not satisfy the envelope contract."""


def validate_event(event: Mapping[str, Any]) -> None:
    for field in ("event_id", "type", "observed_at"):
        if not isinstance(event.get(field), str) or not event[field].strip():
            raise InvalidEvent(f"{field} must be a non-empty string")
    if "data" in event and not isinstance(event["data"], Mapping):
        raise InvalidEvent("data must be an object when present")


class EventStore:
    """An append-only event log; duplicate event IDs are idempotent replays."""

    def __init__(self, path: str | Path = ":memory:") -> None:
        self.connection = sqlite3.connect(str(path))
        self.connection.row_factory = sqlite3.Row
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL UNIQUE,
                event_type TEXT NOT NULL,
                occurred_at TEXT NOT NULL,
                observed_at TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def append(self, event: Mapping[str, Any]) -> bool:
        """Append once, returning False for a byte-equivalent replay.

        Reusing an ID with different content is corruption rather than replay
        and is rejected.  Existing rows are never updated.
        """
        validate_event(event)
        payload = json.dumps(dict(event), sort_keys=True, separators=(",", ":"))
        existing = self.connection.execute(
            "SELECT payload FROM events WHERE event_id = ?", (event["event_id"],)
        ).fetchone()
        if existing is not None:
            if existing["payload"] != payload:
                raise InvalidEvent(f"event_id {event['event_id']!r} has conflicting content")
            return False
        occurred_at = event.get("occurred_at", event["observed_at"])
        if not isinstance(occurred_at, str) or not occurred_at:
            raise InvalidEvent("occurred_at must be a non-empty string when present")
        self.connection.execute(
            "INSERT INTO events(event_id,event_type,occurred_at,observed_at,payload) "
            "VALUES (?,?,?,?,?)",
            (event["event_id"], event["type"], occurred_at, event["observed_at"], payload),
        )
        self.connection.commit()
        return True

    def append_many(self, events: Iterable[Mapping[str, Any]]) -> int:
        return sum(self.append(event) for event in events)

    def events(self) -> list[dict[str, Any]]:
        """Return canonical reducer order, independent of ingestion order."""
        rows = self.connection.execute(
            "SELECT payload FROM events "
            "ORDER BY observed_at, occurred_at, event_id"
        )
        return [json.loads(row["payload"]) for row in rows]

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "EventStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
