import csv
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from readiness.cli import main

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"


def _run(argv, capsys):
    code = main(argv)
    cap = capsys.readouterr()
    return code, cap.out, cap.err


def test_end_to_end_init_fill_score(tmp_path, capsys):
    wb = tmp_path / "assessment.csv"
    code, out, _ = _run(["init", "--out", str(wb)], capsys)
    assert code == 0 and "Wrote 138 rows" in out

    # Fill in a handful of rows, as a user would in a spreadsheet.
    rows = list(csv.DictReader(wb.open(newline="", encoding="utf-8")))
    for r in rows:
        if r["id"].startswith("CE-FW"):
            r["status"] = "implemented"
            r["evidence_ref"] = "EV-1"
            r["last_reviewed"] = "2026-10-01"
        if r["id"] == "A.8.4":
            r["status"] = "not applicable"
            r["notes"] = "No source code is held."
        if r["id"] == "A.5.1":
            r["status"] = "partial"
            r["last_reviewed"] = "2024-01-01"
            r["evidence_ref"] = "POL-1"
    with wb.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    out_dir = tmp_path / "out"
    code, out, _ = _run(["score", "--workbook", str(wb), "--out", str(out_dir), "--as-of", "2026-11-11"], capsys)
    assert code == 0
    assert sorted(p.name for p in out_dir.iterdir()) == ["report.json", "report.md", "soa.csv", "soa.md"]

    data = json.loads((out_dir / "report.json").read_text(encoding="utf-8"))
    fw = next(t for t in data["scopes"]["ce"]["themes"] if t["theme"] == "Firewalls")
    assert fw["coverage_percent"] == 100.0
    assert data["scopes"]["ce"]["overall"]["implemented"] == 8
    assert data["scopes"]["iso"]["overall"]["not_applicable"] == 1
    assert [o["id"] for o in data["overdue_reviews"]] == ["A.5.1"]
    assert data["statement_of_applicability"]["excluded"] == 1

    soa = list(csv.DictReader((out_dir / "soa.csv").open(newline="", encoding="utf-8")))
    assert len(soa) == 93
    row = next(r for r in soa if r["control_id"] == "A.8.4")
    assert row["included"] == "No" and row["justification"] == "No source code is held."


def test_score_is_deterministic(tmp_path, capsys):
    wb = EXAMPLES / "assessment.csv"
    for name in ("one", "two"):
        assert _run(["score", "--workbook", str(wb), "--out", str(tmp_path / name), "--as-of", "2026-11-11"], capsys)[0] == 0
    for fname in ("report.md", "report.json", "soa.csv", "soa.md"):
        assert (tmp_path / "one" / fname).read_bytes() == (tmp_path / "two" / fname).read_bytes()


def test_bad_workbook_exits_2_with_readable_message(tmp_path, capsys):
    bad = tmp_path / "bad.csv"
    bad.write_text("id,status,owner,evidence_ref,last_reviewed,notes\nCE-FW-01,done,,,,\n", encoding="utf-8")
    code, out, err = _run(["score", "--workbook", str(bad), "--out", str(tmp_path / "o")], capsys)
    assert code == 2
    assert "Cannot continue:" in err and "status 'done' is not valid" in err
    assert "Traceback" not in err
    assert not (tmp_path / "o").exists()


def test_missing_workbook_exits_2(tmp_path, capsys):
    code, _, err = _run(["score", "--workbook", str(tmp_path / "none.csv")], capsys)
    assert code == 2 and "File not found" in err


def test_invalid_as_of_date_is_rejected_by_argparse(tmp_path, capsys):
    with pytest.raises(SystemExit) as exc:
        main(["score", "--workbook", str(EXAMPLES / "assessment.csv"), "--as-of", "yesterday"])
    assert exc.value.code == 2
    assert "not a valid date" in capsys.readouterr().err


def test_fail_under_exits_3(tmp_path, capsys):
    base = ["score", "--workbook", str(EXAMPLES / "assessment.csv"), "--out", str(tmp_path / "o"), "--as-of", "2026-11-11"]
    assert _run(base + ["--fail-under", "30"], capsys)[0] == 0
    code, _, err = _run(base + ["--fail-under", "50"], capsys)
    assert code == 3 and "ISO Annex A" in err and "Cyber Essentials" not in err


def test_init_refuses_overwrite(tmp_path, capsys):
    wb = tmp_path / "a.csv"
    assert _run(["init", "--out", str(wb)], capsys)[0] == 0
    code, _, err = _run(["init", "--out", str(wb)], capsys)
    assert code == 2 and "--force" in err


def test_sites_end_to_end(tmp_path, capsys):
    out_dir = tmp_path / "s"
    code, out, _ = _run(["sites", "--sites", str(EXAMPLES / "sites.csv"), "--out", str(out_dir)], capsys)
    assert code == 0 and "Tiered 6 sites" in out
    data = json.loads((out_dir / "sites.json").read_text(encoding="utf-8"))
    assert [t["sites"] for t in data["tiers"]] == [1, 3, 2]
    rows = list(csv.DictReader((out_dir / "site-tiers.csv").open(newline="", encoding="utf-8")))
    assert rows[0]["site"] == "Ashgrove Plant" and rows[0]["tier"] == "3"
    sets = list(csv.DictReader((out_dir / "tier-control-sets.csv").open(newline="", encoding="utf-8")))
    assert len(sets) == 45 + 93
    assert {r["minimum_tier"] for r in sets} == {"1", "2", "3"}


def test_sites_bad_input_exits_2(tmp_path, capsys):
    bad = tmp_path / "s.csv"
    bad.write_text("site,country,headcount,data_sensitivity,regulated_data,it_maturity,connectivity\n"
                   "A,X,ten,low,no,high,good\n", encoding="utf-8")
    code, _, err = _run(["sites", "--sites", str(bad), "--out", str(tmp_path / "o")], capsys)
    assert code == 2 and "headcount 'ten'" in err


def test_module_entry_point_runs(tmp_path):
    proc = subprocess.run(
        [sys.executable, "-m", "readiness", "sites", "--sites", str(EXAMPLES / "sites.csv"),
         "--out", str(tmp_path / "o")],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "Tiered 6 sites" in proc.stdout
    help_proc = subprocess.run([sys.executable, "-m", "readiness", "--help"], cwd=ROOT, capture_output=True, text=True)
    assert help_proc.returncode == 0 and "score" in help_proc.stdout


def test_committed_examples_match_a_fresh_run(tmp_path):
    spec = importlib.util.spec_from_file_location("build_examples", ROOT / "scripts" / "build_examples.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.build(tmp_path)
    compared = 0
    for fresh in sorted(tmp_path.rglob("*")):
        if fresh.is_file():
            committed = EXAMPLES / fresh.relative_to(tmp_path)
            assert committed.is_file(), f"{committed} is not committed"
            assert committed.read_bytes() == fresh.read_bytes(), f"{committed} is out of date. Run scripts/build_examples.py"
            compared += 1
    assert compared == 9
