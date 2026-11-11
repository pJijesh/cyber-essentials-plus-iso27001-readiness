import re
from collections import Counter
from pathlib import Path

from readiness.datafiles import STRENGTHS

DATA = Path(__file__).resolve().parent.parent / "data"

TECHNICAL_THEMES = {
    "Firewalls",
    "Secure configuration",
    "Security update management",
    "User access control",
    "Malware protection",
}


def test_ce_items_cover_the_five_technical_themes_plus_scope(dataset):
    themes = {c.theme for c in dataset.ce_items}
    assert themes == TECHNICAL_THEMES | {"Scope and inventory"}
    assert len(dataset.ce_items) == 45
    assert len({c.id for c in dataset.ce_items}) == 45


def test_every_ce_item_has_all_text_fields(dataset):
    for c in dataset.ce_items:
        assert c.requirement and c.applies_to and c.evidence_examples and c.common_failure, c.id
        assert re.fullmatch(r"CE-[A-Z]{2,3}-\d{2}", c.id), c.id


def test_annex_a_has_93_controls_in_four_themes(dataset):
    assert len(dataset.annex) == 93
    counts = Counter(a.theme for a in dataset.annex)
    assert counts == {"Organisational": 37, "People": 8, "Physical": 14, "Technological": 34}


def test_annex_ids_follow_the_standard_numbering(dataset):
    expected = (
        [f"A.5.{i}" for i in range(1, 38)]
        + [f"A.6.{i}" for i in range(1, 9)]
        + [f"A.7.{i}" for i in range(1, 15)]
        + [f"A.8.{i}" for i in range(1, 35)]
    )
    assert [a.id for a in dataset.annex] == expected


def test_mapping_references_are_valid_and_complete(dataset):
    assert {m.strength for m in dataset.mapping} <= set(STRENGTHS)
    mapped_ce = {m.ce_id for m in dataset.mapping if m.ce_id}
    assert mapped_ce == {c.id for c in dataset.ce_items}, "every CE item maps to at least one control"
    covered = {m.annexa_id for m in dataset.mapping}
    assert covered == {a.id for a in dataset.annex}, "every Annex A control appears in the mapping"
    for m in dataset.mapping:
        assert m.note, f"{m.ce_id or 'none'} -> {m.annexa_id} needs a note"


def test_none_rows_are_only_for_controls_with_no_ce_item(dataset):
    helped = {m.annexa_id for m in dataset.mapping if m.ce_id}
    none_rows = [m for m in dataset.mapping if m.strength == "none"]
    assert none_rows
    for m in none_rows:
        assert m.ce_id == ""
        assert m.annexa_id not in helped
    assert len(none_rows) + len(helped) == 93


def test_known_mapping_counts(dataset):
    helped = {m.annexa_id for m in dataset.mapping if m.ce_id}
    assert len(helped) == 30
    # No Annex A control is claimed to be fully covered by CE: only strong or partial exist.
    assert all(m.strength in ("strong", "partial") for m in dataset.mapping if m.ce_id)


def test_data_files_contain_no_em_or_en_dashes():
    bad = (chr(0x2014), chr(0x2013))
    for path in DATA.glob("*.csv"):
        text = path.read_text(encoding="utf-8")
        assert not any(ch in text for ch in bad), path.name
