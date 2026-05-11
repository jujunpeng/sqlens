"""Sequence diagram formatter — renders the plan as an ASCII sequence diagram."""

from __future__ import annotations

from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class SequenceFormatter(BaseFormatter):
    """Format a query plan as a plain-text sequence diagram.

    Each node is treated as an 'actor'; edges flow from child to parent,
    representing rows being passed up the execution pipeline.
    """

    name = "sequence"

    def format(self, root: PlanNode) -> str:  # type: ignore[override]
        lines: list[str] = []
        lines.append("Sequence Diagram — Query Execution Pipeline")
        lines.append("=" * 44)
        self._render(root, lines, parent_label=None)
        return "\n".join(lines)

    def _render(self, node: PlanNode, lines: list[str], parent_label: str | None) -> None:
        label = self._node_label(node)
        if parent_label is not None:
            rows = self._format_rows(node.rows)
            cost = self._format_cost(node.cost)
            lines.append(f"  {label:<30} ->  {parent_label}")
            lines.append(f"    rows={rows}  cost={cost}")
        else:
            lines.append(f"  [{label}]  (root)")
        for child in node.children:
            self._render(child, lines, parent_label=label)

    def _node_label(self, node: PlanNode) -> str:
        parts = [node.node_type]
        if node.relation:
            parts.append(node.relation)
        return " ".join(parts)
