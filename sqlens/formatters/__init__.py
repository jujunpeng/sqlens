from sqlens.formatters.tree import TreeFormatter
from sqlens.formatters.summary import SummaryFormatter
from sqlens.formatters.base import BaseFormatter

_FORMATTERS: dict[str, type[BaseFormatter]] = {
    "tree": TreeFormatter,
    "summary": SummaryFormatter,
}

_DEFAULT = "tree"


def get_formatter(style: str | None = None) -> BaseFormatter:
    """Return a formatter instance for the given style name.

    Args:
        style: One of 'tree' or 'summary'. Defaults to 'tree'.

    Raises:
        ValueError: If *style* is not a known formatter name.
    """
    key = (style or _DEFAULT).lower()
    if key not in _FORMATTERS:
        known = ", ".join(sorted(_FORMATTERS))
        raise ValueError(f"Unknown formatter style '{style}'. Known styles: {known}")
    return _FORMATTERS[key]()
