"""Adapters from the documented fixture envelope to reducer events."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_oracle(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def group_by_fixture(events: Iterable[Mapping[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        groups.setdefault(str(event["fixture_id"]), []).append(dict(event))
    for group in groups.values():
        group.sort(key=lambda event: (event["observed_at"], event["sequence"], event["event_id"]))
    return groups


def reducer_events(events: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Translate a fixture case without inventing payment evidence."""
    source = list(events)
    order_id = str(source[0]["aggregate_id"])
    attempt_ids = [
        str(event["payload"]["attempt_id"])
        for event in source
        if event.get("payload", {}).get("attempt_id")
    ]
    payment_id = attempt_ids[0] if attempt_ids else f"attempt-{order_id}"
    translated = []
    for event in source:
        payload = dict(event.get("payload", {}))
        kind = str(event["event_type"])
        mapped = kind
        data = payload
        if kind == "order_opened":
            mapped = "order_created"
            data = {**payload, "order_id": order_id,
                    "expected_atomic_amount": payload["expected_amount_atomic"]}
        elif kind == "authorization_verified":
            mapped = "payment_attempt_submitted"
            data = {**payload, "order_id": order_id}
        elif kind == "payment_observed":
            mapped = "chain_observed"
            data = {**payload, "stage": payload.get("finality_stage", "observed")}
        elif kind == "resource_prepared":
            mapped, data = "fulfillment_prepared", {**payload, "order_id": order_id}
        elif kind == "delivery_acknowledged":
            mapped, data = "fulfillment_delivered", {**payload, "order_id": order_id}
        elif kind == "delivery_failed":
            mapped, data = "fulfillment_delivery_failed", {**payload, "order_id": order_id}
        elif kind == "settlement_timed_out":
            mapped = "payment_attempt_timed_out"
        elif kind == "settlement_failed":
            mapped = "payment_attempt_failed"
        elif kind in {"refund_approved_reserved", "refund_submitted_unknown"}:
            data = {**payload, "payment_id": payment_id,
                    "atomic_amount": payload["amount_atomic"]}
        elif kind in {
            "authorization_rejected", "resource_preparation_failed",
            "duplicate_request_received", "payment_claim_conflicted",
            "refund_reservation_rejected", "ingestion_replay_detected",
            "chain_observation_invalidated", "payment_evidence_received",
        }:
            mapped = "exception_opened"
            data = {**payload, "exception_id": event["event_id"], "type": kind,
                    "order_id": order_id}
        translated.append({
            "event_id": str(event["event_id"]),
            "type": mapped,
            "occurred_at": str(event["occurred_at"]),
            "observed_at": str(event["observed_at"]),
            "data": data,
        })
    return translated

