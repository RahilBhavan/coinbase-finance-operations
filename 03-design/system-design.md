# System and data design

## Architecture

`fixtures → append-only events → deterministic reducer → payment/fulfillment projections → exception rules → policy runner → CSV/XLSX/UI/memo`


The reducer is pure: ordered events plus a policy version produce projections. Ingestion uniqueness is enforced by `event_id`; payment evidence has a unique `(network, transaction_ref, log_index)` claim. A stable `order_idempotency_key` binds one business purchase. Unknown outcomes remain open.

## Core records

| Record | Essential fields/invariants |
|---|---|
| Order | order ID, idempotency key, entity, asset, expected atomic amount, resource digest, deadline |
| Authorization | fingerprint, payer, recipient, nonce, valid interval, verification result; validity is not settlement |
| PaymentAttempt | attempt ID, order, submitted time, outcome=`unknown|failed|observed`; never overwrite unknown with a new attempt |
| ChainObservation | tx/log key, block, stage, canonical flag, occurred/observed times; many per attempt |
| Fulfillment | prepared digest, delivery attempt, acknowledgment and failure reason; separate from payment |
| Refund | original payment, approved/reserved/settled atomic amount, destination evidence, state |
| Exception | type, actionable/blocked, owner, SLA, evidence gaps, permissible actions, closure evidence |
| PolicyRun | fixture hash, reducer/policy version, seed, capacity, metrics, timestamp |

Amounts are integers in atomic units. Never aggregate across asset or entity. `completed_refunds + active_reservations <= captured_amount`. One evidence claim cannot satisfy two orders. A late canonical observation updates the original attempt and reopens dependent conclusions when necessary.

## State transitions and permissions

- `unknown → observed|failed`; never infer `failed` from timeout.
- `prepared → delivery_pending → delivered|delivery_failed`; settled does not imply delivered.
- `refund_proposed → approved_reserved → submitted_unknown → settled|failed_released`; only `failed_released` frees a reservation.
- Only an operator decision may approve refund or retry. Rules may recommend, block, or escalate.
- Closure requires payment evidence, fulfillment evidence, and any refund evidence to reconcile; a note alone is not evidence.

## Queue experiment

FIFO and deadline-first receive identical event arrival times, evidence availability, case durations, capacity, and control rules. Blocked cases consume no imaginary resolution. Metrics: overdue count, median/p95 delay, value-weighted overdue time, manual touches, recovered deliveries without new payment, control failures, and unfinished count/value by type. Use regular, urgent-small-case burst, large-complex-case, and delayed-evidence scenarios plus half/double service-time sensitivity.

