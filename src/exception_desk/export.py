"""Dependency-free, print-safe HTML export for the simulated operator desk.

All caller content is escaped at the HTML boundary. The optional JavaScript
only navigates server-rendered cases and simulates a refusal; it cannot perform
an operational action.
"""

from html import escape
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Sequence

_MISSING = "Not provided"


def _first(mapping: Mapping[str, Any], keys: Sequence[str], default: Any = _MISSING) -> Any:
    for key in keys:
        if key in mapping and mapping[key] is not None:
            return mapping[key]
    return default


def _text(value: Any) -> str:
    if value is None:
        return _MISSING
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return str(value)


def _value(value: Any) -> str:
    if isinstance(value, Mapping):
        if not value:
            return '<span class="missing">None provided</span>'
        rows = "".join(
            "<dt>{}</dt><dd>{}</dd>".format(escape(str(key)), _value(item))
            for key, item in value.items()
        )
        return '<dl class="details">{}</dl>'.format(rows)
    if isinstance(value, (list, tuple, set)):
        if not value:
            return '<span class="missing">None provided</span>'
        return "<ul>{}</ul>".format("".join("<li>{}</li>".format(_value(item)) for item in value))
    return escape(_text(value), quote=True)


def _section(title: str, body: str, section_id: str) -> str:
    return '<section id="{}"><h2>{}</h2>{}</section>'.format(
        escape(section_id, quote=True), escape(title), body
    )


def _state_card(label: str, state: Any, detail: Any) -> str:
    return (
        '<article class="state-card"><h3>{}</h3>'
        '<p class="state">{}</p><div class="state-detail">{}</div></article>'
    ).format(escape(label), _value(state), _value(detail))


def _policy_mapping(policy_results: Any) -> dict[str, Mapping[str, Any]]:
    if isinstance(policy_results, Mapping):
        return {
            str(name): metrics if isinstance(metrics, Mapping) else {"result": metrics}
            for name, metrics in policy_results.items()
        }
    policies: dict[str, Mapping[str, Any]] = {}
    if isinstance(policy_results, Iterable) and not isinstance(policy_results, (str, bytes)):
        for row in policy_results:
            if not isinstance(row, Mapping):
                continue
            name = str(_first(row, ("policy", "policy_name", "name"), ""))
            metrics = row.get("metrics", row)
            if name and isinstance(metrics, Mapping):
                policies[name] = metrics
    return policies


def _policy_label(name: str) -> str:
    return name.replace("_", "-").replace("-", " ").title().replace("Fifo", "FIFO")


# Value-weighted overdue is stored as atomic units x minutes; USDC has 6 decimals.
_ATOMIC_PER_USDC = 1_000_000
_METRIC_UNITS = {"value_weighted_overdue_minutes": "value_weighted_overdue (USDC-minutes)"}


def _metric_value(metric: str, value: Any) -> str:
    if metric == "value_weighted_overdue_minutes" and isinstance(value, (int, float)) and not isinstance(value, bool):
        return "{:,.1f}".format(value / _ATOMIC_PER_USDC)
    if isinstance(value, float):
        return "{:,.1f}".format(value)
    return _value(value)


def _policy_table(policy_results: Any) -> str:
    policies = _policy_mapping(policy_results)
    metrics = sorted(
        set().union(*(set(result) for result in policies.values()))
        - {"policy", "policy_name", "name", "outcomes"},
        key=str,
    ) if policies else []
    if not policies or not metrics:
        return '<p class="missing">No policy metrics provided.</p>'
    rows = "".join(
        '<tr><th scope="row">{}</th>{}</tr>'.format(
            escape(_METRIC_UNITS.get(str(metric), str(metric))),
            "".join('<td>{}</td>'.format(_metric_value(metric, result.get(metric, _MISSING)))
                    for result in policies.values()),
        )
        for metric in metrics
    )
    headings = "".join(
        '<th scope="col">{}</th>'.format(escape(_policy_label(name))) for name in policies
    )
    return (
        '<p class="note">Absolute values from the same simulated workload; no percentage-only comparison.</p>'
        '<div class="table-wrap" tabindex="0" aria-label="Scrollable policy comparison">'
        '<table><caption>Queue policy outcomes</caption><thead><tr><th scope="col">Metric</th>'
        '{}</tr></thead>'
        '<tbody>{}</tbody></table></div>'
    ).format(headings, rows)


def _timeline(projection: Mapping[str, Any]) -> str:
    events = _first(projection, ("evidence_timeline", "timeline", "events"), [])
    if not isinstance(events, Iterable) or isinstance(events, (str, bytes, Mapping)):
        events = []
    items = []
    for event in events:
        if isinstance(event, Mapping):
            heading = _first(event, ("event_type", "type", "name"), "Evidence event")
            event_id = _first(event, ("event_id", "id"), _MISSING)
            occurred = _first(event, ("occurred_at", "timestamp", "time"), _MISSING)
            omitted = {"event_type", "type", "name", "event_id", "id", "occurred_at", "timestamp", "time"}
            detail = {key: value for key, value in event.items() if key not in omitted}
            items.append('<li><h3>{}</h3><p class="timeline-meta">{} · {}</p>{}</li>'.format(
                escape(_text(heading)), escape(_text(occurred)), escape(_text(event_id)), _value(detail)
            ))
        else:
            items.append("<li>{}</li>".format(_value(event)))
    if not items:
        event_ids = _first(projection, ("applied_event_ids", "event_ids"), [])
        if isinstance(event_ids, Iterable) and not isinstance(event_ids, (str, bytes, Mapping)):
            items = ["<li><code>{}</code></li>".format(escape(_text(event_id))) for event_id in event_ids]
    return '<ol class="timeline">{}</ol>'.format("".join(items)) if items else '<p class="missing">No timeline evidence provided.</p>'


def _case_panel(projection: Mapping[str, Any], exception: Mapping[str, Any], index: int,
                traceability: Optional[Mapping[str, Any]] = None) -> str:
    payment_state = _first(projection, ("payment_state", "payment_status", "settlement_state"))
    delivery_state = _first(projection, ("delivery_state", "delivery_status", "fulfillment_state"))
    payment_detail = _first(projection, ("payment_evidence", "settlement_evidence", "payment"), {})
    delivery_detail = _first(projection, ("delivery_evidence", "fulfillment_evidence", "delivery"), {})
    evidence_gaps = _first(exception, ("evidence_gaps", "missing_evidence", "gaps"), [])
    allowed = _first(exception, ("allowed_actions", "permissible_actions", "next_actions"), [])
    forbidden = _first(exception, ("forbidden_actions", "prohibited_actions", "blocked_actions"), [])
    refund = _first(projection, ("refund_reservation", "refund_reservation_state", "refund"),
                    _first(exception, ("refund_reservation", "refund_reservation_state"), _MISSING))
    refund_state = refund.get("state", refund) if isinstance(refund, Mapping) else refund
    case_id = _first(projection, ("case_id", "order_id"), _first(exception, ("case_id", "exception_id")))
    identity = {key: projection[key] for key in (
        "case_id", "order_id", "attempt_id", "entity", "asset", "amount_atomic", "deadline"
    ) if key in projection} or {"case": case_id}
    excluded = {"evidence_gaps", "missing_evidence", "gaps", "allowed_actions", "permissible_actions",
                "next_actions", "forbidden_actions", "prohibited_actions", "blocked_actions",
                "refund_reservation", "refund_reservation_state"}
    exception_summary = {key: value for key, value in exception.items() if key not in excluded}
    trace = dict(traceability or {})
    for key in ("fixture_hash", "run_id", "applied_event_ids", "event_ids"):
        if key in projection and key not in trace:
            trace[key] = projection[key]
    trace.setdefault("case_id", case_id)
    actionable = bool(allowed)
    blocked = bool(evidence_gaps) or not actionable
    hidden = "" if index == 0 else " hidden"
    sections = [
        _section("Case identity", _value(identity), "case-identity-{}".format(index)),
        _section("Payment, delivery, and refund states", '<div class="state-grid">{}{}{}</div>'.format(
            _state_card("Payment state", payment_state, payment_detail),
            _state_card("Delivery state", delivery_state, delivery_detail),
            _state_card("Refund reservation state", refund_state, refund)), "states-{}".format(index)),
        _section("Evidence timeline", _timeline(projection), "evidence-timeline-{}".format(index)),
        _section("Exception summary", _value(exception_summary), "exception-summary-{}".format(index)),
        _section("Evidence gaps", _value(evidence_gaps), "evidence-gaps-{}".format(index)),
        _section("Operator action boundaries",
            '<div class="action-grid"><article class="allowed"><h3>Allowed next actions</h3>{}</article>'
            '<article class="forbidden"><h3>Forbidden actions</h3>{}</article></div>'
            '<div class="simulation-control"><button type="button" class="unsafe-action" '
            'aria-describedby="unsafe-help-{}">Simulate unsafe recharge</button>'
            '<p id="unsafe-help-{}" class="note">Training simulation only. No payment request is sent.</p>'
            '<p class="refusal" role="status" aria-live="polite">Not attempted.</p></div>'.format(
                _value(allowed), _value(forbidden), index, index), "actions-{}".format(index)),
        _section("Traceability", _value(trace), "traceability-{}".format(index)),
    ]
    return ('<article class="case-panel" id="case-panel-{}" data-case-index="{}" '
            'data-actionable="{}" data-blocked="{}" aria-labelledby="case-heading-{}"{}>'
            '<h2 class="case-heading" id="case-heading-{}">Case {}</h2>{}</article>').format(
        index, index, str(actionable).lower(), str(blocked).lower(), index, hidden,
        index, escape(_text(case_id)), "".join(sections))


def render_operator_report(projection: Mapping[str, Any], exception: Mapping[str, Any], policy_results: Any, *,
                           title: str = "Settlement-to-delivery exception",
                           stylesheet_href: str = "operator-report.css",
                           script_src: str = "operator-report.js",
                           cases: Optional[Sequence[Mapping[str, Any]]] = None,
                           traceability: Optional[Mapping[str, Any]] = None) -> str:
    """Return a complete interactive and printable report for simulated cases.

    Optional ``cases`` entries can provide ``projection``, ``exception``, and
    ``traceability`` mappings. Existing callers remain fully compatible.
    """
    normalized = [(projection, exception, traceability)]
    for case in cases or ():
        if not isinstance(case, Mapping):
            continue
        case_projection, case_exception = case.get("projection", case), case.get("exception", {})
        if isinstance(case_projection, Mapping) and isinstance(case_exception, Mapping):
            normalized.append((case_projection, case_exception, case.get("traceability")))
    options, panels = [], []
    for index, (case_projection, case_exception, case_trace) in enumerate(normalized):
        label = _first(case_projection, ("case_id", "order_id"),
                       _first(case_exception, ("case_id", "exception_id"), "Case {}".format(index + 1)))
        options.append('<option value="{}">{}</option>'.format(index, escape(_text(label))))
        panels.append(_case_panel(case_projection, case_exception, index,
                                  case_trace if isinstance(case_trace, Mapping) else None))
    toolbar = ('<nav class="desk-tools" aria-label="Case navigation">'
               '<div><label for="case-picker">Case</label><select id="case-picker">{}</select></div>'
               '<fieldset><legend>Show cases</legend>'
               '<label><input type="checkbox" id="filter-actionable"> Actionable</label>'
               '<label><input type="checkbox" id="filter-blocked"> Blocked</label></fieldset>'
               '<p id="filter-status" class="note" role="status" aria-live="polite">{} case(s) available.</p>'
               '</nav>').format("".join(options), len(normalized))
    return """<!doctype html>
<html lang="en" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>x402 payment exception desk: operator report</title>
  <meta name="description" content="Synthetic x402 payment exceptions on Base, replayed through one reducer and compared across four queue policies.">
  <link rel="canonical" href="https://rahilbhavan.github.io/x402-exception-desk/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="x402 payment exception desk: operator report">
  <meta property="og:description" content="Synthetic x402 payment exceptions on Base, replayed through one reducer and compared across four queue policies.">
  <meta property="og:url" content="https://rahilbhavan.github.io/x402-exception-desk/">
  <meta property="og:image" content="https://rahilbhavan.github.io/x402-exception-desk/social-card.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230f172a'/%3E%3Ctext x='32' y='43' font-family='Arial,sans-serif' font-size='28' font-weight='700' text-anchor='middle' fill='%2338bdf8'%3EXD%3C/text%3E%3C/svg%3E">
  <link rel="stylesheet" href="{stylesheet}">
  <script src="{script}" defer></script>
</head>
<body>
  <a class="skip-link" href="#case-workspace">Skip to case workspace</a>
  <header class="report-header">
    <p class="simulation-label">SIMULATED DATA — NOT LIVE — NO ACTIONS EXECUTED. NOT AFFILIATED WITH OR ENDORSED BY COINBASE.</p>
    <h1>{title}</h1>
    <p class="subtitle">Operator decision support. Verify evidence and authorization before acting.</p>
    <p><a href="operations-memo.pdf">Download the operations memo (PDF)</a></p>
  </header>
  <main id="case-workspace" tabindex="-1">{toolbar}{panels}{policy}</main>
  <footer>SIMULATED • Independent synthetic case study • Not affiliated with or endorsed by Coinbase • No live actions</footer>
</body>
</html>
""".format(title=escape(title), stylesheet=escape(stylesheet_href, quote=True),
           script=escape(script_src, quote=True), toolbar=toolbar, panels="".join(panels),
           policy=_section("Queue-policy comparison — absolute metrics", _policy_table(policy_results), "policy-comparison"))


def write_operator_report(output_path: Any, projection: Mapping[str, Any], exception: Mapping[str, Any],
                          policy_results: Any, **kwargs: Any) -> Path:
    """Write a rendered report and its dependency-free default script."""
    path = Path(output_path)
    path.write_text(render_operator_report(projection, exception, policy_results, **kwargs), encoding="utf-8")
    if kwargs.get("script_src", "operator-report.js") == "operator-report.js":
        script_source = Path(__file__).resolve().parents[2] / "web" / "operator-report.js"
        script_destination = path.parent / "operator-report.js"
        if script_source.exists() and script_source.resolve() != script_destination.resolve():
            script_destination.write_text(script_source.read_text(encoding="utf-8"), encoding="utf-8")
    return path
