"""Proportionate site tiering.

Each site gets a risk score from weighted factors, a tier from score thresholds, and a
minimum control set for that tier. Everything that can reasonably be a matter of
judgement (factors, weights, thresholds, floors, control sets) lives in a JSON config
file so it can be adjusted and reviewed. The model is generic. It does not interpret
any country's law: the only legal input is a free text column that the user fills in
and that is passed through unchanged.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .csvio import read_csv
from .datafiles import DataSet
from .errors import ReadinessError

SITE_COLUMNS = (
    "site",
    "country",
    "headcount",
    "data_sensitivity",
    "regulated_data",
    "it_maturity",
    "connectivity",
)
OPTIONAL_COLUMNS = ("local_requirements_note",)
FACTORS = SITE_COLUMNS[2:]
BAND_FACTORS = ("headcount",)

DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "config" / "site-tiering.json"


@dataclass
class TierDef:
    number: int
    name: str
    description: str
    assurance: str
    review_cycle: str
    add_themes: list[str]
    add_ids: list[str]
    add_all_iso: bool


@dataclass
class Config:
    disclaimer: str
    factors: dict[str, dict]
    thresholds: list[float]
    floors: list[dict]
    tiers: dict[int, TierDef]


def _max_points(factor: dict) -> float:
    if "bands" in factor:
        return max(b["points"] for b in factor["bands"])
    return max(factor["points"].values())


def load_config(path: str | Path | None, dataset: DataSet) -> Config:
    p = Path(path) if path else DEFAULT_CONFIG
    if not p.is_file():
        raise ReadinessError(f"Tiering config not found: {p}")
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ReadinessError(f"Cannot read tiering config {p.name}: {exc}") from exc

    problems: list[str] = []
    name = p.name
    if not isinstance(raw, dict):
        raise ReadinessError(f"{name}: top level must be a JSON object")

    factors = raw.get("factors")
    if not isinstance(factors, dict) or not factors:
        problems.append(f"{name}: 'factors' must be an object with at least one factor")
        factors = {}
    for fname, f in factors.items():
        if fname not in FACTORS:
            problems.append(f"{name}: unknown factor '{fname}'. Allowed: {', '.join(FACTORS)}")
            continue
        if not isinstance(f, dict):
            problems.append(f"{name}: factor '{fname}' must be an object")
            continue
        w = f.get("weight")
        if not isinstance(w, (int, float)) or isinstance(w, bool) or w < 0:
            problems.append(f"{name}: factor '{fname}' needs a weight of 0 or more")
        if fname in BAND_FACTORS:
            bands = f.get("bands")
            if not isinstance(bands, list) or not bands:
                problems.append(f"{name}: factor '{fname}' needs a non-empty 'bands' list")
                continue
            last_max = None
            for i, b in enumerate(bands):
                is_last = i == len(bands) - 1
                if not isinstance(b, dict) or "points" not in b or "max" not in b:
                    problems.append(f"{name}: each band in '{fname}' needs 'max' and 'points'")
                    break
                if is_last and b["max"] is not None:
                    problems.append(f"{name}: the last band in '{fname}' must have max null")
                if not is_last:
                    if not isinstance(b["max"], (int, float)):
                        problems.append(f"{name}: band max in '{fname}' must be a number")
                        break
                    if last_max is not None and b["max"] <= last_max:
                        problems.append(f"{name}: band limits in '{fname}' must increase")
                        break
                    last_max = b["max"]
        else:
            pts = f.get("points")
            if not isinstance(pts, dict) or not pts:
                problems.append(f"{name}: factor '{fname}' needs a non-empty 'points' object")
            elif not all(isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 0 for v in pts.values()):
                problems.append(f"{name}: points in '{fname}' must be numbers of 0 or more")

    thresholds = raw.get("thresholds")
    if (
        not isinstance(thresholds, list)
        or not thresholds
        or not all(isinstance(t, (int, float)) and not isinstance(t, bool) for t in thresholds)
        or sorted(thresholds) != thresholds
        or len(set(thresholds)) != len(thresholds)
        or any(t <= 0 or t >= 100 for t in thresholds)
    ):
        problems.append(f"{name}: 'thresholds' must be an increasing list of numbers between 0 and 100")
        thresholds = []

    tiers_raw = raw.get("tiers")
    tiers: dict[int, TierDef] = {}
    if not isinstance(tiers_raw, dict) or not tiers_raw:
        problems.append(f"{name}: 'tiers' must be an object keyed '1', '2', ...")
    else:
        keys = sorted(tiers_raw)
        if keys != [str(i) for i in range(1, len(keys) + 1)]:
            problems.append(f"{name}: tier keys must be consecutive numbers starting at '1'")
        if thresholds and len(keys) != len(thresholds) + 1:
            problems.append(
                f"{name}: {len(thresholds)} thresholds need {len(thresholds) + 1} tiers, found {len(keys)}"
            )
        all_ids = set(dataset.ce_by_id) | set(dataset.annex_by_id)
        themes = set(dataset.themes("ce"))
        for key in keys:
            t = tiers_raw[key]
            if not key.isdigit() or not isinstance(t, dict):
                continue
            for req in ("name", "description", "assurance", "review_cycle"):
                if not isinstance(t.get(req), str) or not t[req]:
                    problems.append(f"{name}: tier {key} needs a text value for '{req}'")
            add_ids = t.get("add_ids", [])
            add_themes = t.get("add_themes", [])
            for i in add_ids:
                if i not in all_ids:
                    problems.append(f"{name}: tier {key} lists unknown control id '{i}'")
            for th in add_themes:
                if th not in themes:
                    problems.append(
                        f"{name}: tier {key} lists unknown Cyber Essentials theme '{th}'. "
                        f"Known themes: {', '.join(sorted(themes))}"
                    )
            tiers[int(key)] = TierDef(
                int(key), str(t.get("name", "")), str(t.get("description", "")),
                str(t.get("assurance", "")), str(t.get("review_cycle", "")),
                list(add_themes), list(add_ids), bool(t.get("add_all_iso", False)),
            )

    floors = raw.get("floors", [])
    if not isinstance(floors, list):
        problems.append(f"{name}: 'floors' must be a list")
        floors = []
    for i, fl in enumerate(floors, start=1):
        if not isinstance(fl, dict) or not isinstance(fl.get("when"), dict) or not fl["when"]:
            problems.append(f"{name}: floor {i} needs a non-empty 'when' object")
            continue
        for fname, values in fl["when"].items():
            if fname in BAND_FACTORS or fname not in FACTORS:
                problems.append(f"{name}: floor {i} cannot test '{fname}'. Use a category factor")
            elif fname in factors and "points" in factors[fname]:
                bad = [v for v in values if str(v).lower() not in factors[fname]["points"]]
                if bad:
                    problems.append(f"{name}: floor {i} uses unknown value(s) for '{fname}': {', '.join(map(str, bad))}")
        mt = fl.get("min_tier")
        if not isinstance(mt, int) or mt < 1 or (tiers and mt > len(tiers)):
            problems.append(f"{name}: floor {i} needs 'min_tier' between 1 and {len(tiers) or 'the number of tiers'}")
        if not isinstance(fl.get("name"), str) or not fl.get("name"):
            problems.append(f"{name}: floor {i} needs a 'name'")

    if factors and all(
        isinstance(f, dict) and isinstance(f.get("weight"), (int, float)) and f["weight"] == 0
        for f in factors.values()
    ):
        problems.append(f"{name}: at least one factor needs a weight above 0")

    if problems:
        raise ReadinessError(problems)

    cfg = Config(str(raw.get("disclaimer", "")), factors, [float(t) for t in thresholds], floors, tiers)
    minimum, _ = resolve_control_sets(cfg, dataset)
    unassigned = [c.id for c in dataset.ce_items if c.id not in minimum]
    if unassigned:
        raise ReadinessError(
            f"{name}: {len(unassigned)} Cyber Essentials item(s) are not assigned to any tier "
            f"(first: {', '.join(unassigned[:5])}). Add them with add_ids or add_themes."
        )
    return cfg


def resolve_control_sets(cfg: Config, dataset: DataSet) -> tuple[dict[str, int], dict[int, list[str]]]:
    """Return (minimum tier per control id, cumulative control ids per tier in standard order)."""
    minimum: dict[str, int] = {}
    for number in sorted(cfg.tiers):
        t = cfg.tiers[number]
        added: set[str] = set(t.add_ids)
        added |= {c.id for c in dataset.ce_items if c.theme in t.add_themes}
        if t.add_all_iso:
            added |= set(dataset.annex_by_id)
        for item_id in added:
            minimum.setdefault(item_id, number)
    order = [c.id for c in dataset.ce_items] + [a.id for a in dataset.annex]
    per_tier = {
        number: [i for i in order if i in minimum and minimum[i] <= number] for number in cfg.tiers
    }
    return minimum, per_tier


def read_sites(path: str | Path, cfg: Config) -> list[dict]:
    p = Path(path)
    raw = read_csv(p, SITE_COLUMNS, OPTIONAL_COLUMNS)
    if not raw:
        raise ReadinessError(f"{p.name} has a header but no sites")
    problems: list[str] = []
    sites: list[dict] = []
    seen: dict[str, int] = {}
    for line, r in raw:
        where = f"{p.name} line {line} ({r['site'] or 'no site name'})"
        row_ok = True
        if not r["site"]:
            problems.append(f"{where}: site name is empty")
            continue
        key = r["site"].lower()
        if key in seen:
            problems.append(f"{where}: duplicate site name (first seen on line {seen[key]})")
            continue
        seen[key] = line
        if not r["country"]:
            problems.append(f"{where}: country is empty")
            row_ok = False
        try:
            headcount = int(r["headcount"])
            if headcount < 0:
                raise ValueError
        except ValueError:
            problems.append(f"{where}: headcount '{r['headcount']}' must be a whole number of 0 or more")
            headcount = 0
            row_ok = False
        values: dict[str, str] = {}
        for fname in FACTORS[1:]:
            v = r[fname].lower()
            allowed = list(cfg.factors[fname]["points"]) if fname in cfg.factors else []
            if fname in cfg.factors and v not in allowed:
                problems.append(
                    f"{where}: {fname} '{r[fname]}' is not valid. Use one of: {', '.join(allowed)}"
                )
                row_ok = False
            values[fname] = v
        if row_ok:
            sites.append(
                {
                    "site": r["site"],
                    "country": r["country"],
                    "headcount": headcount,
                    **values,
                    "local_requirements_note": r.get("local_requirements_note", ""),
                }
            )
    if problems:
        raise ReadinessError(problems)
    return sites


def _points(cfg: Config, factor: str, site: dict) -> float:
    f = cfg.factors[factor]
    if factor in BAND_FACTORS:
        for band in f["bands"]:
            if band["max"] is None or site[factor] <= band["max"]:
                return band["points"]
    return f["points"][site[factor]]


def assess_site(cfg: Config, site: dict, dataset: DataSet, per_tier: dict[int, list[str]]) -> dict:
    total_weight_points = 0.0
    max_total = 0.0
    contributions: dict[str, float] = {}
    factor_points: dict[str, float] = {}
    for fname, f in cfg.factors.items():
        pts = _points(cfg, fname, site)
        factor_points[fname] = pts
        contributions[fname] = f["weight"] * pts
        total_weight_points += f["weight"] * pts
        max_total += f["weight"] * _max_points(f)
    score = round(100.0 * total_weight_points / max_total, 1)
    exact = 100.0 * total_weight_points / max_total
    score_tier = 1 + sum(1 for t in cfg.thresholds if exact >= t)

    tier = score_tier
    applied = []
    for fl in cfg.floors:
        match = all(str(site.get(fname, "")).lower() in [str(v).lower() for v in values]
                    for fname, values in fl["when"].items())
        if match and fl["min_tier"] > score_tier:
            applied.append(fl["name"])
        if match:
            tier = max(tier, fl["min_tier"])

    drivers = sorted(
        ((n, c) for n, c in contributions.items() if c > 0),
        key=lambda x: (-x[1], x[0]),
    )[:3]
    ids = per_tier[tier]
    return {
        "site": site["site"],
        "country": site["country"],
        "headcount": site["headcount"],
        "score": score,
        "score_tier": score_tier,
        "floors_applied": applied,
        "tier": tier,
        "tier_name": cfg.tiers[tier].name,
        "drivers": [f"{n} ({c:g})" for n, c in drivers],
        "factor_points": factor_points,
        "ce_items_required": sum(1 for i in ids if i in dataset.ce_by_id),
        "iso_controls_required": sum(1 for i in ids if i in dataset.annex_by_id),
        "local_requirements_note": site["local_requirements_note"],
    }


def assess_sites(cfg: Config, sites: list[dict], dataset: DataSet) -> dict:
    minimum, per_tier = resolve_control_sets(cfg, dataset)
    results = [assess_site(cfg, s, dataset, per_tier) for s in sites]
    results.sort(key=lambda r: (-r["tier"], -r["score"], r["site"].lower()))
    tiers = []
    for number in sorted(cfg.tiers):
        t = cfg.tiers[number]
        ids = per_tier[number]
        tiers.append(
            {
                "tier": number,
                "name": t.name,
                "description": t.description,
                "assurance": t.assurance,
                "review_cycle": t.review_cycle,
                "ce_items": sum(1 for i in ids if i in dataset.ce_by_id),
                "iso_controls": sum(1 for i in ids if i in dataset.annex_by_id),
                "sites": sum(1 for r in results if r["tier"] == number),
            }
        )
    return {
        "disclaimer": cfg.disclaimer,
        "thresholds": cfg.thresholds,
        "weights": {n: f["weight"] for n, f in cfg.factors.items()},
        "tiers": tiers,
        "sites": results,
        "minimum_tier_by_control": minimum,
    }


def control_set_rows(result: dict, dataset: DataSet) -> list[list[object]]:
    names = {t["tier"]: t["name"] for t in result["tiers"]}
    minimum = result["minimum_tier_by_control"]
    rows = []
    for c in dataset.ce_items:
        if c.id in minimum:
            rows.append([c.id, "Cyber Essentials", c.requirement, minimum[c.id], names[minimum[c.id]]])
    for a in dataset.annex:
        if a.id in minimum:
            rows.append([a.id, "ISO Annex A", a.title, minimum[a.id], names[minimum[a.id]]])
    return rows


def site_rows(result: dict) -> list[list[object]]:
    return [
        [
            s["site"], s["country"], s["headcount"], f"{s['score']:.1f}", s["score_tier"],
            "; ".join(s["floors_applied"]), s["tier"], s["tier_name"], "; ".join(s["drivers"]),
            s["ce_items_required"], s["iso_controls_required"], s["local_requirements_note"],
        ]
        for s in result["sites"]
    ]


SITE_ROW_HEADER = (
    "site", "country", "headcount", "score", "score_tier", "floors_applied", "tier", "tier_name",
    "drivers", "ce_items_required", "iso_controls_required", "local_requirements_note",
)


def render_sites_markdown(result: dict, sites_name: str) -> str:
    def cell(t: object) -> str:
        return str(t).replace("|", "/").replace("\n", " ").strip()

    lines = [
        "# Site tiering report",
        "",
        f"Input: {sites_name}.",
        "",
        "> " + result["disclaimer"],
        "",
        "Tiers set how much local control and assurance a site needs. They do not reduce Cyber "
        "Essentials requirements for any site inside the certified scope: every in-scope device and "
        "service must meet the scheme requirements, whatever its tier.",
        "",
        "## Tiers",
        "",
        "| Tier | Name | Sites | CE items | Annex A controls | Review cycle | Assurance |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for t in result["tiers"]:
        lines.append(f"| {t['tier']} | {cell(t['name'])} | {t['sites']} | {t['ce_items']} | "
                     f"{t['iso_controls']} | {cell(t['review_cycle'])} | {cell(t['assurance'])} |")
    lines += ["", "Tier descriptions:", ""]
    for t in result["tiers"]:
        lines.append(f"- Tier {t['tier']} ({t['name']}): {t['description']}")
    lines += [
        "",
        "## Sites",
        "",
        "Score is the weighted share of the maximum risk points, from 0 to 100. "
        f"Tier thresholds: {', '.join(f'{x:g}' for x in result['thresholds'])}.",
        "",
        "| Site | Country | Headcount | Score | Tier by score | Floor applied | Final tier | Main drivers |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for s in result["sites"]:
        lines.append(
            f"| {cell(s['site'])} | {cell(s['country'])} | {s['headcount']} | {s['score']:.1f} | "
            f"{s['score_tier']} | {cell('; '.join(s['floors_applied']) or 'none')} | "
            f"{s['tier']} ({cell(s['tier_name'])}) | {cell('; '.join(s['drivers']) or 'none')} |"
        )
    lines += ["", "## Weights", ""]
    lines += ["| Factor | Weight |", "| --- | --- |"]
    for name, w in result["weights"].items():
        lines.append(f"| {name} | {w:g} |")
    lines += ["", "## Local requirements notes (supplied by you)", "",
              "This column is passed through from the input. The tool does not read, interpret or "
              "validate it. Complete it with local advice where an obligation may apply.", ""]
    lines += ["| Site | Country | Note |", "| --- | --- | --- |"]
    for s in result["sites"]:
        lines.append(f"| {cell(s['site'])} | {cell(s['country'])} | {cell(s['local_requirements_note']) or 'not completed'} |")
    lines += ["", "The full minimum control set for each tier is in tier-control-sets.csv.", ""]
    return "\n".join(lines)


def to_json(result: dict) -> str:
    return json.dumps(result, indent=2, ensure_ascii=False) + "\n"
