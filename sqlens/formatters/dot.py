"""DOT/Graphviz formatter for query execution plans."""

from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class DotFormatter(BaseFormatter):
    """Renders a query plan as a DOT graph for use with Graphviz."""

    def format(self, root: PlanNode) -> str:
        lines = []
        lines.append("digraph query_plan {")
        lines.append('    rankdir=TB;')
        lines.append('    node [shape=box, fontname="Courier", fontsize=10];')
        lines.append('    edge [fontname="Courier", fontsize=9];')
        lines.append("")
        self._render(root, lines, counter=[0])
        lines.append("}")
        return "\n".join(lines)

    def _render(self, node: PlanNode, lines: list, counter: list, parent_id: int = None) -> None:
        node_id = counter[0]
        counter[0] += 1

        label = self._node_label(node)
        lines.append(f'    n{node_id} [label="{label}"];')

        if parent_id is not None:
            edge_label = ""
            if node.actual_rows is not None:
                edge_label = f" rows={node.actual_rows}"
            lines.append(f'    n{parent_id} -> n{node_id} [label="{edge_label.strip()}"];')

        for child in node.children:
            self._render(child, lines, counter, parent_id=node_id)

    def _node_label(self, node: PlanNode) -> str:
        parts = [node.node_type]
        if node.relation:
            parts.append(f"on {node.relation}")
        cost_str = self._format_cost(node.total_cost)
        if cost_str:
            parts.append(cost_str)
        if node.actual_rows is not None:
            parts.append(f"rows={node.actual_rows}")
        return "\\n".join(parts)
