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
}


def get_formatter(fmt: str):
    """Return a formatter instance for the given format name.

    Args:
        fmt: One of 'tree', 'summary', 'json', 'flamegraph', 'stats',
             'timeline', 'dot', 'markdown', 'mermaid', 'csv', 'html', 'text'.

    Returns:
        An instance of the corresponding formatter.

    Raises:
        ValueError: If the format name is not recognised.
    """
    key = fmt.lower().strip()
    if key not in _FORMATTERS:
        supported = ", ".join(sorted(_FORMATTERS))
        raise ValueError(
            f"Unknown formatter '{fmt}'. Supported formats: {supported}"
        )
    return _FORMATTERS[key]()


def list_formatters() -> list:
    """Return a sorted list of supported formatter names."""
    return sorted(_FORMATTERS.keys())
