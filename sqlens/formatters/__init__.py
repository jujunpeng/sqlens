from sqlens.formatters.base import BaseFormatter
from sqlens.formatters.tree import TreeFormatter

__all__ = ["BaseFormatter", "TreeFormatter"]


def get_formatter(style: str = "tree") -> BaseFormatter:
    """Return a formatter instance by style name."""
    formatters = {
        "tree": TreeFormatter,
    }
    if style not in formatters:
        raise ValueError(
            f"Unknown formatter style '{style}'. Available: {list(formatters.keys())}"
        )
    return formatters[style]()
