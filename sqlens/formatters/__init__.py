from sqlens.formatters.tree import TreeFormatter
from sqlens.formatters.summary import SummaryFormatter
from sqlens.formatters.json_fmt import JsonFormatter
from sqlens.formatters.flamegraph import FlamegraphFormatter
from sqlens.formatters.stats import StatsFormatter
from sqlens.formatters.timeline import TimelineFormatter
from sqlens.formatters.dot import DotFormatter
from sqlens.formatters.markdown import MarkdownFormatter
from sqlens.formatters.mermaid import MermaidFormatter

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
}


def get_formatter(fmt: str):
    """Return a formatter instance for the given format name.

    Args:
        fmt: One of 'tree', 'summary', 'json', 'flamegraph', 'stats',
             'timeline', 'dot', 'markdown', 'mermaid'.

    Raises:
        ValueError: If the format name is not recognised.
    """
    key = fmt.lower()
    if key not in _FORMATTERS:
        available = ", ".join(sorted(_FORMATTERS))
        raise ValueError(
            f"Unknown formatter '{fmt}'. Available formatters: {available}"
        )
    return _FORMATTERS[key]()
