# Synthetic incident corpus v1

`incidents-v1.jsonl` contains fictional, deterministic event histories for four happy paths and twelve required exceptions. Every line is one observed input event. Amounts are integer atomic units, timestamps are UTC, and per-fixture `sequence` values define ingestion order; `occurred_at` may precede a prior event's occurrence when evidence arrives late.

`incidents-v1.oracle.json` is deliberately separate. It contains expected terminal projections, exception classification, allowed and forbidden actions, closure evidence, and financial totals. Reducer or policy code must not ingest the oracle in normal execution.

Evidence labels describe provenance, not truth or finality:

- `synthetic_business_record`: fictional order, resource, or delivery record.
- `synthetic_protocol_evidence`: fictional verification or settlement response shaped by the protocol model.
- `synthetic_chain_observation`: fictional chain-stage evidence; inspect `canonical` and `finality_stage` where present.
- `synthetic_system_observation`: fictional timeout or processing observation.
- `synthetic_control_observation`: fictional duplicate/conflict control result.
- `synthetic_operator_decision`: fictional human approval that does not itself prove settlement.

The corpus performs no network requests, signatures, wallet operations, or transactions. It does not represent Coinbase production data or incident frequencies.
