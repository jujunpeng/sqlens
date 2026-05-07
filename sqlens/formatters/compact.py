"""Compact single-line-per-node formatter for quick plan inspection."""

from sqlens.formatters.base import BaseFormatter
from sqlens.parsers.base import PlanNode


class CompactFormatter(BaseFormatter):
    """Renders each plan node as a single line with key metrics inline."""

    name = "compact"

    def format(self, root: PlanNode) -> str:
        lines = []
        self._render_node(root, lines, depth=0, prefix="")
        return "\n".join(lines)

    def _render_node(
        self,
        node: PlanNode,
        lines: list,
        depth: int,
        prefix: str,
    ) -> None:
        indent = "  " * depth
        node_type = node.node_type or "Unknown"
        cost = self._format_cost(node.cost)
        rows = self._format_rows(node.estimated_rows)

        parts = [f"{indent}{prefix}{node_type}"]
        if cost:
            parts.append(f"cost={cost}")
        if rows:
            parts.append(f"rows={rows}")
        if node.relation:
            parts.append(f"on={node.relation}")
        if node.index_name:
            parts.append(f"idx={node.index_name}")

        lines.append("  ".join(parts))

        child_count = len(node.children)
        for i, child in enumerate(node.children):
            is_last = i == child_count - 1
            child_prefix = "└─ " if is_last else "├─ "
            self._render_node(child, lines, depth + 1, child_prefix)
