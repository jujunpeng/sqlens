"""Sankey-style flow formatter showing row flow between plan nodes."""
from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class SankeyFormatter(BaseFormatter):
    """Renders a text-based Sankey diagram showing row flow through plan nodes."""

    name = "sankey"

    def format(self, root: PlanNode) -> str:
        lines = ["== Row Flow (Sankey) ==", ""]
        self._render(root, lines, depth=0)
        return "\n".join(lines)

    def _render(self, node: PlanNode, lines: list, depth: int) -> None:
        indent = "  " * depth
        label = self._node_label(node)
        bar = self._flow_bar(node.rows)
        rows_str = f"{node.rows:,}" if node.rows is not None else "?"
        lines.append(f"{indent}{label}")
        lines.append(f"{indent}  rows: {rows_str}  {bar}")
        if node.cost:
            lines.append(f"{indent}  cost: {self._format_cost(node.cost)}")
        if node.children:
            lines.append(f"{indent}  |")
            for child in node.children:
                self._render(child, lines, depth + 1)
        lines.append("")

    def _node_label(self, node: PlanNode) -> str:
        parts = [f"[{node.node_type}]"]
        if node.relation:
            parts.append(f"on {node.relation}")
        if node.index:
            parts.append(f"via {node.index}")
        return " ".join(parts)

    def _flow_bar(self, rows) -> str:
        if rows is None:
            return ""
        max_width = 30
        try:
            length = min(max_width, max(1, int(rows / 100)))
        except (TypeError, ValueError):
            return ""
        return "▶" * length
