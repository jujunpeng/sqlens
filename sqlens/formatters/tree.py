from typing import List
from sqlens.parsers.base import PlanNode, is_leaf
from sqlens.formatters.base import BaseFormatter


class TreeFormatter(BaseFormatter):
    """Renders a query plan as an ASCII tree in the terminal."""

    def format(self, root: PlanNode) -> str:
        lines = self._render_node(root, prefix="", is_last=True)
        return "\n".join(lines)

    def _render_node(self, node: PlanNode, prefix: str, is_last: bool) -> List[str]:
        connector = self.LAST_BRANCH if is_last else self.BRANCH
        label = self._node_label(node)
        cost = self._format_cost(node)

        if prefix == "":
            header = f"{label}{cost}"
        else:
            header = f"{prefix}{connector}{label}{cost}"

        lines = [header]

        child_prefix = prefix + (self.SPACE if is_last else self.PIPE)
        children = node.children
        for i, child in enumerate(children):
            child_is_last = i == len(children) - 1
            lines.extend(self._render_node(child, child_prefix, child_is_last))

        return lines

    def _node_label(self, node: PlanNode) -> str:
        label = node.node_type
        if node.relation:
            label += f" on {node.relation}"
        if node.extra.get("index_name"):
            label += f" [{node.extra['index_name']}]"
        if node.extra.get("join_type"):
            label += f" ({node.extra['join_type']} join)"
        return label
