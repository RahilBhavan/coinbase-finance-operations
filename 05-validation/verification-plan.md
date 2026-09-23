# Verification plan

No checks below have been run against an implementation.

| Check | Expected result |
|---|---|
| V01 duplicate event replay | same projections, balances, entitlements, and exception count |
| V02 restart and shuffled ingestion | canonical event ordering reproduces identical state; invalid ordering is reported |
| V03 timeout then late success | original attempt becomes observed; no second charge or entitlement |
| V04 conclusive failure | retry remains human-reviewed and only after original attempt resolves |
| V05 evidence reused across orders | conflict opens; neither second order nor balance closes silently |
| V06 finality-stage removal | dependent release/closure is reopened or blocked per declared policy |
| V07 concurrent refunds | completed plus reserved never exceeds capture; unknown keeps reservation |
| V08 atomic reconciliation | exact integer equality by asset/entity; no floating-point conversion in ledger |
| V09 policy fairness | identical input hash, capacity, durations, and evidence timing for both policies |
| V10 no future leakage | policy sees only evidence observed by decision time |
| V11 held-out gate | absolute metrics, failures, and unfinished cases reported even if baseline wins |
| V12 traceability | memo number links to run ID, fixture hash, metric definition, and incident evidence |

For each run record: check ID, exact command, input/version hash, expected, actual, exit status, evidence path, date, and reviewer. Use golden fixture assertions, reducer property tests, database uniqueness constraints, a hand-calculated reconciliation, and a clean-clone reproduction. A failing control removes the policy recommendation until fixed or explicitly narrows the claim.

