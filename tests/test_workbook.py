import csv
from datetime import date

import pytest

from readiness.errors import ReadinessError
from readiness.workbook import init_workbook, normalise_status, read_workbook

AS_OF = date(2026, 11, 11)


def _read(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def test_init_creates_all_rows_with_exact_columns(dataset, tmp_path):
    path = tmp_path / "a.csv"
    n = init_workbook(path, dataset)
    assert n == 138
    rows = _read(path)
    assert list(rows[0]) == ["id", "status", "owner", "evidence_ref", "last_reviewed", "notes"]
    assert rows[0]["id"] == "CE-SCO-01"
    assert rows[45]["id"] == "A.5.1"
    assert {r["status"] for r in rows} == {"not started"}


def test_init_scope_and_titles(dataset, tmp_path):
    ce = tmp_path / "ce.csv"
    assert init_workbook(ce, dataset, scope="ce") == 45
    iso = tmp_path / "iso.csv"
    assert init_workbook(iso, dataset, scope="iso", with_titles=True) == 93
    assert list(_read(iso)[0])[:3] == ["id", "title", "status"]


def test_init_refuses_to_overwrite_without_force(dataset, tmp_path):
    path = tmp_path / "a.csv"
    init_workbook(path, dataset)
    with pytest.raises(ReadinessError, match="already exists"):
        init_workbook(path, dataset)
    assert init_workbook(path, dataset, force=True) == 138


def test_init_rejects_unknown_scope(dataset, tmp_path):
    with pytest.raises(ReadinessError, match="Unknown scope"):
        init_workbook(tmp_path / "a.csv", dataset, scope="nope")


def test_init_output_reads_back_cleanly(dataset, tmp_path):
    path = tmp_path / "a.csv"
    init_workbook(path, dataset, with_titles=True)
    wb = read_workbook(path, dataset, AS_OF)
    assert wb.has_ce and wb.has_iso and len(wb.rows) == 138


@pytest.mark.parametrize(
    "text,expected",
    [("Implemented", "implemented"), ("NOT STARTED", "not started"), ("not_started", "not started"),
     ("not-applicable", "not applicable"), ("n/a", "not applicable"), (" Partial ", "partial"),
     ("done", None), ("", None)],
)
def test_status_normalisation(text, expected):
    assert normalise_status(text) == expected


def test_ce_only_workbook_is_accepted(make_workbook, dataset):
    wb = read_workbook(make_workbook(scope="ce"), dataset, AS_OF)
    assert wb.has_ce and not wb.has_iso


def test_all_problems_are_reported_together(make_workbook, dataset):
    path = make_workbook({
        "CE-FW-01": {"status": "finished"},
        "CE-FW-02": {"last_reviewed": "11/11/2026"},
        "CE-FW-03": {"last_reviewed": "2026-13-45"},
        "CE-FW-04": {"last_reviewed": "2027-01-01"},
        "CE-FW-05": {"status": "not applicable", "notes": "n/a"},
    })
    with pytest.raises(ReadinessError) as exc:
        read_workbook(path, dataset, AS_OF)
    text = "\n".join(exc.value.problems)
    assert "CE-FW-01" in text and "status 'finished' is not valid" in text
    assert "must be YYYY-MM-DD" in text
    assert "not a real date" in text
    assert "after the as-of date" in text
    assert "needs a justification" in text
    assert len(exc.value.problems) == 5
    assert "wb.csv line 10 (CE-FW-01)" in text  # line numbers are included


def test_not_applicable_with_justification_is_accepted(make_workbook, dataset):
    path = make_workbook({"A.8.4": {"status": "not applicable", "notes": "No source code is held."}})
    wb = read_workbook(path, dataset, AS_OF)
    assert wb.rows["A.8.4"].status == "not applicable"


def test_unknown_and_duplicate_ids(make_workbook, dataset):
    path = make_workbook()
    with open(path, "a", newline="", encoding="utf-8") as fh:
        fh.write("A.9.9,not started,,,,\n")
        fh.write("CE-FW-01,partial,,,,\n")
    with pytest.raises(ReadinessError) as exc:
        read_workbook(path, dataset, AS_OF)
    text = "\n".join(exc.value.problems)
    assert "unknown id" in text
    assert "duplicate id" in text


def test_missing_rows_are_reported(make_workbook, dataset, tmp_path):
    path = make_workbook()
    lines = path.read_text(encoding="utf-8").splitlines()
    kept = [l for l in lines if not l.startswith(("CE-FW-01,", "A.8.1,"))]
    path.write_text("\n".join(kept) + "\n", encoding="utf-8")
    with pytest.raises(ReadinessError) as exc:
        read_workbook(path, dataset, AS_OF)
    text = "\n".join(exc.value.problems)
    assert "missing 1 Cyber Essentials id(s): CE-FW-01" in text
    assert "missing 1 ISO Annex A id(s): A.8.1" in text


def test_missing_file_columns_and_empty_file(dataset, tmp_path):
    with pytest.raises(ReadinessError, match="File not found"):
        read_workbook(tmp_path / "nope.csv", dataset, AS_OF)
    bad = tmp_path / "bad.csv"
    bad.write_text("id,status\nCE-FW-01,partial\n", encoding="utf-8")
    with pytest.raises(ReadinessError, match="missing required column"):
        read_workbook(bad, dataset, AS_OF)
    empty = tmp_path / "empty.csv"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(ReadinessError, match="is empty"):
        read_workbook(empty, dataset, AS_OF)
    header_only = tmp_path / "h.csv"
    header_only.write_text("id,status,owner,evidence_ref,last_reviewed,notes\n", encoding="utf-8")
    with pytest.raises(ReadinessError, match="no rows"):
        read_workbook(header_only, dataset, AS_OF)


def test_byte_order_mark_from_spreadsheet_is_tolerated(make_workbook, dataset):
    path = make_workbook()
    path.write_bytes(b"\xef\xbb\xbf" + path.read_bytes())
    assert len(read_workbook(path, dataset, AS_OF).rows) == 138
