from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from sqlens.parsers import get_parser
from sqlens.formatters import get_formatter

FORMATTERS = [
    "tree",
    "summary",
    "json",
    "flamegraph",
    "stats",
    "timeline",
    "dot",
    "markdown",
    "mermaid",
    "csv",
    "html",
]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sqlens",
        description="Parse and visualize PostgreSQL / MySQL query execution plans.",
    )
    p.add_argument(
        "file",
        nargs="?",
        help="Path to a JSON file containing the query plan (reads stdin if omitted).",
    )
    p.add_argument(
        "-d",
        "--dialect",
        choices=["postgres", "mysql"],
        default="postgres",
        help="SQL dialect of the plan (default: postgres).",
    )
    p.add_argument(
        "-f",
        "--format",
        choices=FORMATTERS,
        default="tree",
        dest="formatter",
        help="Output format (default: tree).",
    )
    p.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="Write output to FILE instead of stdout.",
    )
    return p


def read_input(file_arg: str | None) -> str:
    if file_arg is None:
        return sys.stdin.read()
    path = Path(file_arg)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_arg}")
    return path.read_text(encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        raw = read_input(args.file)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON — {exc}", file=sys.stderr)
        return 1

    try:
        plan_parser = get_parser(args.dialect)
        root = plan_parser.parse(data)
    except Exception as exc:  # noqa: BLE001
        print(f"error: could not parse plan — {exc}", file=sys.stderr)
        return 1

    formatter = get_formatter(args.formatter)
    output = formatter.format(root)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
