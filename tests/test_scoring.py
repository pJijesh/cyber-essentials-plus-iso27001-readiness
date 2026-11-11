from datetime import date

from readiness.scoring import CE_PRIORITY_IDS, coverage_percent, score
from readiness.workbook import read_workbook

AS_OF = date(2026, 11, 11)


def _score(make_workbook, dataset, overrides, **kw):
    wb = read_workbook(make_workbook(overrides, **kw.pop("wbargs", {})), dataset, AS_OF)
    return score(dataset, wb, AS_OF, **kw)


def _theme(result, scope, theme):
    return next(t for t in result["scopes"][scope]["themes"] if t["theme"] == theme)


def test_coverage_formula():
    assert coverage_percent(4, 2, 7) == 71.4
    assert coverage_percent(0, 0, 0) is None
    assert coverage_percent(0, 1, 2) == 25.0


def test_all_not_started_is_zero(make_workbook, dataset):
    r = _score(make_workbook, dataset, {})
    assert r["scopes"]["ce"]["overall"]["coverage_percent"] == 0.0
    assert r["scopes"]["iso"]["overall"]["coverage_percent"] == 0.0
    assert len(r["gaps"]) == 138


def test_all_implemented_is_one_hundred(make_workbook, dataset):
    r = _score(make_workbook, dataset, {}, wbargs={"default_status": "implemented"})
    assert r["scopes"]["ce"]["overall"]["coverage_percent"] == 100.0
    assert r["scopes"]["iso"]["overall"]["coverage_percent"] == 100.0
    assert r["gaps"] == []


def test_known_theme_score_with_not_applicable_excluded(make_workbook, dataset):
    # Firewalls has 8 items: 4 implemented, 2 partial, 1 not started, 1 not applicable.
    overrides = {f"CE-FW-0{i}": {"status": "implemented"} for i in (1, 2, 3, 4)}
    overrides.update({f"CE-FW-0{i}": {"status": "partial"} for i in (5, 6)})
    overrides["CE-FW-08"] = {"status": "not applicable", "notes": "No cloud services used at all."}
    r = _score(make_workbook, dataset, overrides)
    t = _theme(r, "ce", "Firewalls")
    assert (t["implemented"], t["partial"], t["not_started"], t["not_applicable"]) == (4, 2, 1, 1)
    assert t["applicable"] == 7
    assert t["coverage_percent"] == 71.4  # (4 + 0.5 * 2) / 7
    overall = r["scopes"]["ce"]["overall"]
    assert overall["applicable"] == 44
    assert overall["coverage_percent"] == round(100 * 5 / 44, 1)


def test_theme_with_only_not_applicable_items_has_no_percentage(make_workbook, dataset):
    overrides = {c.id: {"status": "not applicable", "notes": "Not used in this organisation."}
                 for c in dataset.ce_items if c.theme == "Malware protection"}
    r = _score(make_workbook, dataset, overrides)
    t = _theme(r, "ce", "Malware protection")
    assert t["applicable"] == 0 and t["coverage_percent"] is None


def test_gaps_list_priority_items_first_then_ce_then_status(make_workbook, dataset):
    overrides = {"CE-UPD-04": {"status": "partial"}, "CE-FW-01": {"status": "partial"}}
    for item in dataset.ce_items:
        if item.id not in ("CE-UPD-04", "CE-FW-01", "CE-UAC-04"):
            overrides.setdefault(item.id, {"status": "implemented"})
    r = _score(make_workbook, dataset, overrides)
    ids = [g["id"] for g in r["gaps"][:5]]
    # CE-UAC-04 (not started) and CE-UPD-04 (partial) are priority items and come first,
    # not started before partial; then the remaining CE gap; then ISO items.
    assert ids[:2] == ["CE-UAC-04", "CE-UPD-04"]
    assert ids[2] == "CE-FW-01"
    assert ids[3] == "A.5.1"
    assert r["gaps"][0]["priority"] is True and r["gaps"][2]["priority"] is False


def test_priority_ids_exist_in_data(dataset):
    for item_id in CE_PRIORITY_IDS:
        assert item_id in dataset.ce_by_id


def test_ce_priority_table_reports_status(make_workbook, dataset):
    r = _score(make_workbook, dataset, {"CE-UAC-04": {"status": "implemented"}})
    status = {p["id"]: p["status"] for p in r["ce_priority"]}
    assert status["CE-UAC-04"] == "implemented"
    assert status["CE-UPD-04"] == "not started"


def test_overdue_review_boundaries(make_workbook, dataset):
    ok = {"status": "implemented", "evidence_ref": "E1"}
    r = _score(
        make_workbook,
        dataset,
        {
            "CE-FW-01": {**ok, "last_reviewed": "2025-11-11"},  # exactly 365 days: not overdue
            "CE-FW-02": {**ok, "last_reviewed": "2025-11-10"},  # 366 days: overdue by 1
            "CE-FW-03": {**ok, "last_reviewed": "2025-01-01"},  # 314 days overdue
            "CE-FW-04": {**ok, "last_reviewed": ""},  # no date
        },
    )
    overdue = {o["id"]: o["days_overdue"] for o in r["overdue_reviews"]}
    assert overdue == {"CE-FW-02": 1, "CE-FW-03": 314}
    assert [o["id"] for o in r["overdue_reviews"]] == ["CE-FW-03", "CE-FW-02"]  # most overdue first
    assert [u["id"] for u in r["no_review_date"]] == ["CE-FW-04"]


def test_review_days_is_adjustable(make_workbook, dataset):
    over = {"CE-FW-01": {"status": "implemented", "evidence_ref": "E1", "last_reviewed": "2026-06-01"}}
    assert _score(make_workbook, dataset, over, review_days=365)["overdue_reviews"] == []
    r = _score(make_workbook, dataset, over, review_days=90)
    assert r["overdue_reviews"][0]["days_since_review"] == 163
    assert r["overdue_reviews"][0]["days_overdue"] == 73


def test_missing_evidence_and_not_started_not_flagged(make_workbook, dataset):
    r = _score(make_workbook, dataset, {
        "CE-FW-01": {"status": "implemented", "last_reviewed": "2026-10-01"},
        "CE-FW-02": {"status": "partial", "evidence_ref": "E2", "last_reviewed": "2026-10-01"},
    })
    assert [m["id"] for m in r["missing_evidence"]] == ["CE-FW-01"]
    assert r["overdue_reviews"] == [] and r["no_review_date"] == []


def test_not_applicable_items_are_listed_with_justification(make_workbook, dataset):
    r = _score(make_workbook, dataset, {"A.8.4": {"status": "not applicable", "notes": "No source code is held."}})
    assert r["not_applicable"] == [{
        "scope": "iso", "id": "A.8.4", "title": "Source code access",
        "justification": "No source code is held.", "owner": "",
    }]


def test_scoring_is_independent_of_row_order(make_workbook, dataset, tmp_path):
    path = make_workbook({"CE-FW-01": {"status": "implemented"}, "A.8.8": {"status": "partial"}})
    lines = path.read_text(encoding="utf-8").splitlines()
    shuffled = tmp_path / "shuffled.csv"
    shuffled.write_text("\n".join([lines[0]] + list(reversed(lines[1:]))) + "\n", encoding="utf-8")
    a = score(dataset, read_workbook(path, dataset, AS_OF), AS_OF)
    b = score(dataset, read_workbook(shuffled, dataset, AS_OF), AS_OF)
    assert a == b
