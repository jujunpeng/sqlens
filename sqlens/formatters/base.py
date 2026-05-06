from __future__ import annotations

from abc import ABC, abstractmethod

from sqlens.parsers.base import PlanNode


class BaseFormatter(ABC):
    """Abstract base class for all plan formatters."""

    @abstractmethod
    def format(self, root: PlanNode) -> str:
        """Render *root* and its subtree as a human-readable string."""
        ...

    # ------------------------------------------------------------------ helpers

    def _indent_lines(self, text: str, level: int, indent: str = "  ") -> str:
        """Re-indent every line in *text* by *level* * *indent*."""
        prefix = indent * level
        return "\n".join(prefix + line for line in text.splitlines())

    def _format_cost(self, value: float) -> str:
        """Return a human-readable cost string."""
        if value >= 1_000_000:
            return f"{value / 1_000_000:.2f}M"
        if value >= 1_000:
            return f"{value / 1_000:.2f}k"
        return f"{value:.2f}"
