"""Small helpers for reading and writing CSV files deterministically."""

from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Iterable, Sequence

from .errors import ReadinessError


def read_csv(
    path: str | Path,
    required: Sequence[str],
    optional: Sequence[str] = (),
) -> list[tuple[int, dict[str, str]]]:
    """Read a CSV file and return ``(line_number, row)`` pairs.

    Header names are matched case-insensitively. Values are stripped. Rows that
    are completely empty are skipped. A UTF-8 byte order mark (added by some
    spreadsheet programs) is tolerated. Columns that are neither required nor
    optional are ignored.
    """
    p = Path(path)
    if not p.is_file():
        raise ReadinessError(f"File not found: {p}")
    try:
        text = p.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as exc:
        raise ReadinessError(f"Cannot read {p}: {exc}") from exc

    reader = csv.reader(io.StringIO(text, newline=""))
    try:
        header = next(reader)
    except StopIteration:
        raise ReadinessError(f"{p} is empty. Expected a header row with: {', '.join(required)}")
    names = [h.strip().lower() for h in header]
    missing = [c for c in required if c not in names]
    if missing:
        raise ReadinessError(
            f"{p} is missing required column(s): {', '.join(missing)}. "
            f"Found: {', '.join(n for n in names if n) or 'none'}"
        )
    wanted = list(required) + list(optional)
    index = {name: names.index(name) for name in wanted if name in names}

    rows: list[tuple[int, dict[str, str]]] = []
    problems: list[str] = []
    for raw in reader:
        line = reader.line_num
        if not any(cell.strip() for cell in raw):
            continue
        if len(raw) > len(names) and any(cell.strip() for cell in raw[len(names):]):
            problems.append(f"{p.name} line {line}: more values than header columns")
            continue
        row = {
            name: (raw[i].strip() if i < len(raw) else "")
            for name, i in index.items()
        }
        rows.append((line, row))
    if problems:
        raise ReadinessError(problems)
    return rows


def write_csv(path: str | Path, header: Sequence[str], rows: Iterable[Sequence[object]]) -> None:
    """Write a CSV with Unix line endings so output is identical on every platform."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def write_text(path: str | Path, text: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as fh:
        fh.write(text if text.endswith("\n") else text + "\n")
