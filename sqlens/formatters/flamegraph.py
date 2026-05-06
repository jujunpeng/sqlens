from __future__ import annotations

from sqlens.formatters.base import BaseFormatter
from sqlens.parsers.base import PlanNode


class FlamegraphFormatter(BaseFormatter):
    """Render a plan as an ASCII flame-graph (horizontal bar chart).

    Each node is drawn as a bar whose width is proportional to its
    *actual_rows* (or *estimated_rows* when actual is unavailable),
    indented by depth to convey the call hierarchy.
    """

    BAR_CHAR = "█"
    MAX_BAR_WIDTH = 40

    def format(self, root: PlanNode) -> str:
        lines: list[str] = ["Flame Graph (rows scale)\n"]
        max_rows = self._max_rows(root)
        self._render(root, depth=0, max_rows=max_rows, lines=lines)
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _render(
        self,
        node: PlanNode,
        depth: int,
        max_rows: float,
        lines: list[str],
    ) -> None:
        rows = node.actual_rows if node.actual_rows is not None else node.estimated_rows
        bar_len = self._bar_length(rows, max_rows)
        bar = self.BAR_CHAR * bar_len
        cost_str = self._format_cost(node.estimated_cost)
        indent = "  " * depth
        label = f"{indent}{node.node_type:<28} {bar:<{self.MAX_BAR_WIDTH}}  rows={rows or 0:>8.0f}  cost={cost_str}"
        lines.append(label)
        for child in node.children:
            self._render(child, depth + 1, max_rows, lines)

    def _bar_length(self, rows: float | None, max_rows: float) -> int:
        if not max_rows or rows is None:
            return 1
        ratio = rows / max_rows
        return max(1, round(ratio * self.MAX_BAR_WIDTH))

    def _max_rows(self, node: PlanNode) -> float:
        val = node.actual_rows if node.actual_rows is not None else node.estimated_rows
        current = val or 0.0
        for child in node.children:
            current = max(current, self._max_rows(child))
        return current
