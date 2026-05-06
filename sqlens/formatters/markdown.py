from sqlens.formatters.base import BaseFormatter
from sqlens.parsers.base import PlanNode


class MarkdownFormatter(BaseFormatter):
    """Renders a query execution plan as a Markdown document."""

    def format(self, root: PlanNode) -> str:
        lines = []
        lines.append("# Query Execution Plan\n")
        lines.append(self._render_node(root, depth=0))
        return "\n".join(lines)

    def _render_node(self, node: PlanNode, depth: int) -> str:
        indent = "  " * depth
        heading_level = min(depth + 2, 6)
        heading = "#" * heading_level
        parts = [f"{indent}{heading} {node.node_type}"]

        if node.relation:
            parts.append(f"{indent}- **Relation:** `{node.relation}`")
        if node.index_name:
            parts.append(f"{indent}- **Index:** `{node.index_name}`")

        cost_str = self._format_cost(node.startup_cost, node.total_cost)
        if cost_str:
            parts.append(f"{indent}- **Cost:** {cost_str}")

        if node.rows is not None:
            parts.append(f"{indent}- **Rows:** {node.rows}")
        if node.width is not None:
            parts.append(f"{indent}- **Width:** {node.width}")
        if node.actual_rows is not None:
            parts.append(f"{indent}- **Actual Rows:** {node.actual_rows}")
        if node.actual_time is not None:
            parts.append(f"{indent}- **Actual Time:** {node.actual_time:.3f} ms")

        for child in node.children:
            parts.append("")
            parts.append(self._render_node(child, depth + 1))

        return "\n".join(parts)
