"""Cascade formatter – renders the plan as a left-to-right cost cascade.

Each node is printed on its own line with a proportional bar that
represents its total_cost relative to the root's total_cost.
"""

from __future__ import annotations

from sqlens.formatters.base import BaseFormatter
from sqlens.parsers.base import PlanNode

_BAR_WIDTH = 36
_FILL = "█"
_EMPTY = "░"


class CascadeFormatter(BaseFormatter):
    name = "cascade"

    def format(self, root: PlanNode) -> str:
        max_cost = self._max_cost(root)
        lines: list[str] = ["Cascade cost view", "=" * 52, ""]
        self._render(root, depth=0, max_cost=max_cost, lines=lines)
        return "\n".join(lines)

    def _render(
        self,
        node: PlanNode,
        depth: int,
        max_cost: float,
        lines: list[str],
    ) -> None:
        bar = self._cost_bar(node, max_cost)
        indent = "  " * depth
        cost_str = self._format_cost(node.cost)
        rows_str = self._format_rows(node.rows)
        label = f"{indent}{node.node_type}"
        lines.append(f"{label:<28} {bar}  cost={cost_str} rows={rows_str}")
        for child in node.children:
            self._render(child, depth + 1, max_cost, lines)

    def _cost_bar(self, node: PlanNode, max_cost: float) -> str:
        if max_cost == 0:
            filled = 0
        else:
            raw = self._extract_total(node.cost)
            filled = round((raw / max_cost) * _BAR_WIDTH)
            filled = max(0, min(filled, _BAR_WIDTH))
        return _FILL * filled + _EMPTY * (_BAR_WIDTH - filled)

    def _max_cost(self, node: PlanNode) -> float:
        val = self._extract_total(node.cost)
        for child in node.children:
            val = max(val, self._max_cost(child))
        return val

    @staticmethod
    def _extract_total(cost: str) -> float:
        """Parse the upper bound from a cost string like '0.00..8.49'."""
        if not cost:
            return 0.0
        try:
            parts = cost.split("..")
            return float(parts[-1])
        except (ValueError, IndexError):
            return 0.0
