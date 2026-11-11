"""Render the scoring result as Markdown."""

from __future__ import annotations

SCOPE_LABEL = {"ce": "Cyber Essentials", "iso": "ISO/IEC 27001 Annex A"}

NOTICE = (
    "> This report is a planning aid based on self-reported status. It is not an assessment, "
    "an audit or a certification decision. Cyber Essentials is a baseline subset of what ISO/IEC "
    "27001 expects, so certification to one does not imply the other. Check requirements against "
    "the current published scheme documents."
)


def _cell(text: object) -> str:
    return str(text).replace("|", "/").replace("\n", " ").strip()


def _pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.1f}%"


def _table(header: list[str], rows: list[list[object]]) -> list[str]:
    out = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
    for row in rows:
        out.append("| " + " | ".join(_cell(c) for c in row) + " |")
    return out


def render_report(result: dict, workbook_name: str) -> str:
    lines = [
        "# Readiness report",
        "",
        f"Workbook: {workbook_name}. As-of date: {result['as_of']}. "
        f"Evidence review interval: {result['review_days']} days.",
        "",
        NOTICE,
        "",
        f"Scoring rule: {result['scoring_rule']}.",
        "",
        "## Summary",
        "",
    ]
    rows = []
    for scope, data in result["scopes"].items():
        o = data["overall"]
        rows.append([SCOPE_LABEL[scope], o["total"], o["applicable"], o["implemented"], o["partial"],
                     o["not_started"], o["not_applicable"], _pct(o["coverage_percent"])])
    lines += _table(["Scope", "Items", "Applicable", "Implemented", "Partial", "Not started",
                     "Not applicable", "Coverage"], rows)
    lines.append("")

    lines += ["## Coverage by theme", ""]
    for scope, data in result["scopes"].items():
        lines += [f"### {SCOPE_LABEL[scope]}", ""]
        rows = [[t["theme"], t["total"], t["implemented"], t["partial"], t["not_started"],
                 t["not_applicable"], _pct(t["coverage_percent"])] for t in data["themes"]]
        lines += _table(["Theme", "Items", "Implemented", "Partial", "Not started",
                         "Not applicable", "Coverage"], rows)
        lines.append("")

    if result["ce_priority"]:
        lines += [
            "## Cyber Essentials automatic fail areas",
            "",
            "These items are treated as automatic failures by the scheme as of the April 2026 changes "
            "(see docs/sources.md). Close any gap here before booking an assessment.",
            "",
        ]
        lines += _table(["Id", "Requirement", "Why it matters", "Status"],
                        [[p["id"], p["requirement"], p["why_it_matters"], p["status"]]
                         for p in result["ce_priority"]])
        lines.append("")

    lines += ["## Gaps", ""]
    if not result["gaps"]:
        lines += ["No gaps: every applicable item is marked implemented.", ""]
    else:
        n_pri = sum(1 for g in result["gaps"] if g["priority"])
        lines += [
            f"{len(result['gaps'])} items are not started or partial. {n_pri} of them are automatic "
            "fail areas and are listed first.",
            "",
        ]
        lines += _table(
            ["Id", "Scope", "Theme", "Item", "Status", "Owner", "Priority", "Notes"],
            [[g["id"], SCOPE_LABEL[g["scope"]], g["theme"], g["title"], g["status"],
              g["owner"] or "unassigned", "auto fail area" if g["priority"] else "", g["notes"]]
             for g in result["gaps"]],
        )
        lines.append("")

    lines += ["## Evidence and review hygiene", ""]
    lines += [f"### Overdue evidence reviews ({len(result['overdue_reviews'])})", ""]
    if result["overdue_reviews"]:
        lines += _table(
            ["Id", "Item", "Owner", "Last reviewed", "Days overdue"],
            [[o["id"], o["title"], o["owner"] or "unassigned", o["last_reviewed"], o["days_overdue"]]
             for o in result["overdue_reviews"]],
        )
    else:
        lines.append("None.")
    lines += ["", f"### Implemented or partial with no review date ({len(result['no_review_date'])})", ""]
    if result["no_review_date"]:
        lines += _table(["Id", "Item", "Owner"],
                        [[u["id"], u["title"], u["owner"] or "unassigned"] for u in result["no_review_date"]])
    else:
        lines.append("None.")
    lines += ["", f"### Implemented or partial with no evidence reference ({len(result['missing_evidence'])})", ""]
    if result["missing_evidence"]:
        lines += _table(["Id", "Item", "Status", "Owner"],
                        [[m["id"], m["title"], m["status"], m["owner"] or "unassigned"]
                         for m in result["missing_evidence"]])
    else:
        lines.append("None.")
    lines.append("")

    lines += [f"## Not applicable items ({len(result['not_applicable'])})", ""]
    if result["not_applicable"]:
        lines += ["Each exclusion needs a justification that an assessor or auditor will accept.", ""]
        lines += _table(["Id", "Scope", "Item", "Justification"],
                        [[n["id"], SCOPE_LABEL[n["scope"]], n["title"], n["justification"]]
                         for n in result["not_applicable"]])
    else:
        lines.append("None.")
    lines.append("")
    return "\n".join(lines)
