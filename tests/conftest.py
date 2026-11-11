import csv
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from readiness.datafiles import load_dataset  # noqa: E402


@pytest.fixture(scope="session")
def dataset():
    return load_dataset()


@pytest.fixture
def make_workbook(dataset, tmp_path):
    """Write a complete workbook where every item is 'not started' unless overridden.

    ``overrides`` maps an id to a dict of column values to change.
    """

    def _make(overrides=None, name="wb.csv", scope="both", default_status="not started"):
        overrides = overrides or {}
        ids = []
        if scope in ("ce", "both"):
            ids += [c.id for c in dataset.ce_items]
        if scope in ("iso", "both"):
            ids += [a.id for a in dataset.annex]
        path = tmp_path / name
        with path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(["id", "status", "owner", "evidence_ref", "last_reviewed", "notes"])
            for i in ids:
                row = {"id": i, "status": default_status, "owner": "", "evidence_ref": "",
                       "last_reviewed": "", "notes": ""}
                row.update(overrides.get(i, {}))
                w.writerow([row[c] for c in ("id", "status", "owner", "evidence_ref", "last_reviewed", "notes")])
        return path

    return _make


@pytest.fixture
def write_sites(tmp_path):
    def _write(rows, header=None, name="sites.csv"):
        header = header or ["site", "country", "headcount", "data_sensitivity", "regulated_data",
                            "it_maturity", "connectivity", "local_requirements_note"]
        path = tmp_path / name
        with path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(header)
            for r in rows:
                w.writerow(r)
        return path

    return _write
