from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class IndentFormatter(BaseFormatter):
    """Formats a query plan as a plain indented text block."""

    name = "indent"

    def format(self, root: PlanNode) -> str:
        lines = []
        self._render_node(root, lines, depth=0)
        return "\n".join(lines)

    def _render_node(self, node: PlanNode, lines: list, depth: int) -> None:
        prefix = "  " * depth
        cost_str = self._format_cost(node.cost) if node.cost else ""
        rows_str = self._format_rows(node.rows) if node.rows is not None else ""

        parts = [node.node_type]
        if node.relation:
            parts.append(f"on {node.relation}")
        if cost_str:
            parts.append(f"cost={cost_str}")
        if rows_str:
            parts.append(f"rows={rows_str}")
        if node.extra.get("Index Name"):
            parts.append(f"index={node.extra['Index Name']}")
        if node.extra.get("Filter"):
            parts.append(f"filter={node.extra['Filter']}")

        lines.append(f"{prefix}{' '.join(parts)}")

        for child in node.children:
            self._render_node(child, lines, depth + 1)
