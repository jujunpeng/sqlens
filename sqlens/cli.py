"""CLI entry point for sqlens."""

import sys
import json
import argparse

from sqlens.parsers import get_parser
from sqlens.formatters import get_formatter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sqlens",
        description="Parse and visualize PostgreSQL / MySQL query execution plans.",
    )
    parser.add_argument(
        "plan",
        nargs="?",
        help="Path to a file containing the query plan (JSON). Reads from stdin if omitted.",
    )
    parser.add_argument(
        "-d",
        "--dialect",
        choices=["postgres", "mysql"],
        default="postgres",
        help="SQL dialect of the plan (default: postgres).",
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="style",
        default="tree",
        help="Output format style (default: tree).",
    )
    return parser


def read_input(path: str | None) -> str:
    if path:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    return sys.stdin.read()


def main(argv: list[str] | None = None) -> int:
    arg_parser = build_parser()
    args = arg_parser.parse_args(argv)

    try:
        raw = read_input(args.plan)
    except FileNotFoundError as exc:
        print(f"sqlens: error: {exc}", file=sys.stderr)
        return 1

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"sqlens: error: invalid JSON — {exc}", file=sys.stderr)
        return 1

    try:
        plan_parser = get_parser(args.dialect)
        root = plan_parser.parse(data)
    except (KeyError, ValueError) as exc:
        print(f"sqlens: error: could not parse plan — {exc}", file=sys.stderr)
        return 1

    try:
        formatter = get_formatter(args.style)
        print(formatter.format(root))
    except ValueError as exc:
        print(f"sqlens: error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
