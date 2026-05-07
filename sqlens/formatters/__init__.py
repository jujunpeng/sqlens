from __future__ import annotations

from sqlens.formatters.base import BaseFormatter


def get_formatter(name: str) -> BaseFormatter:
    """Return a formatter instance for the given name."""
    name = name.lower().strip()

    if name == "tree":
        from sqlens.formatters.tree import TreeFormatter
        return TreeFormatter()

    if name == "summary":
        from sqlens.formatters.summary import SummaryFormatter
        return SummaryFormatter()

    if name in ("json", "json_fmt"):
        from sqlens.formatters.json_fmt import JsonFormatter
        return JsonFormatter()

    if name == "flamegraph":
        from sqlens.formatters.flamegraph import FlamegraphFormatter
        return FlamegraphFormatter()

    if name == "stats":
        from sqlens.formatters.stats import StatsFormatter
        return StatsFormatter()

    if name == "timeline":
        from sqlens.formatters.timeline import TimelineFormatter
        return TimelineFormatter()

    if name == "dot":
        from sqlens.formatters.dot import DotFormatter
        return DotFormatter()

    if name == "markdown":
        from sqlens.formatters.markdown import MarkdownFormatter
        return MarkdownFormatter()

    if name == "mermaid":
        from sqlens.formatters.mermaid import MermaidFormatter
        return MermaidFormatter()

    if name == "csv":
        from sqlens.formatters.csv import CsvFormatter
        return CsvFormatter()

    if name == "html":
        from sqlens.formatters.html import HtmlFormatter
        return HtmlFormatter()

    raise ValueError(f"Unknown formatter: {name!r}")
