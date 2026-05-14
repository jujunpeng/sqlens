"""Network-style formatter: renders the plan as an adjacency list with edge weights."""

from __future__ import annotations

from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class NetworkFormatter(BaseFormatter):
    """Renders the query plan as a network edge list suitable for graph tools.

    Each line describes a directed edge from a parent node to a child node,
    annotated with the estimated row count flowing across that edge.
    """

    def format(self, root: PlanNode) -> str:
        lines: list[str] = []
        lines.append("# sqlens network format")
        lines.append("# source -> target  [rows]  [cost]")
        lines.append("")
        self._render(root, parent_label=None, lines=lines)
        return "\n".join(lines)

    def _render(
        self,
        node: PlanNode,
        parent_label: str | None,
        lines: list[str],
        counter: list[int] | None = None,
    ) -> str:
        if counter is None:
            counter = [0]

        node_id = counter[0]
        counter[0] += 1
        label = self._node_label(node, node_id)

        if parent_label is not None:
            rows_str = self._format_rows(node.rows)
            cost_str = self._format_cost(node.cost)
            lines.append(f"{parent_label} -> {label}  rows={rows_str}  cost={cost_str}")
        else:
            lines.append(f"ROOT: {label}")

        for child in node.children:
            self._render(child, label, lines, counter)

        return label

    def _node_label(self, node: PlanNode, node_id: int) -> str:
        name = node.node_type.replace(" ", "_")
        return f"{name}_{node_id}"
