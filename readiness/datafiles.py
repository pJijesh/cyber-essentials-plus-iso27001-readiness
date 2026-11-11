"""Load and validate the three reference data files in ``data/``."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .csvio import read_csv
from .errors import ReadinessError

CE_FILE = "ce-requirements.csv"
ANNEX_FILE = "iso27001-annexa.csv"
MAPPING_FILE = "mapping-ce-to-iso.csv"

STRENGTHS = ("strong", "partial", "none")


def default_data_dir() -> Path:
    """The ``data`` folder next to the package, i.e. in the repository root."""
    return Path(__file__).resolve().parent.parent / "data"


@dataclass(frozen=True)
class CeItem:
    id: str
    theme: str
    requirement: str
    applies_to: str
    evidence_examples: str
    common_failure: str


@dataclass(frozen=True)
class AnnexControl:
    id: str
    theme: str
    title: str


@dataclass(frozen=True)
class MappingRow:
    ce_id: str
    annexa_id: str
    strength: str
    note: str


@dataclass
class DataSet:
    ce_items: list[CeItem]
    annex: list[AnnexControl]
    mapping: list[MappingRow]
    ce_by_id: dict[str, CeItem] = field(init=False)
    annex_by_id: dict[str, AnnexControl] = field(init=False)

    def __post_init__(self) -> None:
        self.ce_by_id = {c.id: c for c in self.ce_items}
        self.annex_by_id = {a.id: a for a in self.annex}

    def ce_helping(self, annex_id: str) -> list[tuple[str, str]]:
        """CE items (id, strength) that contribute to an Annex A control, in file order."""
        return [
            (m.ce_id, m.strength)
            for m in self.mapping
            if m.annexa_id == annex_id and m.ce_id
        ]

    def themes(self, scope: str) -> list[str]:
        """Theme names in order of first appearance for ``ce`` or ``iso``."""
        items = self.ce_items if scope == "ce" else self.annex
        seen: list[str] = []
        for item in items:
            if item.theme not in seen:
                seen.append(item.theme)
        return seen


def load_dataset(data_dir: str | Path | None = None) -> DataSet:
    base = Path(data_dir) if data_dir else default_data_dir()
    problems: list[str] = []

    ce_rows = read_csv(
        base / CE_FILE,
        ("id", "theme", "requirement", "applies_to", "evidence_examples", "common_failure"),
    )
    annex_rows = read_csv(base / ANNEX_FILE, ("id", "theme", "short_title"))
    map_rows = read_csv(base / MAPPING_FILE, ("ce_id", "annexa_id", "strength", "note"))

    ce_items: list[CeItem] = []
    seen: set[str] = set()
    for line, r in ce_rows:
        if not r["id"] or not r["requirement"] or not r["theme"]:
            problems.append(f"{CE_FILE} line {line}: id, theme and requirement are required")
            continue
        if r["id"] in seen:
            problems.append(f"{CE_FILE} line {line}: duplicate id {r['id']}")
            continue
        seen.add(r["id"])
        ce_items.append(CeItem(**{k: r[k] for k in (
            "id", "theme", "requirement", "applies_to", "evidence_examples", "common_failure")}))

    annex: list[AnnexControl] = []
    seen_a: set[str] = set()
    for line, r in annex_rows:
        if not r["id"] or not r["theme"] or not r["short_title"]:
            problems.append(f"{ANNEX_FILE} line {line}: id, theme and short_title are required")
            continue
        if r["id"] in seen_a:
            problems.append(f"{ANNEX_FILE} line {line}: duplicate id {r['id']}")
            continue
        seen_a.add(r["id"])
        annex.append(AnnexControl(r["id"], r["theme"], r["short_title"]))

    mapping: list[MappingRow] = []
    for line, r in map_rows:
        if r["strength"] not in STRENGTHS:
            problems.append(
                f"{MAPPING_FILE} line {line}: strength must be one of {', '.join(STRENGTHS)}, "
                f"got '{r['strength']}'"
            )
            continue
        if r["annexa_id"] not in seen_a:
            problems.append(f"{MAPPING_FILE} line {line}: unknown Annex A id '{r['annexa_id']}'")
            continue
        if r["strength"] == "none":
            if r["ce_id"]:
                problems.append(f"{MAPPING_FILE} line {line}: strength none must have an empty ce_id")
                continue
        elif r["ce_id"] not in seen:
            problems.append(f"{MAPPING_FILE} line {line}: unknown CE id '{r['ce_id']}'")
            continue
        mapping.append(MappingRow(r["ce_id"], r["annexa_id"], r["strength"], r["note"]))

    if problems:
        raise ReadinessError(problems)
    return DataSet(ce_items, annex, mapping)
