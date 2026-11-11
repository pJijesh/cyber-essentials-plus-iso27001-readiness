from datetime import date

from readiness.soa import PLACEHOLDER, build_soa, soa_markdown, summarise_soa
from readiness.workbook import read_workbook

AS_OF = date(2026, 11, 11)


def _soa(make_workbook, dataset, overrides):
    wb = read_workbook(make_workbook(overrides), dataset, AS_OF)
    return build_soa(dataset, wb)


def test_soa_has_one_entry_per_control_in_order(make_workbook, dataset):
    entries = _soa(make_workbook, dataset, {})
    assert [e["control_id"] for e in entries] == [a.id for a in dataset.annex]
    assert len(entries) == 93


def test_not_applicable_is_excluded_with_its_justification(make_workbook, dataset):
    entries = _soa(make_workbook, dataset, {"A.8.4": {"status": "not applicable", "notes": "No source code is held."}})
    e = next(x for x in entries if x["control_id"] == "A.8.4")
    assert e["included"] == "No"
    assert e["justification"] == "No source code is held."
    assert e["implementation_status"] == "not applicable"


def test_included_control_without_justification_gets_placeholder(make_workbook, dataset):
    entries = _soa(make_workbook, dataset, {"A.5.1": {"status": "partial", "notes": "Policy drafted."}})
    by = {e["control_id"]: e for e in entries}
    assert by["A.5.1"]["justification"] == "Policy drafted."
    assert by["A.5.2"]["justification"] == PLACEHOLDER
    s = summarise_soa(entries)
    assert s == {"controls": 93, "included": 93, "excluded": 0, "included_without_justification": 92}


def test_ce_items_that_help_are_listed_with_their_state(make_workbook, dataset):
    entries = _soa(make_workbook, dataset, {"CE-MAL-01": {"status": "implemented"}})
    e = next(x for x in entries if x["control_id"] == "A.8.7")
    assert "CE-MAL-01 (strong, implemented)" in e["ce_items_that_help"]
    assert "CE-MAL-02 (strong, not started)" in e["ce_items_that_help"]
    assert next(x for x in entries if x["control_id"] == "A.5.1")["ce_items_that_help"] == ""


def test_markdown_contains_every_control_and_a_warning(make_workbook, dataset):
    entries = _soa(make_workbook, dataset, {})
    md = soa_markdown(entries, "2026-11-11")
    assert md.count("| A.") == 93
    assert "not a completed Statement of Applicability" in md
    assert "## Technological" in md
