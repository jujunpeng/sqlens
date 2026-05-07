from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class OutlineFormatter(BaseFormatter):
    """
    Renders the query plan as a numbered outline (1., 1.1., 1.1.1., …)
    with cost and row estimates on each line.
    """

    name = "outline"

    def format(self, root: PlanNode) -> str:
        lines = ["Query Plan Outline", "=================="]
        self._render_node(root, [], lines)
        return "\n".join(lines)

    def _render_node(
        self,
        node: PlanNode,
        index_path: list,
        lines: list,
        depth: int = 0,
    ) -> None:
        # Build section number like "1.", "1.2.", "1.2.3."
        section = ".".join(str(i) for i in index_path) + "." if index_path else "1."
        indent = "    " * depth

        cost_str = self._format_cost(node.cost)
        rows_str = self._format_rows(node.rows)

        parts = [f"{indent}{section} {node.node_type}"]
        if node.relation:
            parts.append(f"on {node.relation}")
        meta: list[str] = []
        if cost_str:
            meta.append(f"cost={cost_str}")
        if rows_str:
            meta.append(f"rows={rows_str}")
        if meta:
            parts.append(f"({', '.join(meta)})")

        lines.append(" ".join(parts))

        for i, child in enumerate(node.children, start=1):
            self._render_node(child, index_path + [i], lines, depth + 1)
