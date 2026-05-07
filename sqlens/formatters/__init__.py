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

_FORMATTERS = {
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
}


def get_formatter(name: str):
    """Return a formatter instance by name."""
    key = name.lower()
    if key not in _FORMATTERS:
        available = ", ".join(sorted(_FORMATTERS))
        raise ValueError(f"Unknown formatter '{name}'. Available: {available}")
    return _FORMATTERS[key]()


def list_formatters() -> list:
    """Return sorted list of available formatter names."""
    return sorted(_FORMATTERS.keys())
