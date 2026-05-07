from sqlens.formatters.base import BaseFormatter
from sqlens.parsers.base import PlanNode


class TextFormatter(BaseFormatter):
    """Renders the execution plan as plain indented text."""

    def format(self, root: PlanNode) -> str:
        lines = ["Query Execution Plan", "=" * 40]
        self._render_node(root, lines, depth=0)
        return "\n".join(lines)

    def _render_node(self, node: PlanNode, lines: list, depth: int) -> None:
        indent = "  " * depth
        prefix = f"{indent}- "
        label = node.node_type
        if node.relation:
            label += f" on {node.relation}"
        parts = [label]
        if node.cost is not None:
            parts.append(f"cost={self._format_cost(node.cost)}")
        if node.rows is not None:
            parts.append(f"rows={self._format_rows(node.rows)}")
        if node.extra:
            for k, v in node.extra.items():
                parts.append(f"{k}={v}")
        lines.append(prefix + "  ".join(parts))
        for child in node.children:
            self._render_node(child, lines, depth + 1)
