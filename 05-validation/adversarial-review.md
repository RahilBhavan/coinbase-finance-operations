# Adversarial quality review

## Strongest weaknesses

1. **Synthetic realism.** Protocol-shaped records do not establish realistic incident frequency, staffing, or loss. Mitigation: scenario grid and sensitivity, no savings claim.
2. **Role uncertainty.** The current Finance Operations role scope is unverified. Mitigation: treat the project as an analogy and revisit it once the role description is confirmed.
3. **Finality policy is business-specific.** Documentation describes stages, not which stage a fictional seller should accept. Mitigation: declare the release rule and rerun at a stronger stage.
4. **Delivery proof is application-owned.** x402 settlement does not prove client receipt. Mitigation: explicit resource digest, delivery attempt, and acknowledgment model.
5. **Queue metric gaming.** Deadline-first can improve counts while delaying a high-value case. Mitigation: adverse workload, value-weighted metric, unfinished value, and narrow-policy fallback.
6. **Usability evidence may be weak.** Three convenience reviewers cannot validate production usability. Mitigation: report task errors without broad claims; labeled self-review if nobody participates.
7. **Event sourcing can become portfolio theater.** Mitigation: one SQLite database, one reducer, no services or live integration in milestone one.

## Scope cuts, in order

Cut live Base Sepolia first, then UI animation/polish, AI-generated notes, large 500-order simulation, and external usability study. Preserve the hand-authored oracle, reducer, reconciliation, control tests, one policy comparison, memo, and demo. Never cut duplicate-charge, unknown-outcome, refund-reservation, or traceability controls.

## Pre-mortem

If the project fails, likely causes are an interface built before states are correct, assumed metrics presented as operational truth, an unpinned changing protocol, or an opaque recommendation that no one can defend. Stop the build when the 16 fixtures cannot be hand-reconciled, material source semantics remain unresolved, or the memo depends on UI output that cannot be reproduced independently.

