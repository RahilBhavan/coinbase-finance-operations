# Decision brief

## Business decision

Choose the handling policy for a fixed-capacity exception team: **FIFO** or **deadline-first among actionable cases, with unresolved value as tie-breaker**. Adopt the proposed policy only if, on identical held-out workloads, it reduces overdue cases without any duplicate charge, duplicate entitlement, cross-order evidence reuse, excess refund, or incorrect closure, and without materially worsening value-weighted overdue time.

This is not a generic dashboard. The unit of work is an exception whose payment and service obligations may disagree.

## Required distinctions

| Situation | Meaning | Safe action |
|---|---|---|
| Settle request timed out | outcome unknown | reconcile the original attempt; suppress a new charge |
| Conclusive settlement failure | no captured payment under the modeled evidence rule | reviewed retry may be eligible |
| Payment observed, delivery unacknowledged | paid, service obligation unresolved | recover the persisted report; do not charge again |
| Duplicate request/evidence | replay or cross-order conflict | return persisted outcome or escalate; create no new entitlement |
| Refund approved but unsettled | reservation consumes refundable balance | keep reservation until conclusive outcome |
| Refund settled | linked return of value observed | reduce refundable balance; preserve original capture |

## Decision rule

Proposed gate (a design choice, not an observed benchmark): on a held-out regular workload, at least 15% fewer overdue cases; zero control failures in all scenarios; and no more than 10% worse value-weighted overdue time in any adverse scenario. Report absolute counts and unfinished work. If the gate fails, retain FIFO or apply deadline-first only to a narrower case class.

## Audience and claim boundary

Primary audience: finance-operations or payments-operations reviewer. Secondary audience: Product/Engineering partner. The project may demonstrate analytical judgment, controls, reconciliation, and handoff design. It must not claim Coinbase process knowledge, production readiness, customer identity, real savings, legal sufficiency, or hiring eligibility.

