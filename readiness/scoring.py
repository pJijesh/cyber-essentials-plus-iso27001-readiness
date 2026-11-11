"""Coverage, gaps and evidence hygiene calculations.

Scoring rule: implemented counts 1, partial counts 0.5, not started counts 0.
Items marked not applicable leave the denominator, so they neither help nor hurt,
but they are listed with their justification.
"""

from __future__ import annotations

from datetime import date

from .datafiles import DataSet
from .workbook import IMPLEMENTED, NOT_APPLICABLE, NOT_STARTED, PARTIAL, Row, Workbook

STATUS_WEIGHT = {IMPLEMENTED: 1.0, PARTIAL: 0.5, NOT_STARTED: 0.0}

# Cyber Essentials areas that the scheme treats as automatic failures in 2026, so a gap
# here is listed first. Basis: IASME announcement of the April 2026 changes (MFA on cloud
# services, 14 day installation of critical and high updates for operating systems and
# firmware, and for applications) and the IASME FAQ (unsupported software in scope).
CE_PRIORITY_IDS = (
    "CE-UAC-04",
    "CE-UPD-01",
    "CE-UPD-02",
    "CE-UPD-04",
    "CE-UPD-05",
)

CE_PRIORITY_REASON = {
    "CE-UAC-04": "MFA not enabled on a cloud service that offers it is an automatic fail",
    "CE-UPD-01": "Unsupported software in scope is an automatic fail",
    "CE-UPD-02": "Unsupported software in scope is an automatic fail",
    "CE-UPD-04": "Critical or high operating system and firmware updates must be installed within 14 days",
    "CE-UPD-05": "Critical or high application updates must be installed within 14 days",
}


def coverage_percent(implemented: int, partial: int, applicable: int) -> float | None:
    if applicable == 0:
        return None
    return round(100.0 * (implemented + 0.5 * partial) / applicable, 1)


def _tally(rows: list[Row]) -> dict:
    counts = {IMPLEMENTED: 0, PARTIAL: 0, NOT_STARTED: 0, NOT_APPLICABLE: 0}
    for r in rows:
        counts[r.status] += 1
    applicable = counts[IMPLEMENTED] + counts[PARTIAL] + counts[NOT_STARTED]
    return {
        "total": len(rows),
        "applicable": applicable,
        "implemented": counts[IMPLEMENTED],
        "partial": counts[PARTIAL],
        "not_started": counts[NOT_STARTED],
        "not_applicable": counts[NOT_APPLICABLE],
        "coverage_percent": coverage_percent(counts[IMPLEMENTED], counts[PARTIAL], applicable),
    }


def score(dataset: DataSet, wb: Workbook, as_of: date, review_days: int = 365) -> dict:
    """Return a JSON-ready dictionary with everything the report needs."""
    universe: list[tuple[str, str, str, str]] = []  # scope, id, theme, title
    if wb.has_ce:
        universe += [("ce", c.id, c.theme, c.requirement) for c in dataset.ce_items]
    if wb.has_iso:
        universe += [("iso", a.id, a.theme, a.title) for a in dataset.annex]
    order = {item[1]: i for i, item in enumerate(universe)}

    scopes: dict[str, dict] = {}
    for scope in ("ce", "iso"):
        items = [u for u in universe if u[0] == scope]
        if not items:
            continue
        rows = [wb.rows[u[1]] for u in items]
        themes = []
        for theme in dataset.themes(scope):
            t_rows = [wb.rows[u[1]] for u in items if u[2] == theme]
            entry = {"theme": theme}
            entry.update(_tally(t_rows))
            themes.append(entry)
        scopes[scope] = {"overall": _tally(rows), "themes": themes}

    gaps = []
    for scope, item_id, theme, title in universe:
        row = wb.rows[item_id]
        if row.status in (NOT_STARTED, PARTIAL):
            gaps.append(
                {
                    "scope": scope,
                    "id": item_id,
                    "theme": theme,
                    "title": title,
                    "status": row.status,
                    "owner": row.owner,
                    "notes": row.notes,
                    "priority": item_id in CE_PRIORITY_IDS,
                }
            )
    gaps.sort(
        key=lambda g: (
            0 if g["priority"] else 1,
            0 if g["scope"] == "ce" else 1,
            0 if g["status"] == NOT_STARTED else 1,
            order[g["id"]],
        )
    )

    ce_priority = []
    if wb.has_ce:
        for item_id in CE_PRIORITY_IDS:
            row = wb.rows[item_id]
            ce_priority.append(
                {
                    "id": item_id,
                    "requirement": dataset.ce_by_id[item_id].requirement,
                    "why_it_matters": CE_PRIORITY_REASON[item_id],
                    "status": row.status,
                }
            )

    overdue, unreviewed, missing_evidence = [], [], []
    for scope, item_id, theme, title in universe:
        row = wb.rows[item_id]
        if row.status not in (IMPLEMENTED, PARTIAL):
            continue
        if row.last_reviewed is None:
            unreviewed.append({"scope": scope, "id": item_id, "title": title, "owner": row.owner})
        else:
            age = (as_of - row.last_reviewed).days
            if age > review_days:
                overdue.append(
                    {
                        "scope": scope,
                        "id": item_id,
                        "title": title,
                        "owner": row.owner,
                        "last_reviewed": row.last_reviewed.isoformat(),
                        "days_since_review": age,
                        "days_overdue": age - review_days,
                    }
                )
        if not row.evidence_ref:
            missing_evidence.append(
                {"scope": scope, "id": item_id, "title": title, "status": row.status, "owner": row.owner}
            )
    overdue.sort(key=lambda o: (-o["days_overdue"], order[o["id"]]))

    not_applicable = [
        {
            "scope": scope,
            "id": item_id,
            "title": title,
            "justification": wb.rows[item_id].notes,
            "owner": wb.rows[item_id].owner,
        }
        for scope, item_id, theme, title in universe
        if wb.rows[item_id].status == NOT_APPLICABLE
    ]

    return {
        "as_of": as_of.isoformat(),
        "review_days": review_days,
        "scoring_rule": "implemented 1.0, partial 0.5, not started 0.0, not applicable excluded",
        "scopes": scopes,
        "ce_priority": ce_priority,
        "gaps": gaps,
        "overdue_reviews": overdue,
        "no_review_date": unreviewed,
        "missing_evidence": missing_evidence,
        "not_applicable": not_applicable,
    }
