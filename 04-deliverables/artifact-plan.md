# Deliverables and acceptance criteria

The package was built locally and revalidated on 2026-09-22. “Built” means the file exists and its automated checks pass; it does not imply production readiness or practitioner endorsement.

| ID | Status | Output | Acceptance criterion |
|---|---|---|---|
| FO-01 | Built | `artifacts/operations-memo.pdf` | recommendation, baseline, absolute metrics, limitations, and counterargument |
| FO-02 | Built | `artifacts/state-model.md` | every fixture maps to payment state, delivery state, exception, permissible action, and closure evidence |
| FO-03 | Built | `artifacts/incidents-v1.jsonl` + oracle | 16 deterministic cases; unique IDs; schema and fixture hash; expected outcomes authored before implementation |
| FO-04 | Built | `artifacts/reconciliation.xlsx` | captures − completed refunds − reservations = available refundable balance exactly by asset/entity; one hand-worked case |
| FO-05 | Built | `artifacts/policy-results.csv` | identical workloads/controls; unresolved work retained; run metadata included |
| FO-06 | Built | `artifacts/operator-runbook.md` | owner, evidence, safe action, forbidden action, escalation, closure test for every exception type |
| FO-07 | Built | `artifacts/validation-report.md` | command, expected/actual, evidence path, date, and visible limitations |
| FO-08 | Protocol ready; external review pending | `artifacts/operator-task-protocol.md` | same task/rubric for eligible reviewers; critical errors, time, confidence |
| FO-09 | Built | `artifacts/demo.mp4` | synthetic label; unknown-vs-failed, delivery recovery, refund reservation, policy tradeoff |
| FO-10 | Built | `artifacts/source-register.csv` | source version/date, claim supported, evidence label, assumption links, access limitations |

Ready-to-share requires all required artifacts, reproducible key numbers, no unresolved material control failure, prominent limitations, and a reviewer packet usable without wallet/account. It does not mean production-ready.
