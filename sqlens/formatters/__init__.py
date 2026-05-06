from sqlens.formatters.tree import TreeFormatter
from sqlens.formatters.summary import SummaryFormatter
from sqlens.formatters.json_fmt import JsonFormatter

_FORMATTERS = {
    "tree": TreeFormatter,
    "summary": SummaryFormatter,
    "json": JsonFormatter,
}

DEFAULT_FORMAT = "tree"


def get_formatter(fmt: str = DEFAULT_FORMAT):
    """Return an instantiated formatter for the given format name.

    Args:
        fmt: One of 'tree', 'summary', or 'json'. Defaults to 'tree'.

    Returns:
        An instance of the appropriate formatter.

    Raises:
        ValueError: If the format name is not recognised.
    """
    key = fmt.lower()
    if key not in _FORMATTERS:
        raise ValueError(
            f"Unknown format '{fmt}'. Choose from: {', '.join(_FORMATTERS)}"
        )
    return _FORMATTERS[key]()
