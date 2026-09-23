# External operator-review protocol

Status: ready to run; **no external reviewers have completed it**. This protocol must be used unchanged for every participant so results are comparable.

## Participants and setup

Find at least three practitioners who have handled payments, treasury, reconciliation, risk, or customer-funds exceptions. Record role family and relevant experience band, but no employer-confidential information. Give each reviewer the same generated build, runbook, and three tasks below. Do not coach after timing begins.

The facilitator records screen or notes with consent, starts the timer when the task is revealed, and stops it when the reviewer states a decision and cites evidence. A reviewer may answer “insufficient evidence”; that is a valid decision.

## Three identical tasks

1. **Timeout / late settlement:** Decide whether to charge again, recover delivery, refund, or wait. Cite the payment evidence and the rule that governs the decision.
2. **Evidence mismatch:** Decide whether the case may be recognized as paid and delivered. Identify every mismatched field and the safe next action.
3. **Unknown refund outcome:** Decide whether another refund may be approved. Calculate the presently refundable balance and name the evidence required to release the reservation.

For each task, ask only: “What is your decision, what evidence supports it, and what would you do next?” Then collect confidence from 1 (guessing) to 5 (certain).

## Error taxonomy

| Code | Error | Critical? |
|---|---|---|
| C1 | recommends a second charge while original settlement is unresolved or observed | yes |
| C2 | recognizes mismatched or conflicted evidence as a valid capture | yes |
| C3 | approves value above captured less completed and reserved refunds | yes |
| C4 | treats chain settlement as proof of delivery | yes |
| E1 | reaches a safe action but cites incomplete evidence | no |
| E2 | misses an evidence gap or closure condition | no |
| N1 | cannot find the relevant case, state, or action boundary | no |
| N2 | uses ambiguous language that prevents a decision from being executed safely | no |

## Scoring and exact pass criteria

Score each task out of 4: correct disposition (2), correct evidence cited (1), and correct next action/closure evidence (1). Maximum is 12 per reviewer.

The review passes only when all of these are true:

- at least three qualified practitioners complete all three tasks without coaching;
- zero C1–C4 critical errors across all sessions;
- every reviewer scores at least 10/12;
- median completion time is at most 180 seconds per task;
- median confidence is at least 4/5;
- all N1 navigation failures and recurring E1/E2 errors are logged and either fixed or explicitly accepted with rationale;
- the build run ID and artifact hashes used by every reviewer are recorded.

## Result record

Record one row per task: anonymous reviewer ID, role family, experience band, run ID, task, start/end or elapsed seconds, decision, evidence cited, next action, error codes, score, confidence, and unprompted observations. Preserve failures; do not average them away.

## Honest interpretation

Passing supports the narrow claim that a small practitioner sample could use this simulated interface to resolve three scripted exception types safely and quickly. It does not prove production usability, staffing impact, protocol interoperability, or generalization to other cases. Fewer than three reviewers, any coaching, changed tasks, missing timing, or incomplete records makes the result **inconclusive**, not a pass. Report individual results and ranges alongside medians; never invent participants or convert this protocol’s readiness into evidence of completed review.
