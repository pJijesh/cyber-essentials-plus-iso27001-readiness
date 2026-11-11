"""Create and read the assessment workbook (a plain CSV file)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .csvio import read_csv, write_csv
from .datafiles import DataSet
from .errors import ReadinessError

NOT_STARTED = "not started"
PARTIAL = "partial"
IMPLEMENTED = "implemented"
NOT_APPLICABLE = "not applicable"
STATUSES = (NOT_STARTED, PARTIAL, IMPLEMENTED, NOT_APPLICABLE)

STATUS_ALIASES = {"n/a": NOT_APPLICABLE, "na": NOT_APPLICABLE}

COLUMNS = ("id", "status", "owner", "evidence_ref", "last_reviewed", "notes")

# A justification shorter than this is treated as missing, so "n/a" or "no" does not count.
MIN_JUSTIFICATION_CHARS = 10

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SCOPES = ("ce", "iso", "both")


@dataclass(frozen=True)
class Row:
    id: str
    status: str
    owner: str
    evidence_ref: str
    last_reviewed: date | None
    notes: str
    line: int


@dataclass
class Workbook:
    rows: dict[str, Row]
    has_ce: bool
    has_iso: bool


def normalise_status(value: str) -> str | None:
    """Map free text to a canonical status, or None if it is not recognised."""
    v = re.sub(r"[\s_\-]+", " ", value.strip().lower())
    if v in STATUSES:
        return v
    return STATUS_ALIASES.get(v)


def init_workbook(
    path: str | Path,
    dataset: DataSet,
    scope: str = "both",
    with_titles: bool = False,
    force: bool = False,
) -> int:
    """Write a blank workbook and return the number of rows written."""
    if scope not in SCOPES:
        raise ReadinessError(f"Unknown scope '{scope}'. Use one of: {', '.join(SCOPES)}")
    p = Path(path)
    if p.exists() and not force:
        raise ReadinessError(f"{p} already exists. Use --force to overwrite it.")
    header = list(COLUMNS)
    entries: list[tuple[str, str]] = []
    if scope in ("ce", "both"):
        entries += [(c.id, c.requirement) for c in dataset.ce_items]
    if scope in ("iso", "both"):
        entries += [(a.id, a.title) for a in dataset.annex]
    if with_titles:
        header.insert(1, "title")
    rows = []
    for item_id, title in entries:
        row = [item_id] + ([title] if with_titles else []) + [NOT_STARTED, "", "", "", ""]
        rows.append(row)
    write_csv(p, header, rows)
    return len(rows)


def read_workbook(path: str | Path, dataset: DataSet, as_of: date) -> Workbook:
    """Read and validate a workbook. Every problem found is reported together."""
    p = Path(path)
    raw = read_csv(p, COLUMNS)
    if not raw:
        raise ReadinessError(f"{p.name} has a header but no rows. Create one with: python -m readiness init")

    problems: list[str] = []
    rows: dict[str, Row] = {}
    known = set(dataset.ce_by_id) | set(dataset.annex_by_id)

    for line, r in raw:
        item_id = r["id"]
        where = f"{p.name} line {line} ({item_id or 'no id'})"
        if not item_id:
            problems.append(f"{where}: id is empty")
            continue
        if item_id not in known:
            problems.append(f"{where}: unknown id. It is not in the CE or Annex A data files")
            continue
        if item_id in rows:
            problems.append(f"{where}: duplicate id (first seen on line {rows[item_id].line})")
            continue
        status = normalise_status(r["status"])
        if status is None:
            problems.append(
                f"{where}: status '{r['status']}' is not valid. Use one of: {', '.join(STATUSES)}"
            )
            continue
        reviewed: date | None = None
        if r["last_reviewed"]:
            if not _DATE_RE.match(r["last_reviewed"]):
                problems.append(f"{where}: last_reviewed '{r['last_reviewed']}' must be YYYY-MM-DD")
                continue
            try:
                reviewed = date.fromisoformat(r["last_reviewed"])
            except ValueError:
                problems.append(f"{where}: last_reviewed '{r['last_reviewed']}' is not a real date")
                continue
            if reviewed > as_of:
                problems.append(
                    f"{where}: last_reviewed {reviewed} is after the as-of date {as_of}"
                )
                continue
        if status == NOT_APPLICABLE and len(r["notes"]) < MIN_JUSTIFICATION_CHARS:
            problems.append(
                f"{where}: 'not applicable' needs a justification in notes "
                f"(at least {MIN_JUSTIFICATION_CHARS} characters)"
            )
            continue
        rows[item_id] = Row(
            item_id, status, r["owner"], r["evidence_ref"], reviewed, r["notes"], line
        )

    present = {r["id"] for _, r in raw if r["id"]}
    has_ce = bool(present & set(dataset.ce_by_id))
    has_iso = bool(present & set(dataset.annex_by_id))
    if has_ce:
        missing = [c.id for c in dataset.ce_items if c.id not in rows]
        missing = [m for m in missing if not _reported(m, problems)]
        if missing:
            problems.append(_missing_message(p.name, "Cyber Essentials", missing))
    if has_iso:
        missing = [a.id for a in dataset.annex if a.id not in rows]
        missing = [m for m in missing if not _reported(m, problems)]
        if missing:
            problems.append(_missing_message(p.name, "ISO Annex A", missing))
    if not has_ce and not has_iso and not problems:
        problems.append(f"{p.name} contains no Cyber Essentials or Annex A ids")

    if problems:
        raise ReadinessError(problems)
    return Workbook(rows, has_ce, has_iso)


def _reported(item_id: str, problems: list[str]) -> bool:
    """True if a row for this id already produced an error, so it is not also 'missing'."""
    return any(f"({item_id})" in prob for prob in problems)


def _missing_message(name: str, label: str, missing: list[str]) -> str:
    shown = ", ".join(missing[:8])
    more = f" and {len(missing) - 8} more" if len(missing) > 8 else ""
    return (
        f"{name} is missing {len(missing)} {label} id(s): {shown}{more}. "
        "Every item must have a row. Use status 'not started' for work not begun."
    )
