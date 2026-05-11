"""Waterfall formatter — shows cumulative cost as a horizontal bar chart."""

from __future__ import annotations

from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter

_BAR_WIDTH = 40


class WaterfallFormatter(BaseFormatter):
    """Render a waterfall chart of node costs in the terminal."""

    name = "waterfall"

    def format(self, root: PlanNode) -> str:  # type: ignore[override]
        nodes: list[PlanNode] = []
        self._collect(root, nodes)
        max_cost = self._max_total(nodes)
        lines: list[str] = []
        lines.append("Waterfall — Cumulative Cost")
        lines.append("-" * 60)
        header = f"  {'Node':<28} {'Cost':>10}  Chart"
        lines.append(header)
        lines.append("-" * 60)
        for node in nodes:
            label = self._node_label(node)
            total = self._total_cost(node)
            bar = self._bar(total, max_cost)
            lines.append(f"  {label:<28} {total:>10.2f}  {bar}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    def _collect(self, node: PlanNode, out: list[PlanNode]) -> None:
        out.append(node)
        for child in node.children:
            self._collect(child, out)

    def _total_cost(self, node: PlanNode) -> float:
        """Return the upper bound of the cost range."""
        try:
            return float(node.cost.split("..")[1])
        except (AttributeError, IndexError, ValueError):
            return 0.0

    def _max_total(self, nodes: list[PlanNode]) -> float:
        costs = [self._total_cost(n) for n in nodes]
        return max(costs) if costs else 1.0

    def _bar(self, value: float, maximum: float) -> str:
        if maximum == 0:
            length = 0
        else:
            length = int(round(value / maximum * _BAR_WIDTH))
        return "█" * length

    def _node_label(self, node: PlanNode) -> str:
        parts = [node.node_type]
        if node.relation:
            parts.append(node.relation)
        label = " ".join(parts)
        return label[:28]
