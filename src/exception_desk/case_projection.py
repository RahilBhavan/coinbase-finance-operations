"""Oracle reporting over the canonical reducer projection.

This module intentionally contains no projection rules. ``project_case`` is
re-exported for compatibility, so application output and conformance use the
same state engine.
"""

from __future__ import annotations

from typing import Any, Mapping

from .reducer import project_case

__all__ = ["project_case", "oracle_conformance"]


def oracle_conformance(groups: Mapping[str, list[dict[str, Any]]], oracle: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for expected in oracle["cases"]:
        fixture_id = expected["fixture_id"]
        actual = project_case(groups[fixture_id])
        fields = ("expected_payment_state", "expected_fulfillment_state",
                  "expected_exception_type", "actionable", "expected_financials")
        mismatches = [field for field in fields if actual[field] != expected[field]]
        rows.append({"fixture_id": fixture_id, "status": "PASS" if not mismatches else "FAIL",
                     "mismatches": mismatches, "actual": actual})
    return rows
