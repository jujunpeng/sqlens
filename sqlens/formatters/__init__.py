"""Formatter registry for sqlens."""
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
from sqlens.formatters.sparkline import SparklineFormatter
from sqlens.formatters.diff import DiffFormatter
from sqlens.formatters.plantuml import PlantUMLFormatter
from sqlens.formatters.ascii_art import AsciiArtFormatter
from sqlens.formatters.heatmap import HeatmapFormatter
from sqlens.formatters.sankey import SankeyFormatter

_REGISTRY = {
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
    "sparkline": SparklineFormatter,
    "diff": DiffFormatter,
    "plantuml": PlantUMLFormatter,
    "ascii_art": AsciiArtFormatter,
    "heatmap": HeatmapFormatter,
    "sankey": SankeyFormatter,
}


def get_formatter(name: str):
    """Return an instantiated formatter by name."""
    key = name.lower()
    if key not in _REGISTRY:
        raise ValueError(
            f"Unknown formatter '{name}'. Available: {', '.join(sorted(_REGISTRY))}"
        )
    return _REGISTRY[key]()


def list_formatters() -> list:
    """Return sorted list of available formatter names."""
    return sorted(_REGISTRY.keys())
