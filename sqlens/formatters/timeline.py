from sqlens.formatters.base import BaseFormatter
from sqlens.parsers.base import PlanNode
from typing import List, Tuple


class TimelineFormatter(BaseFormatter):
    """Renders a horizontal timeline showing relative node execution costs."""

    BAR_WIDTH = 40

    def format(self, root: PlanNode) -> str:
        rows: List[Tuple[str, float]] = []
        self._collect(root, rows)

        if not rows:
            return "(no nodes)"

        max_cost = max(cost for _, cost in rows) or 1.0
        lines = ["Execution Timeline", "=" * 56, ""]

        for label, cost in rows:
            bar_len = int((cost / max_cost) * self.BAR_WIDTH)
            bar = "█" * bar_len
            cost_str = self._format_cost(cost)
            lines.append(f"  {label:<22} {bar:<{self.BAR_WIDTH}} {cost_str}")

        lines.append("")
        lines.append(f"  Max cost: {self._format_cost(max_cost)}")
        return "\n".join(lines)

    def _collect(self, node: PlanNode, rows: List[Tuple[str, float]]) -> None:
        label = node.node_type[:22]
        rows.append((label, node.total_cost))
        for child in node.children:
            self._collect(child, rows)
