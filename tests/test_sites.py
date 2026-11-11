import copy
import json
from pathlib import Path

import pytest

from readiness.errors import ReadinessError
from readiness.sites import (
    DEFAULT_CONFIG,
    assess_sites,
    load_config,
    read_sites,
    resolve_control_sets,
)

ROOT = Path(__file__).resolve().parent.parent
HEADER = ["site", "country", "headcount", "data_sensitivity", "regulated_data", "it_maturity", "connectivity"]


@pytest.fixture
def cfg(dataset):
    return load_config(None, dataset)


def _assess(cfg, dataset, write_sites, rows):
    return assess_sites(cfg, read_sites(write_sites(rows), cfg), dataset)["sites"]


def test_example_sites_have_the_hand_calculated_scores(cfg, dataset):
    # Maximum weighted points: (2 + 3 + 3 + 2 + 1) * 4 = 44.
    sites = read_sites(ROOT / "examples" / "sites.csv", cfg)
    result = assess_sites(cfg, sites, dataset)
    got = {s["site"]: (s["score"], s["tier"]) for s in result["sites"]}
    assert got == {
        "Northgate Works": (72.7, 3),         # 8 + 12 + 12 + 0 + 0 = 32
        "Ashgrove Plant": (72.7, 3),          # 4 + 6 + 12 + 8 + 2 = 32
        "Rhenmark Plant": (63.6, 2),          # 6 + 6 + 12 + 4 + 0 = 28
        "Calder Design Studio": (40.9, 2),    # 2 + 12 + 0 + 4 + 0 = 18
        "Silvermere Assembly": (36.4, 2),     # 4 + 6 + 0 + 4 + 2 = 16
        "Tidewater Sales Office": (31.8, 1),  # 2 + 0 + 0 + 8 + 4 = 14
    }


def test_sites_are_sorted_by_tier_then_score_then_name(cfg, dataset):
    result = assess_sites(cfg, read_sites(ROOT / "examples" / "sites.csv", cfg), dataset)
    names = [s["site"] for s in result["sites"]]
    assert names == ["Ashgrove Plant", "Northgate Works", "Rhenmark Plant", "Calder Design Studio",
                     "Silvermere Assembly", "Tidewater Sales Office"]


def test_floor_raises_tier_and_is_reported(cfg, dataset, write_sites):
    rows = [
        ["Regulated and sensitive", "X", 5, "high", "yes", "high", "good"],   # 24/44 = 54.5, tier 2 by score
        ["Sensitive only", "X", 5, "high", "no", "high", "good"],             # 12/44 = 27.3, tier 1 by score
        ["Regulated only", "X", 5, "low", "yes", "high", "good"],             # 12/44 = 27.3, tier 1 by score
        ["Quiet", "X", 5, "low", "no", "high", "good"],                        # 0
    ]
    by = {s["site"]: s for s in _assess(cfg, dataset, write_sites, rows)}
    a = by["Regulated and sensitive"]
    assert (a["score"], a["score_tier"], a["tier"]) == (54.5, 2, 3)
    assert a["floors_applied"] == ["regulated and highly sensitive data"]
    b = by["Sensitive only"]
    assert (b["score"], b["score_tier"], b["tier"], b["floors_applied"]) == (27.3, 1, 2, ["high sensitivity data"])
    c = by["Regulated only"]
    assert (c["score_tier"], c["tier"], c["floors_applied"]) == (1, 2, ["regulated data"])
    q = by["Quiet"]
    assert (q["score"], q["tier"], q["floors_applied"]) == (0.0, 1, [])


def test_headcount_band_edges(cfg, dataset, write_sites):
    def pts(n):
        row = [["S", "X", n, "low", "no", "high", "good"]]
        return _assess(cfg, dataset, write_sites, row)[0]["factor_points"]["headcount"]

    assert [pts(n) for n in (0, 10, 11, 50, 51, 150, 151, 300, 301, 5000)] == [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]


def test_threshold_boundary_is_inclusive(dataset, write_sites, tmp_path):
    # Only headcount counts, so scores are exact: 1/4, 2/4 and 3/4 of the maximum points.
    raw = json.loads(DEFAULT_CONFIG.read_text())
    for name, factor in raw["factors"].items():
        factor["weight"] = 1 if name == "headcount" else 0
    raw["thresholds"] = [50, 75]
    p = tmp_path / "cfg.json"
    p.write_text(json.dumps(raw))
    cfg2 = load_config(p, dataset)
    rows = [
        ["Exactly 50", "X", 150, "low", "no", "high", "good"],   # band points 2 of 4
        ["Exactly 75", "X", 300, "low", "no", "high", "good"],   # band points 3 of 4
        ["Below 50", "X", 50, "low", "no", "high", "good"],      # band points 1 of 4
    ]
    got = {s["site"]: (s["score"], s["tier"]) for s in _assess(cfg2, dataset, write_sites, rows)}
    assert got == {"Exactly 50": (50.0, 2), "Exactly 75": (75.0, 3), "Below 50": (25.0, 1)}


def test_changing_a_weight_changes_the_result(dataset, write_sites, tmp_path):
    raw = json.loads(DEFAULT_CONFIG.read_text())
    raw["factors"]["data_sensitivity"]["weight"] = 0
    p = tmp_path / "cfg.json"
    p.write_text(json.dumps(raw))
    cfg2 = load_config(p, dataset)
    rows = [["Calder", "X", 28, "high", "no", "medium", "good"]]
    # Remaining: 2*1 + 0 + 0 + 2*2 + 0 = 6 of (2 + 3 + 2 + 1) * 4 = 32, which is 18.75, rounded 18.8.
    site = _assess(cfg2, dataset, write_sites, rows)[0]
    assert site["score"] == 18.8
    assert site["score_tier"] == 1
    assert site["tier"] == 2  # the sensitivity floor still applies


def test_control_sets_are_cumulative_with_known_counts(cfg, dataset):
    minimum, per_tier = resolve_control_sets(cfg, dataset)
    count = lambda tier, d: sum(1 for i in per_tier[tier] if i in d)
    assert (count(1, dataset.ce_by_id), count(1, dataset.annex_by_id)) == (39, 0)
    assert (count(2, dataset.ce_by_id), count(2, dataset.annex_by_id)) == (45, 25)
    assert (count(3, dataset.ce_by_id), count(3, dataset.annex_by_id)) == (45, 93)
    assert set(per_tier[1]) <= set(per_tier[2]) <= set(per_tier[3])
    assert minimum["CE-FW-01"] == 1 and minimum["CE-SCO-01"] == 2 and minimum["A.5.1"] == 2
    assert minimum["A.8.34"] == 3


def test_every_ce_item_is_assigned_a_tier(cfg, dataset):
    minimum, _ = resolve_control_sets(cfg, dataset)
    assert all(c.id in minimum for c in dataset.ce_items)


def test_local_requirements_note_is_passed_through_unchanged(cfg, dataset, write_sites):
    rows = [["Site A", "X", 5, "low", "no", "high", "good", "Ask local counsel | about this"]]
    site = _assess(cfg, dataset, write_sites, rows)[0]
    assert site["local_requirements_note"] == "Ask local counsel | about this"


def test_site_input_errors_are_all_reported(cfg, write_sites):
    path = write_sites([
        ["A", "X", "many", "low", "no", "high", "good"],
        ["B", "X", 5, "severe", "no", "high", "good"],
        ["B", "X", 5, "low", "no", "high", "good"],
        ["", "X", 5, "low", "no", "high", "good"],
        ["C", "", 5, "low", "maybe", "high", "good"],
        ["D", "X", -4, "low", "no", "high", "good"],
    ])
    with pytest.raises(ReadinessError) as exc:
        read_sites(path, cfg)
    text = "\n".join(exc.value.problems)
    assert "headcount 'many'" in text
    assert "data_sensitivity 'severe'" in text and "Use one of: low, medium, high" in text
    assert "duplicate site name" in text
    assert "site name is empty" in text
    assert "country is empty" in text
    assert "regulated_data 'maybe'" in text
    assert "headcount '-4'" in text


def test_site_file_problems(cfg, tmp_path, write_sites):
    with pytest.raises(ReadinessError, match="File not found"):
        read_sites(tmp_path / "none.csv", cfg)
    with pytest.raises(ReadinessError, match="missing required column"):
        read_sites(write_sites([["a", "b"]], header=["site", "country"]), cfg)
    with pytest.raises(ReadinessError, match="no sites"):
        read_sites(write_sites([]), cfg)


def _bad_config(tmp_path, dataset, mutate):
    raw = json.loads(DEFAULT_CONFIG.read_text())
    mutate(raw)
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(raw))
    with pytest.raises(ReadinessError) as exc:
        load_config(p, dataset)
    return "\n".join(exc.value.problems)


def test_config_validation_messages(tmp_path, dataset):
    assert "unknown factor 'colour'" in _bad_config(
        tmp_path, dataset, lambda r: r["factors"].update({"colour": {"weight": 1, "points": {"a": 1}}}))
    assert "needs a weight" in _bad_config(
        tmp_path, dataset, lambda r: r["factors"]["connectivity"].update({"weight": -1}))
    assert "'thresholds' must be an increasing list" in _bad_config(
        tmp_path, dataset, lambda r: r.update({"thresholds": [65, 35]}))
    assert "3 thresholds need 4 tiers, found 3" in _bad_config(
        tmp_path, dataset, lambda r: r.update({"thresholds": [20, 40, 60]}))
    assert "unknown control id 'A.99.1'" in _bad_config(
        tmp_path, dataset, lambda r: r["tiers"]["2"]["add_ids"].append("A.99.1"))
    assert "unknown Cyber Essentials theme 'Wifi'" in _bad_config(
        tmp_path, dataset, lambda r: r["tiers"]["1"]["add_themes"].append("Wifi"))
    assert "not assigned to any tier" in _bad_config(
        tmp_path, dataset, lambda r: r["tiers"]["2"].update({"add_themes": []}))
    assert "last band" in _bad_config(
        tmp_path, dataset, lambda r: r["factors"]["headcount"]["bands"][-1].update({"max": 999}))
    assert "unknown value(s) for 'regulated_data'" in _bad_config(
        tmp_path, dataset, lambda r: r["floors"][0]["when"].update({"regulated_data": ["perhaps"]}))
    assert "at least one factor needs a weight above 0" in _bad_config(
        tmp_path, dataset, lambda r: [f.update({"weight": 0}) for f in r["factors"].values()])


def test_config_file_problems(tmp_path, dataset):
    with pytest.raises(ReadinessError, match="Tiering config not found"):
        load_config(tmp_path / "missing.json", dataset)
    broken = tmp_path / "broken.json"
    broken.write_text("{not json")
    with pytest.raises(ReadinessError, match="Cannot read tiering config"):
        load_config(broken, dataset)
