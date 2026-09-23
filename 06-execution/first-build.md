# Original first-build plan: 28–36 focused hours

This section is the historical implementation plan. The completed build used dependency-free Python 3.9+, SQLite, and static HTML instead of the candidate Node/TypeScript stack below; current build status is recorded in the root README and release-readiness record.

| Stage | Hours | Exit gate |
|---|---:|---|
| Freeze sources and author schema/oracle | 4–5 | 16 cases reviewed by hand; protocol commit recorded |
| Event store, reducer, projections | 7–9 | replay/restart/late-evidence golden tests pass |
| Exception rules and operator actions | 4–5 | each case has owner, evidence gap, allowed/forbidden action, closure test |
| Reconciliation export and hand case | 3–4 | atomic-unit balances match exactly |
| FIFO and deadline-first runner | 4–5 | same fixture hash/capacity; adverse and sensitivity runs produced |
| Minimal case/queue interface | 3–4 | reviewer can find next action and evidence; simulation label visible |
| Memo, validation record, demo | 3–4 | claim-to-run traceability and explicit limitations |

## Dependencies and sequence

Candidate stack: current supported Node.js, TypeScript, SQLite, a test runner, and CSV/XLSX export library; select exact versions only at implementation time and record them. A static local HTML view is the fallback if a UI framework adds setup risk. No production dependency is authorized by this plan.

Day 1 freezes the x402 source revision and authors fixtures before code. Days 2–3 implement state/reconciliation. Day 4 runs control tests. Day 5 runs policy experiments. Day 6 builds the minimal view and reviewer packet. Day 7 records memo/demo only after checks. Do not implement policy ranking until V01–V08 pass.

## Milestone-one acceptance

The 16-case corpus and oracle exist; all ledger/control checks pass or failures are prominently recorded; a reader can reproduce one reconciliation and one policy metric from source rows; unknown settlement never causes automatic recharge; delivery recovery reuses the original entitlement; refund reservations prevent over-refund; the recommendation follows the declared gate. Live transactions and external review are not required.
