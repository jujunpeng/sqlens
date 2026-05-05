from abc import ABC, abstractmethod
from typing import List
from sqlens.parsers.base import PlanNode


class BaseFormatter(ABC):
    """Abstract base class for plan formatters."""

    INDENT = "  "
    BRANCH = "├── "
    LAST_BRANCH = "└── "
    PIPE = "│   "
    SPACE = "    "

    @abstractmethod
    def format(self, root: PlanNode) -> str:
        """Format a plan tree into a string representation."""
        raise NotImplementedError

    def _indent_lines(self, lines: List[str], prefix: str) -> List[str]:
        return [prefix + line for line in lines]

    def _format_cost(self, node: PlanNode) -> str:
        parts = []
        if "actual_rows" in node.stats:
            parts.append(f"rows={node.stats['actual_rows']}")
        if "actual_time" in node.stats:
            parts.append(f"time={node.stats['actual_time']}ms")
        if "cost" in node.stats:
            parts.append(f"cost={node.stats['cost']}")
        return f"  ({', '.join(parts)})" if parts else ""
