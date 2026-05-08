from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class PlantUMLFormatter(BaseFormatter):
    """Renders a query plan as a PlantUML activity/component diagram."""

    name = "plantuml"

    def format(self, root: PlanNode) -> str:
        lines = ["@startuml", "skinparam defaultTextAlignment center", ""]
        self._render(root, lines)
        lines.append("")
        lines.append("@enduml")
        return "\n".join(lines)

    def _render(self, node: PlanNode, lines: list, parent_id: str = None) -> str:
        node_id = self._make_id(node)
        label = self._node_label(node)
        lines.append(f'rectangle "{label}" as {node_id}')
        if parent_id:
            lines.append(f"{parent_id} --> {node_id}")
        for child in node.children:
            self._render(child, lines, node_id)
        return node_id

    def _make_id(self, node: PlanNode) -> str:
        safe = node.node_type.replace(" ", "_").replace("-", "_")
        return f"{safe}_{id(node)}"

    def _node_label(self, node: PlanNode) -> str:
        parts = [node.node_type]
        if node.relation:
            parts.append(node.relation)
        cost = self._format_cost(node.cost)
        if cost:
            parts.append(cost)
        rows = self._format_rows(node.rows)
        if rows:
            parts.append(rows)
        return "\\n".join(parts)
