# Changelog

## v1.1.0 (2026-09-23)

### Fixed

- Refunds are capped at the canonical on-chain capture, not at any observed payment evidence.
- Refund amounts given under the `amount` key are kept instead of read as zero.
- The simulation no longer leaves an operator idle when a case still fits before the horizon.
- Events are ordered by parsed, timezone-aware timestamps instead of raw strings.
- A reused event ID with different content is rejected instead of silently accepted.

### Changed

- Value-weighted overdue time is shown in USDC-minutes in the report, README, memo, and workbook.
- The report, memo, and README state that the project is not affiliated with or endorsed by Coinbase.
- The repository is renamed to `x402-exception-desk`, and the release archive is now `outputs/x402-exception-desk-package.zip`.
- The operator report has link-preview metadata, a favicon, and a social card.
- The memo PDF builds with fixed dates and document ID, so rebuilds are byte-identical.
- A weekly link check and Dependabot updates for GitHub Actions run in CI.
