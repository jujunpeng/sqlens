"""Matrix formatter: displays plan nodes in a cost/rows grid."""

from __future__ import annotations

from typing import List, Tuple

from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class MatrixFormatter(BaseFormatter):
    """Render a cost-vs-rows matrix where each cell represents a plan node."""

    name = "matrix"

    def format(self, root: PlanNode) -> str:
        nodes = self._collect(root)
        if not nodes:
            return "(empty plan)"

        lines: List[str] = []
        lines.append("Plan Node Matrix  [cost → columns | rows → rows]")
        lines.append("-" * 60)

        header = f"  {'Node Type':<28} {'Cost':>12} {'Rows':>10}"
        lines.append(header)
        lines.append("  " + "-" * 52)

        max_cost = max((self._total_cost(n) for n in nodes), default=1.0) or 1.0
        max_rows = max((n.rows or 0 for n in nodes), default=1) or 1

        for node in nodes:
            cost = self._total_cost(node)
            rows = node.rows or 0
            cost_bar = self._scale_bar(cost, max_cost, width=10)
            rows_bar = self._scale_bar(rows, max_rows, width=8)
            label = node.node_type[:28]
            lines.append(f"  {label:<28} {cost_bar:>12} {rows_bar:>10}")

        lines.append("")
        lines.append(f"  Total nodes: {len(nodes)}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    def _collect(self, node: PlanNode) -> List[PlanNode]:
        result = [node]
        for child in node.children:
            result.extend(self._collect(child))
        return result

    def _total_cost(self, node: PlanNode) -> float:
        if node.cost is None:
            return 0.0
        try:
            parts = str(node.cost).split("..")
            return float(parts[-1])
        except (ValueError, IndexError):
            return 0.0

    def _scale_bar(self, value: float, maximum: float, width: int = 10) -> str:
        if maximum <= 0:
            filled = 0
        else:
            filled = round((value / maximum) * width)
        filled = max(0, min(width, filled))
        return "[" + "#" * filled + "." * (width - filled) + "]"
