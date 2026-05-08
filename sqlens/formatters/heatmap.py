from sqlens.parsers.base import PlanNode, is_leaf
from sqlens.formatters.base import BaseFormatter


class HeatmapFormatter(BaseFormatter):
    """Renders a heatmap-style view highlighting nodes by row cost intensity."""

    HEAT_CHARS = [" ", "░", "▒", "▓", "█"]

    def format(self, root: PlanNode) -> str:
        all_nodes: list[PlanNode] = []
        self._collect(root, all_nodes)
        max_rows = max((n.rows for n in all_nodes if n.rows is not None), default=1) or 1
        lines = ["Heatmap (row intensity):", ""]
        self._render(root, all_nodes, max_rows, lines, depth=0)
        return "\n".join(lines)

    def _collect(self, node: PlanNode, acc: list) -> None:
        acc.append(node)
        for child in node.children:
            self._collect(child, acc)

    def _render(self, node: PlanNode, all_nodes: list, max_rows: int, lines: list, depth: int) -> None:
        indent = "  " * depth
        heat = self._heat_char(node.rows, max_rows)
        cost_str = self._format_cost(node.cost) if node.cost else "cost=?"
        rows_str = self._format_rows(node.rows) if node.rows is not None else "rows=?"
        label = f"{indent}{heat} {node.node_type}  [{cost_str}  {rows_str}]"
        lines.append(label)
        for child in node.children:
            self._render(child, all_nodes, max_rows, lines, depth + 1)

    def _heat_char(self, rows, max_rows: int) -> str:
        if rows is None:
            return self.HEAT_CHARS[0]
        ratio = rows / max_rows
        idx = min(int(ratio * (len(self.HEAT_CHARS) - 1)), len(self.HEAT_CHARS) - 1)
        return self.HEAT_CHARS[idx]
