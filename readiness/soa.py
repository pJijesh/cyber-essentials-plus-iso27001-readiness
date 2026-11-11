"""Draft Statement of Applicability built from the ISO rows of the workbook."""

from __future__ import annotations

from .datafiles import DataSet
from .workbook import NOT_APPLICABLE, Workbook

PLACEHOLDER = "TO COMPLETE: record the risk, legal or contractual reason this control is needed"

SOA_COLUMNS = (
    "control_id",
    "theme",
    "title",
    "included",
    "implementation_status",
    "justification",
    "evidence_ref",
    "owner",
    "ce_items_that_help",
)


def build_soa(dataset: DataSet, wb: Workbook) -> list[dict]:
    """One entry per Annex A control, in standard order."""
    entries = []
    for control in dataset.annex:
        row = wb.rows[control.id]
        included = row.status != NOT_APPLICABLE
        justification = row.notes
        if included and not justification:
            justification = PLACEHOLDER
        helping = []
        for ce_id, strength in dataset.ce_helping(control.id):
            ce_row = wb.rows.get(ce_id)
            state = ce_row.status if ce_row else "not assessed"
            helping.append(f"{ce_id} ({strength}, {state})")
        entries.append(
            {
                "control_id": control.id,
                "theme": control.theme,
                "title": control.title,
                "included": "Yes" if included else "No",
                "implementation_status": row.status,
                "justification": justification,
                "evidence_ref": row.evidence_ref,
                "owner": row.owner,
                "ce_items_that_help": "; ".join(helping),
            }
        )
    return entries


def summarise_soa(entries: list[dict]) -> dict:
    included = [e for e in entries if e["included"] == "Yes"]
    return {
        "controls": len(entries),
        "included": len(included),
        "excluded": len(entries) - len(included),
        "included_without_justification": sum(1 for e in included if e["justification"] == PLACEHOLDER),
    }


def soa_markdown(entries: list[dict], as_of: str) -> str:
    summary = summarise_soa(entries)
    lines = [
        "# Statement of Applicability (draft)",
        "",
        f"As-of date: {as_of}",
        "",
        "> Draft generated from the assessment workbook. It is a working document, not a "
        "completed Statement of Applicability. Each included control needs a documented reason "
        "linked to your risk assessment and risk treatment plan, and each exclusion needs a "
        "justification that an auditor will accept. Control titles are short paraphrases.",
        "",
        f"Controls: {summary['controls']}. Included: {summary['included']}. "
        f"Excluded: {summary['excluded']}. "
        f"Included controls still without a justification: {summary['included_without_justification']}.",
        "",
    ]
    themes: list[str] = []
    for e in entries:
        if e["theme"] not in themes:
            themes.append(e["theme"])
    for theme in themes:
        lines += [f"## {theme}", "", "| Control | Title | Included | Status | Justification | CE items that help |",
                  "| --- | --- | --- | --- | --- | --- |"]
        for e in entries:
            if e["theme"] != theme:
                continue
            lines.append(
                "| {id} | {title} | {inc} | {status} | {just} | {ce} |".format(
                    id=e["control_id"],
                    title=_cell(e["title"]),
                    inc=e["included"],
                    status=e["implementation_status"],
                    just=_cell(e["justification"]),
                    ce=_cell(e["ce_items_that_help"]) or "none",
                )
            )
        lines.append("")
    return "\n".join(lines)


def _cell(text: str) -> str:
    return text.replace("|", "/").replace("\n", " ").strip()
