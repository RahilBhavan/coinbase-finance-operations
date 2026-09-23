# Operator runbook

**Scope:** synthetic fixed-price x402 `exact` report orders on Base Sepolia. Never use this runbook for live funds.

| Exception | Owner | Inspect | Allowed next action | Forbidden | Close when |
|---|---|---|---|---|---|
| Authorization rejected | Service operations | requirements, signature-verification reason | request corrected authorization or cancel | prepare, settle, deliver | rejection disposition recorded |
| Preparation failed | Delivery operations | resource job, digest, error | retry preparation or cancel | settle or deliver | preparation succeeds or order cancels |
| Settlement timed out | Payments operations | original attempt, facilitator result, chain observations | reconcile original attempt | new charge or entitlement | matching evidence or conclusive failure |
| Settlement failed | Payments operations | signed request, failure code, expiry | reviewed retry or cancel | automatic retry or delivery | retry/cancellation disposition |
| Paid, delivery failed | Delivery operations | payment claim, resource digest, delivery log | recover persisted resource, retry delivery, or propose refund | charge again | acknowledgment or settled refund |
| Duplicate request | Service operations | idempotency key, original result | return persisted response | new charge, resource, or entitlement | original outcome returned |
| Second authorization | Payments operations | original paid order, unused authorization | invalidate unused authorization, investigate retry | settle second authorization | unused authorization disposition |
| Evidence mismatch | Payments operations | network, asset, amount, recipient, tx/log | quarantine and request matching evidence | recognize capture or deliver | all fields match or evidence rejected |
| Cross-order evidence claim | Risk operations | both orders, unique claim index | preserve first valid claim, investigate second | close second order paid | unique ownership established |
| Observation invalidated | Payments operations | prior stage, canonical history | await canonical evidence | deliver, charge again, close paid | replacement evidence or failure |
| Refund outcome unknown | Treasury operations | original payer, capture, reservations, refund tx | reconcile original refund and retain reservation | release reservation or submit excess refund | settlement or conclusive failure |

Escalate any evidence conflict, refund-cap breach, cross-entity/asset mismatch, or attempt to override a forbidden action. Preserve every event; correct with a new event rather than mutation.

