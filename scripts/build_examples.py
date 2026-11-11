"""Regenerate everything under examples/ from the repository's own code.

Run from the repository root:  python scripts/build_examples.py

The example is a fictional manufacturing group. Statuses are generated with a fixed seed
and then adjusted by a short list of explicit, story-driven overrides, so the same
inputs always give byte-identical files. A test compares the committed files with a
fresh run.
"""

from __future__ import annotations

import random
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from readiness.cli import main  # noqa: E402
from readiness.csvio import write_csv  # noqa: E402
from readiness.datafiles import load_dataset  # noqa: E402

EXAMPLES = ROOT / "examples"
AS_OF = date(2026, 11, 11)
SEED = 2026

CE_PROBS = {  # implemented, partial (the rest is not started)
    "Scope and inventory": (0.55, 0.30),
    "Firewalls": (0.75, 0.20),
    "Secure configuration": (0.70, 0.25),
    "Security update management": (0.50, 0.35),
    "User access control": (0.60, 0.30),
    "Malware protection": (0.85, 0.15),
}
ISO_UNMAPPED_PROBS = {
    "Organisational": (0.15, 0.30),
    "People": (0.30, 0.30),
    "Physical": (0.50, 0.30),
    "Technological": (0.30, 0.30),
}
CE_OWNERS = {
    "Scope and inventory": "IT Manager",
    "Firewalls": "Network Engineer",
    "Secure configuration": "IT Manager",
    "Security update management": "Endpoint Engineer",
    "User access control": "IT Manager",
    "Malware protection": "Endpoint Engineer",
}
ISO_OWNERS = {
    "Organisational": "Security Lead",
    "People": "HR Manager",
    "Physical": "Facilities Manager",
    "Technological": "IT Manager",
}

CE_OVERRIDES = {
    "CE-UAC-04": ("partial", "MFA enforced on the email and collaboration suite and the ERP portal. Two supplier portals and one workflow app still use passwords only. Plan to enforce or retire by end of January."),
    "CE-UPD-02": ("not started", "Two legacy shop-floor PCs run an operating system that is out of support. Isolation design agreed but not yet built."),
    "CE-UPD-04": ("partial", "Operating systems meet the 14 day target through update rings. Firmware on branch routers is not yet tracked."),
    "CE-UPD-05": ("partial", "Browsers and office applications are covered. Browser extensions and the CAD plug-ins are not."),
    "CE-UPD-01": ("partial", "All supported except the two legacy shop-floor PCs (see CE-UPD-02)."),
    "CE-SCO-04": ("partial", "Register covers the main cloud tenant. Plant level and supplier-hosted services still to be added."),
    "CE-UPD-07": ("partial", "Dashboard covers managed laptops only. Servers and plant PCs are reported by hand."),
    "CE-SCO-07": ("not started", "Mexico plant network shares a wireless segment with a contractor. Segregation not yet in place, so the site is not ready to be in scope."),
    "CE-SCO-05": ("implemented", "Personal devices blocked from company data unless registered."),
    "CE-MAL-03": ("not applicable", "Anti-malware software is used on every in-scope device, so allow listing is not relied on."),
    "CE-FW-08": ("partial", "Storage account network rules reviewed for the main tenant only."),
}
ISO_OVERRIDES = {
    "A.5.1": ("partial", "Policy set drafted and awaiting board approval."),
    "A.5.2": ("partial", "Security lead named. Site level roles not yet defined."),
    "A.5.7": ("not started", "No threat intelligence source subscribed yet."),
    "A.5.24": ("not started", "Incident plan to be written after the risk assessment."),
    "A.5.30": ("not started", "Continuity plan covers the main plant only."),
    "A.8.13": ("partial", "Backups run for the main plant systems. Restore tests not yet recorded."),
    "A.8.15": ("partial", "Central logging for identity and email only."),
    "A.8.4": ("not applicable", "The group holds no bespoke source code. It buys packaged software only."),
    "A.8.25": ("not applicable", "No software is developed in house or by suppliers for the group."),
    "A.8.28": ("not applicable", "No software is developed in house or by suppliers for the group."),
    "A.8.29": ("not applicable", "No software is developed in house or by suppliers for the group."),
    "A.8.30": ("not applicable", "No software development is outsourced."),
    "A.8.31": ("not applicable", "No development environments exist. Packaged software is configured in production under change control."),
    "A.7.4": ("partial", "CCTV at the main plant and design studio. Other sites rely on alarms only."),
}


def pick(rng: random.Random, probs: tuple[float, float]) -> str:
    r = rng.random()
    if r < probs[0]:
        return "implemented"
    if r < probs[0] + probs[1]:
        return "partial"
    return "not started"


def review_date(rng: random.Random) -> str:
    start = date(2025, 8, 15)
    span = (date(2026, 11, 3) - start).days
    return (start + timedelta(days=int(rng.random() * span))).isoformat()


def build_workbook(path: Path) -> None:
    ds = load_dataset()
    rng = random.Random(SEED)
    status: dict[str, str] = {}
    notes: dict[str, str] = {}
    owner: dict[str, str] = {}

    for c in ds.ce_items:
        s = pick(rng, CE_PROBS[c.theme])
        n = ""
        if c.id in CE_OVERRIDES:
            s, n = CE_OVERRIDES[c.id]
        status[c.id], notes[c.id] = s, n
        owner[c.id] = CE_OWNERS[c.theme]

    for a in ds.annex:
        helping = ds.ce_helping(a.id)
        strong = [ce for ce, st in helping if st == "strong"]
        if strong and any(status[ce] == "implemented" for ce in strong):
            s = "implemented" if rng.random() < 0.4 else "partial"
        elif helping:
            s = "partial" if rng.random() < 0.5 else "not started"
        else:
            s = pick(rng, ISO_UNMAPPED_PROBS[a.theme])
        n = ""
        if a.id in ISO_OVERRIDES:
            s, n = ISO_OVERRIDES[a.id]
        status[a.id], notes[a.id] = s, n
        owner[a.id] = ISO_OWNERS[a.theme]

    rows = []
    n_ev = 0
    for item_id in [c.id for c in ds.ce_items] + [a.id for a in ds.annex]:
        s = status[item_id]
        ev = reviewed = ""
        if s in ("implemented", "partial"):
            if rng.random() > 0.08:
                n_ev += 1
                ev = f"EVD-{n_ev:03d}"
            if rng.random() > 0.05:
                reviewed = review_date(rng)
        own = owner[item_id]
        if s == "not started" and rng.random() < 0.25:
            own = ""
        rows.append([item_id, s, own, ev, reviewed, notes[item_id]])
    write_csv(path, ["id", "status", "owner", "evidence_ref", "last_reviewed", "notes"], rows)


def run(argv: list[str]) -> None:
    code = main(argv)
    if code != 0:
        raise SystemExit(f"command failed with status {code}: {' '.join(argv)}")


def build(target: Path = EXAMPLES) -> None:
    """Write the example workbook and outputs under ``target`` (sites.csv is always read from examples/)."""
    build_workbook(target / "assessment.csv")
    run(["score", "--workbook", str(target / "assessment.csv"), "--out", str(target / "output-score"),
         "--as-of", AS_OF.isoformat()])
    run(["sites", "--sites", str(EXAMPLES / "sites.csv"), "--out", str(target / "output-sites")])


if __name__ == "__main__":
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else EXAMPLES)
