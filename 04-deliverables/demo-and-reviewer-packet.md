# Demo storyboard and reviewer packet

## Three-minute storyboard

The narrated video captures the original FIFO-versus-deadline-first decision. The generated operator report and policy exports are the current source for the later four-policy comparison and 3,600-scenario sensitivity sweep.

1. **0:00–0:25 — Decision.** Fictional report seller, synthetic fixtures, FIFO versus deadline-first gate.
2. **0:25–1:05 — Ambiguity.** Open a settle timeout. Show authorization valid, outcome unknown, reconciliation task, and disabled “charge again.” Late payment evidence attaches to the original attempt.
3. **1:05–1:35 — Delivery recovery.** Payment observed but acknowledgment absent. Verify persisted resource digest, redeliver entitlement, and close without another payment.
4. **1:35–2:00 — Refund control.** Two proposals contend for the same refundable balance. Reservation blocks over-refund while unknown submission remains reserved.
5. **2:00–2:40 — Policy result.** Same workload under both queues, including one adverse scenario where deadline-first loses on value-weighted delay.
6. **2:40–3:00 — Recommendation and limits.** State whether gate passed, which assumption matters most, and why results do not generalize to Coinbase.

## Reviewer packet

Order: one-page cover → decision memo → one annotated incident → reconciliation excerpt → policy comparison → validation summary → source/assumption register → feedback form.

Ask only three questions:

1. At the timeout incident, is the next action and forbidden action unambiguous?
2. Which evidence would you require before retry, delivery recovery, refund, and closure?
3. Does the policy recommendation survive the adverse case, or should its use be narrower?

Record reviewer role, version, date, answer, change made, and unresolved disagreement. Do not imply endorsement. No outreach is authorized by this package.
