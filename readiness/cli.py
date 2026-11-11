"""Command line interface: ``python -m readiness <command>``."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from . import __version__
from .csvio import write_csv, write_text
from .datafiles import load_dataset
from .errors import ReadinessError
from .report import render_report
from .scoring import score
from .sites import (
    SITE_ROW_HEADER,
    assess_sites,
    control_set_rows,
    load_config,
    read_sites,
    render_sites_markdown,
    site_rows,
    to_json,
)
from .soa import SOA_COLUMNS, build_soa, soa_markdown, summarise_soa
from .workbook import SCOPES, init_workbook, read_workbook

EXIT_INPUT = 2
EXIT_BELOW_THRESHOLD = 3


def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid date. Use YYYY-MM-DD")


def _positive_int(value: str) -> int:
    try:
        n = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a whole number")
    if n < 1:
        raise argparse.ArgumentTypeError("must be 1 or more")
    return n


def _percent(value: str) -> float:
    try:
        n = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a number")
    if not 0 <= n <= 100:
        raise argparse.ArgumentTypeError("must be between 0 and 100")
    return n


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m readiness",
        description="Readiness kit for Cyber Essentials Plus and ISO/IEC 27001 preparation.",
    )
    parser.add_argument("--version", action="version", version=f"readiness {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="create a blank assessment workbook (CSV)")
    p_init.add_argument("--out", default="assessment.csv", help="workbook to create (default assessment.csv)")
    p_init.add_argument("--scope", choices=SCOPES, default="both", help="which items to include (default both)")
    p_init.add_argument("--with-titles", action="store_true", help="add a read-only title column to help people fill it in")
    p_init.add_argument("--force", action="store_true", help="overwrite an existing file")
    p_init.add_argument("--data-dir", help="folder with the reference CSV files (default: data/ in the repository)")

    p_score = sub.add_parser("score", help="score a workbook and write the report, SoA draft and JSON")
    p_score.add_argument("--workbook", default="assessment.csv", help="workbook to read (default assessment.csv)")
    p_score.add_argument("--out", default="output", help="folder for results (default output)")
    p_score.add_argument("--as-of", type=_parse_date, default=None,
                         help="date used for review ageing, YYYY-MM-DD (default today). Set it for repeatable output")
    p_score.add_argument("--review-days", type=_positive_int, default=365,
                         help="evidence is overdue when last reviewed more than this many days ago (default 365)")
    p_score.add_argument("--fail-under", type=_percent, default=None,
                         help="exit with status 3 if any scope's overall coverage is below this percentage")
    p_score.add_argument("--data-dir", help="folder with the reference CSV files")

    p_sites = sub.add_parser("sites", help="tier sites by risk and list the minimum control set per tier")
    p_sites.add_argument("--sites", default="sites.csv", help="sites CSV (default sites.csv)")
    p_sites.add_argument("--config", help="tiering config JSON (default config/site-tiering.json)")
    p_sites.add_argument("--out", default="output", help="folder for results (default output)")
    p_sites.add_argument("--data-dir", help="folder with the reference CSV files")
    return parser


def cmd_init(args: argparse.Namespace) -> int:
    dataset = load_dataset(args.data_dir)
    n = init_workbook(args.out, dataset, args.scope, args.with_titles, args.force)
    print(f"Wrote {n} rows to {args.out}")
    print("Next: fill in status, owner, evidence_ref, last_reviewed (YYYY-MM-DD) and notes, then run:")
    print(f"  python -m readiness score --workbook {args.out}")
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    dataset = load_dataset(args.data_dir)
    as_of = args.as_of or date.today()
    wb = read_workbook(args.workbook, dataset, as_of)
    result = score(dataset, wb, as_of, args.review_days)
    out = Path(args.out)
    name = Path(args.workbook).name

    write_text(out / "report.md", render_report(result, name))
    written = ["report.md"]

    soa_summary = None
    if wb.has_iso:
        entries = build_soa(dataset, wb)
        soa_summary = summarise_soa(entries)
        write_csv(out / "soa.csv", SOA_COLUMNS, ([e[c] for c in SOA_COLUMNS] for e in entries))
        write_text(out / "soa.md", soa_markdown(entries, as_of.isoformat()))
        written += ["soa.csv", "soa.md"]
        result["statement_of_applicability"] = soa_summary
    write_text(out / "report.json", json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    written.append("report.json")

    print(f"Scored {name} as of {as_of.isoformat()}")
    labels = {"ce": "Cyber Essentials", "iso": "ISO Annex A"}
    below: list[str] = []
    for scope, data in result["scopes"].items():
        o = data["overall"]
        cov = "n/a" if o["coverage_percent"] is None else f"{o['coverage_percent']:.1f}%"
        print(f"  {labels[scope]}: coverage {cov} ({o['implemented']} implemented, {o['partial']} partial, "
              f"{o['not_started']} not started, {o['not_applicable']} not applicable)")
        if args.fail_under is not None and (o["coverage_percent"] or 0.0) < args.fail_under:
            below.append(labels[scope])
    print(f"  Gaps: {len(result['gaps'])}. Overdue reviews: {len(result['overdue_reviews'])}. "
          f"No review date: {len(result['no_review_date'])}. Missing evidence: {len(result['missing_evidence'])}")
    if soa_summary:
        print(f"  SoA draft: {soa_summary['included']} included, {soa_summary['excluded']} excluded, "
              f"{soa_summary['included_without_justification']} still need a justification")
    print(f"Wrote {', '.join(written)} to {out}")
    if below:
        print(f"Coverage is below {args.fail_under:g}% for: {', '.join(below)}", file=sys.stderr)
        return EXIT_BELOW_THRESHOLD
    return 0


def cmd_sites(args: argparse.Namespace) -> int:
    dataset = load_dataset(args.data_dir)
    cfg = load_config(args.config, dataset)
    sites = read_sites(args.sites, cfg)
    result = assess_sites(cfg, sites, dataset)
    out = Path(args.out)
    name = Path(args.sites).name

    write_csv(out / "site-tiers.csv", SITE_ROW_HEADER, site_rows(result))
    write_csv(out / "tier-control-sets.csv",
              ("id", "scope", "item", "minimum_tier", "minimum_tier_name"), control_set_rows(result, dataset))
    write_text(out / "sites-report.md", render_sites_markdown(result, name))
    public = {k: v for k, v in result.items() if k != "minimum_tier_by_control"}
    write_text(out / "sites.json", to_json(public))

    print(f"Tiered {len(result['sites'])} sites from {name}")
    for s in result["sites"]:
        print(f"  {s['site']} ({s['country']}): score {s['score']:.1f}, tier {s['tier']} {s['tier_name']}")
    print(f"Wrote site-tiers.csv, tier-control-sets.csv, sites-report.md, sites.json to {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        handler = {"init": cmd_init, "score": cmd_score, "sites": cmd_sites}[args.command]
        return handler(args)
    except ReadinessError as exc:
        print("Cannot continue:", file=sys.stderr)
        for problem in exc.problems:
            print(f"  - {problem}", file=sys.stderr)
        return EXIT_INPUT
