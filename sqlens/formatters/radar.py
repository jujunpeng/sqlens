"""Radar/spider-chart-style ASCII formatter for plan node metrics."""

from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class RadarFormatter(BaseFormatter):
    """Display per-node metrics as a simple ASCII radar summary."""

    name = "radar"

    def format(self, root: PlanNode) -> str:
        nodes: list[PlanNode] = []
        self._collect(root, nodes)

        lines = ["Radar View — Node Metrics", "=" * 40]
        for node in nodes:
            lines.append(self._render_node(node))
        return "\n".join(lines)

    def _collect(self, node: PlanNode, acc: list[PlanNode]) -> None:
        acc.append(node)
        for child in node.children:
            self._collect(child, acc)

    def _render_node(self, node: PlanNode) -> str:
        rows = node.rows or 0
        cost_str = node.cost or "0..0"
        try:
            total_cost = float(cost_str.split("..")[-1])
        except (ValueError, IndexError):
            total_cost = 0.0

        max_bar = 20
        row_bar = self._scale_bar(rows, 10_000, max_bar)
        cost_bar = self._scale_bar(total_cost, 5_000.0, max_bar)

        lines = [
            f"  [{node.node_type}]",
            f"    rows  [{row_bar:<{max_bar}}] {rows}",
            f"    cost  [{cost_bar:<{max_bar}}] {total_cost:.2f}",
        ]
        return "\n".join(lines)

    def _scale_bar(self, value: float, max_value: float, width: int) -> str:
        if max_value <= 0:
            filled = 0
        else:
            filled = min(int((value / max_value) * width), width)
        return "#" * filled
