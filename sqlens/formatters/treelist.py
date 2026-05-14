"""TreeList formatter: numbered hierarchical list of plan nodes."""

from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class TreeListFormatter(BaseFormatter):
    """Render plan nodes as a numbered hierarchical list."""

    name = "treelist"

    def format(self, root: PlanNode) -> str:
        lines = ["Plan Node List", "=" * 30]
        counter = [0]
        self._render_node(root, depth=0, lines=lines, counter=counter)
        return "\n".join(lines)

    def _render_node(
        self,
        node: PlanNode,
        depth: int,
        lines: list,
        counter: list,
    ) -> None:
        counter[0] += 1
        index = counter[0]
        indent = "  " * depth
        label = self._node_label(node)
        lines.append(f"{indent}{index}. {label}")
        for child in node.children:
            self._render_node(child, depth + 1, lines, counter)

    def _node_label(self, node: PlanNode) -> str:
        parts = [node.node_type]
        if node.cost:
            parts.append(f"cost={self._format_cost(node.cost)}")
        if node.rows is not None:
            parts.append(f"rows={self._format_rows(node.rows)}")
        if node.extra.get("relation"):
            parts.append(f"on {node.extra['relation']}")
        return "  ".join(parts)
