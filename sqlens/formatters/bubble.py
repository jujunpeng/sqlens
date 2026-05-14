"""Bubble chart formatter — renders nodes as ASCII bubbles sized by row count."""

from __future__ import annotations

from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class BubbleFormatter(BaseFormatter):
    """Render each plan node as an ASCII bubble whose radius reflects row count."""

    name = "bubble"

    # Bubble radii available (1-5)
    _RADII = [
        ["+"],
        ["-+-", "| |", "-+-"],
        [" .-.", "(   )", " '-'"],
        [" .---.", "|     |", "|     |", " '---'"],
        [" .-----.", "|       |", "|       |", "|       |", " '-----'"],
    ]

    def format(self, root: PlanNode) -> str:
        nodes: list[PlanNode] = []
        self._collect(root, nodes)
        max_rows = max((n.rows or 0) for n in nodes) if nodes else 1
        lines: list[str] = ["Bubble Chart — node size ∝ estimated rows", ""]
        for node in nodes:
            lines.extend(self._render_bubble(node, max_rows))
            lines.append("")
        return "\n".join(lines).rstrip()

    def _collect(self, node: PlanNode, out: list[PlanNode]) -> None:
        out.append(node)
        for child in node.children:
            self._collect(child, out)

    def _radius(self, node: PlanNode, max_rows: int) -> int:
        rows = node.rows or 0
        if max_rows == 0:
            return 1
        ratio = rows / max_rows
        return max(1, min(5, round(ratio * 5)))

    def _render_bubble(self, node: PlanNode, max_rows: int) -> list[str]:
        radius = self._radius(node, max_rows)
        bubble_lines = self._RADII[radius - 1]
        label = self._node_label(node)
        result: list[str] = []
        for i, bline in enumerate(bubble_lines):
            if i == len(bubble_lines) // 2:
                result.append(f"  {bline}  {label}")
            else:
                result.append(f"  {bline}")
        return result

    def _node_label(self, node: PlanNode) -> str:
        parts = [node.node_type]
        if node.rows is not None:
            parts.append(f"rows={node.rows}")
        if node.cost is not None:
            parts.append(self._format_cost(node.cost))
        return "  ".join(parts)
