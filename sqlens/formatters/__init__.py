from sqlens.formatters.tree import TreeFormatter
from sqlens.formatters.summary import SummaryFormatter
from sqlens.formatters.json_fmt import JsonFormatter
from sqlens.formatters.flamegraph import FlamegraphFormatter
from sqlens.formatters.stats import StatsFormatter
from sqlens.formatters.timeline import TimelineFormatter

_FORMATTERS = {
    "tree": TreeFormatter,
    "summary": SummaryFormatter,
    "json": JsonFormatter,
    "flamegraph": FlamegraphFormatter,
    "stats": StatsFormatter,
    "timeline": TimelineFormatter,
}


def get_formatter(name: str):
    """Return a formatter instance by name.

    Args:
        name: One of 'tree', 'summary', 'json', 'flamegraph', 'stats', 'timeline'.

    Returns:
        An instance of the corresponding formatter.

    Raises:
        ValueError: If the name is not recognised.
    """
    key = name.lower()
    if key not in _FORMATTERS:
        available = ", ".join(sorted(_FORMATTERS))
        raise ValueError(
            f"Unknown formatter '{name}'. Available: {available}"
        )
    return _FORMATTERS[key]()
