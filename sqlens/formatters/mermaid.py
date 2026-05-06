from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class MermaidFormatter(BaseFormatter):
    """Renders a query plan as a Mermaid flowchart diagram."""

    def format(self, root: PlanNode) -> str:
        lines = ["flowchart TD"]
        self._render(root, lines, parent_id=None, counter=[0])
        return "\n".join(lines)

    def _render(
        self,
        node: PlanNode,
        lines: list,
        parent_id: str | None,
        counter: list,
    ) -> str:
        node_id = f"N{counter[0]}"
        counter[0] += 1

        label = self._node_label(node)
        # Escape quotes inside labels
        label = label.replace('"', "'")
        lines.append(f'    {node_id}["{label}"]')

        if parent_id is not None:
            lines.append(f"    {parent_id} --> {node_id}")

        for child in node.children:
            self._render(child, lines, parent_id=node_id, counter=counter)

        return node_id

    def _node_label(self, node: PlanNode) -> str:
        parts = [node.node_type]
        if node.relation:
            parts.append(f"on {node.relation}")
        cost = self._format_cost(node.estimated_cost)
        if cost:
            parts.append(cost)
        return " | ".join(parts)
