# Settlement exception state model

**Status: verified against 16 synthetic fixtures on 2026-09-20.** This model is project-owned and does not describe Coinbase systems.

## Independent state axes

| Axis | States | Rule |
|---|---|---|
| Payment | `not_submitted`, `unknown`, `failed`, `observed`, `conflicted` | A timeout is `unknown`, never `failed`. Only matching canonical evidence produces `observed`. |
| Fulfillment | `not_started`, `preparation_failed`, `prepared`, `delivery_failed`, `delivered` | Payment does not advance delivery. Delivery acknowledgment is separate evidence. |
| Refund | `none`, `approved_reserved`, `submitted_unknown`, `settled`, `failed_released` | Unknown submission retains its reservation. Settled plus reserved cannot exceed capture. |
| Exception | `blocked`, `actionable`, `closed` | Rules recommend or block; an operator approves retry or refund. |

## Safe transition rules

- Settlement timeout opens reconciliation on the original attempt. It does not authorize another charge.
- Late matching payment evidence updates the original attempt and unlocks recovery of the persisted resource.
- Conclusive failure makes a reviewed retry eligible; it never triggers an automatic retry.
- One `(network, transaction reference, log index)` claim belongs to one order. Reuse opens a conflict.
- A paid order can have one entitlement. Duplicate requests return the persisted result.
- Pre-finality evidence invalidation reopens the payment conclusion and any dependent closure.
- Refund approval first reserves the amount. An unknown outcome remains reserved until settlement or conclusive failure.

## Closure evidence

Closure requires matching payment evidence or conclusive failure, resource/delivery disposition, and refund disposition when applicable. Notes, HTTP timeouts, authorization validity, or a facilitator request alone are not closure evidence.

