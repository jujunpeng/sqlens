from __future__ import annotations

from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class SunburstFormatter(BaseFormatter):
    """Render a text-based sunburst / radial hierarchy of the plan tree.

    Each depth level is shown as an indented ring, with row-proportional
    bar segments to give a rough sense of relative cost.
    """

    name = "sunburst"

    def format(self, root: PlanNode) -> str:
        max_rows = self._max_rows(root)
        lines: list[str] = ["Sunburst Plan View", "=" * 40]
        self._render(root, depth=0, lines=lines, max_rows=max_rows)
        return "\n".join(lines)

    def _render(
        self,
        node: PlanNode,
        depth: int,
        lines: list[str],
        max_rows: int,
    ) -> None:
        indent = "  " * depth
        arc = self._arc_bar(node.rows or 0, max_rows)
        label = self._node_label(node)
        lines.append(f"{indent}[{arc}] {label}")
        for child in node.children:
            self._render(child, depth + 1, lines, max_rows)

    def _arc_bar(self, rows: int, max_rows: int, width: int = 12) -> str:
        if max_rows == 0:
            filled = 0
        else:
            filled = round((rows / max_rows) * width)
        filled = max(0, min(filled, width))
        return "#" * filled + "-" * (width - filled)

    def _node_label(self, node: PlanNode) -> str:
        parts = [node.node_type]
        if node.rows is not None:
            parts.append(f"rows={node.rows}")
        if node.cost is not None:
            parts.append(f"cost={node.cost}")
        return "  ".join(parts)

    def _max_rows(self, node: PlanNode) -> int:
        val = node.rows or 0
        for child in node.children:
            val = max(val, self._max_rows(child))
        return val
