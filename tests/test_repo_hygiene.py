"""Checks on the repository text: dashes, and that relative Markdown links resolve."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_SUFFIXES = {".md", ".py", ".csv", ".json", ".yml", ".mmd", ".txt", ".toml", ".svg"}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache"}
BAD_DASHES = (chr(0x2014), chr(0x2013))


def _files():
    for p in ROOT.rglob("*"):
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS):
            yield p


def test_no_em_or_en_dashes_anywhere():
    offenders = []
    for p in _files():
        if p.suffix in TEXT_SUFFIXES or p.name in {"LICENSE", ".gitignore"}:
            text = p.read_text(encoding="utf-8", errors="ignore")
            if any(d in text for d in BAD_DASHES):
                offenders.append(str(p.relative_to(ROOT)))
    assert offenders == []


def test_relative_markdown_links_resolve():
    link = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
    broken = []
    for p in _files():
        if p.suffix != ".md":
            continue
        for target in link.findall(p.read_text(encoding="utf-8")):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            path = target.split("#")[0]
            if path and not (p.parent / path).exists():
                broken.append(f"{p.relative_to(ROOT)} -> {target}")
    assert broken == []
