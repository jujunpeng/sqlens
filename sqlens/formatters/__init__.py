"""Formatter registry — maps format names to formatter classes."""
from __future__ import annotations

from sqlens.formatters.tree import TreeFormatter
from sqlens.formatters.summary import SummaryFormatter
from sqlens.formatters.json_fmt import JsonFormatter
from sqlens.formatters.flamegraph import FlamegraphFormatter
from sqlens.formatters.stats import StatsFormatter
from sqlens.formatters.timeline import TimelineFormatter
from sqlens.formatters.dot import DotFormatter
from sqlens.formatters.markdown import MarkdownFormatter
from sqlens.formatters.mermaid import MermaidFormatter
from sqlens.formatters.csv import CsvFormatter
from sqlens.formatters.html import HtmlFormatter
from sqlens.formatters.text import TextFormatter
from sqlens.formatters.compact import CompactFormatter
from sqlens.formatters.yaml_fmt import YamlFormatter
from sqlens.formatters.table import TableFormatter
from sqlens.formatters.outline import OutlineFormatter
from sqlens.formatters.indent import IndentFormatter
from sqlens.formatters.color import ColorFormatter

_REGISTRY: dict[str, type] = {
    "tree": TreeFormatter,
    "summary": SummaryFormatter,
    "json": JsonFormatter,
    "flamegraph": FlamegraphFormatter,
    "stats": StatsFormatter,
    "timeline": TimelineFormatter,
    "dot": DotFormatter,
    "markdown": MarkdownFormatter,
    "mermaid": MermaidFormatter,
    "csv": CsvFormatter,
    "html": HtmlFormatter,
    "text": TextFormatter,
    "compact": CompactFormatter,
    "yaml": YamlFormatter,
    "table": TableFormatter,
    "outline": OutlineFormatter,
    "indent": IndentFormatter,
    "color": ColorFormatter,
}


def get_formatter(name: str):
    """Return an instantiated formatter for *name*, or raise ValueError."""
    key = name.lower().strip()
    if key not in _REGISTRY:
        available = ", ".join(sorted(_REGISTRY))
        raise ValueError(f"Unknown formatter {name!r}. Available: {available}")
    return _REGISTRY[key]()


def list_formatters() -> list[str]:
    """Return sorted list of registered formatter names."""
    return sorted(_REGISTRY.keys())
