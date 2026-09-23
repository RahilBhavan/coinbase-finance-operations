import tempfile
import unittest
from pathlib import Path

from exception_desk.reducer import project_case, reduce_events
from exception_desk.store import EventStore, InvalidEvent


def event(event_id, kind, minute, **data):
    return {"event_id": event_id, "type": kind,
            "observed_at": f"2027-01-01T00:{minute:02d}:00Z", "data": data}


class ReducerTests(unittest.TestCase):
    def base(self):
        return [
            event("o1", "order_created", 0, order_id="order-1", expected_atomic_amount=100, asset="USDC"),
            event("a1", "payment_attempt_submitted", 1, attempt_id="attempt-1", order_id="order-1"),
        ]

    def test_timeout_is_unknown_and_late_evidence_updates_original_attempt(self):
        events = self.base() + [
            event("t1", "payment_attempt_timed_out", 2, attempt_id="attempt-1"),
            event("c1", "chain_observed", 9, attempt_id="attempt-1", network="base", transaction_ref="0x1", log_index=0),
        ]
        state = reduce_events(events)
        self.assertTrue(state["payment_attempts"]["attempt-1"]["timed_out"])
        self.assertEqual("observed", state["payment_attempts"]["attempt-1"]["outcome"])

    def test_replay_and_ingestion_order_are_idempotent(self):
        events = self.base()
        self.assertEqual(reduce_events(events), reduce_events(list(reversed(events)) + events))

    def test_payment_evidence_cannot_satisfy_two_orders(self):
        events = self.base() + [
            event("o2", "order_created", 2, order_id="order-2", expected_atomic_amount=100),
            event("a2", "payment_attempt_submitted", 3, attempt_id="attempt-2", order_id="order-2"),
            event("c1", "chain_observed", 4, attempt_id="attempt-1", network="base", transaction_ref="0x1", log_index=0),
            event("c2", "chain_observed", 5, attempt_id="attempt-2", network="base", transaction_ref="0x1", log_index=0),
        ]
        state = reduce_events(events)
        self.assertEqual("observed", state["orders"]["order-1"]["payment_state"])
        self.assertEqual("unpaid", state["orders"]["order-2"]["payment_state"])
        self.assertTrue(any(x["type"] == "evidence_claim_conflict" for x in state["exceptions"].values()))

    def test_refund_reservations_and_completed_never_exceed_capture(self):
        events = self.base() + [
            event("c1", "chain_observed", 1, attempt_id="attempt-1", network="base",
                  transaction_ref="0x1", log_index=0, amount_atomic=100),
            event("r1", "refund_reserved", 2, refund_id="r1", attempt_id="attempt-1", atomic_amount=70),
            event("r2", "refund_reserved", 3, refund_id="r2", attempt_id="attempt-1", atomic_amount=40),
        ]
        state = reduce_events(events)
        self.assertEqual("approved_reserved", state["refunds"]["r1"]["state"])
        self.assertEqual("proposed", state["refunds"]["r2"]["state"])
        self.assertTrue(any(x["type"] == "refund_over_capture" for x in state["exceptions"].values()))

    def test_payment_and_delivery_are_separate(self):
        state = reduce_events(self.base() + [
            event("c1", "chain_observed", 2, attempt_id="attempt-1", network="base", transaction_ref="0x1"),
            event("f1", "fulfillment_delivery_failed", 3, order_id="order-1", reason="upstream timeout"),
        ])
        self.assertEqual("observed", state["orders"]["order-1"]["payment_state"])
        self.assertEqual("delivery_failed", state["orders"]["order-1"]["delivery_state"])

    def test_invalidated_observation_reverts_capture_and_releases_claim(self):
        events = self.base() + [
            event("c1", "chain_observed", 2, attempt_id="attempt-1", network="base",
                  transaction_ref="0x1", log_index=0, amount_atomic=100),
            event("x1", "chain_observation_invalidated", 3, order_id="order-1",
                  transaction_ref="0x1", log_index=0),
        ]
        state = reduce_events(events)
        self.assertEqual("unknown", state["payment_attempts"]["attempt-1"]["outcome"])
        self.assertEqual({}, state["evidence_claims"])
        self.assertEqual(0, project_case(events)["expected_financials"]["captured_atomic"])

    def test_refund_is_capped_at_canonical_chain_capture(self):
        observed = self.base() + [
            event("c1", "chain_observed", 2, attempt_id="attempt-1", network="base",
                  transaction_ref="0x1", log_index=0, amount_atomic=10),
        ]
        refund = event("r1", "refund_settled", 4, refund_id="r1", order_id="order-1", amount_atomic=100)
        cases = {
            "partial capture": (observed + [refund], "refund_over_capture"),
            "invalidated capture": (observed + [
                event("x1", "chain_observation_invalidated", 3, order_id="order-1",
                      transaction_ref="0x1", log_index=0), refund], "refund_capture_unknown"),
        }
        for name, (events, expected) in cases.items():
            with self.subTest(name):
                state = reduce_events(events)
                self.assertEqual("proposed", state["refunds"]["r1"]["state"])
                self.assertIn(expected, {x["type"] for x in state["exceptions"].values()})
                self.assertEqual(0, project_case(events)["expected_financials"]["completed_refund_atomic"])

    def test_refund_amount_key_is_kept_in_projection(self):
        events = self.base() + [
            event("c1", "chain_observed", 2, attempt_id="attempt-1", network="base",
                  transaction_ref="0x1", log_index=0, amount_atomic=100),
            event("r1", "refund_settled", 3, refund_id="r1", order_id="order-1", amount=40),
        ]
        self.assertEqual(40, reduce_events(events)["refunds"]["r1"]["atomic_amount"])
        self.assertEqual(40, project_case(events)["expected_financials"]["completed_refund_atomic"])

    def test_events_sort_by_instant_and_naive_times_are_rejected(self):
        later_utc = {**event("o1", "order_created", 0, order_id="order-1", expected_atomic_amount=100),
                     "observed_at": "2027-01-01T00:30:00+00:00"}
        earlier_offset = {**event("a1", "payment_attempt_submitted", 0, attempt_id="attempt-1", order_id="order-1"),
                          "observed_at": "2027-01-01T01:00:00+02:00"}  # 23:00Z the previous day
        self.assertEqual(["a1", "o1"], reduce_events([later_utc, earlier_offset])["applied_event_ids"])
        with self.assertRaises(InvalidEvent):
            reduce_events([{**later_utc, "observed_at": "2027-01-01T00:30:00"}])

    def test_duplicate_event_id_with_different_content_is_rejected(self):
        original = event("o1", "order_created", 0, order_id="order-1", expected_atomic_amount=100)
        changed = event("o1", "order_created", 0, order_id="order-1", expected_atomic_amount=999)
        with self.assertRaises(InvalidEvent):
            reduce_events([original, changed])


class StoreTests(unittest.TestCase):
    def test_persistent_append_only_store_and_duplicate_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.sqlite"
            with EventStore(path) as store:
                self.assertTrue(store.append(event("o1", "order_created", 0, order_id="o", expected_atomic_amount=1)))
                self.assertFalse(store.append(event("o1", "order_created", 0, order_id="o", expected_atomic_amount=1)))
            with EventStore(path) as store:
                self.assertEqual(1, len(store.events()))
                with self.assertRaises(InvalidEvent):
                    store.append(event("o1", "order_created", 0, order_id="different", expected_atomic_amount=1))


if __name__ == "__main__":
    unittest.main()
