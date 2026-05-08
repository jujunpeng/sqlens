"""Diff formatter: compare two plan nodes side-by-side."""
from __future__ import annotations

from typing import List, Tuple

from sqlens.formatters.base import BaseFormatter
from sqlens.parsers.base import PlanNode


class DiffFormatter(BaseFormatter):
    """Format two query plans as a side-by-side diff summary."""

    name = "diff"

    def format(self, node: PlanNode) -> str:  # type: ignore[override]
        raise NotImplementedError(
            "DiffFormatter requires two plans; use format_diff(left, right) instead."
        )

    def format_diff(self, left: PlanNode, right: PlanNode) -> str:
        lines: List[str] = []
        lines.append("=" * 60)
        lines.append("  PLAN DIFF")
        lines.append("=" * 60)
        lines.append(f"  {'LEFT':<28}  {'RIGHT':<28}")
        lines.append("-" * 60)

        left_rows = self._flatten(left)
        right_rows = self._flatten(right)
        max_len = max(len(left_rows), len(right_rows))

        changed = 0
        for i in range(max_len):
            l_label = left_rows[i] if i < len(left_rows) else "<missing>"
            r_label = right_rows[i] if i < len(right_rows) else "<missing>"
            marker = "*" if l_label != r_label else " "
            if l_label != r_label:
                changed += 1
            lines.append(f"{marker} {l_label:<28}  {r_label:<28}")

        lines.append("-" * 60)
        lines.append(f"  Nodes compared : {max_len}")
        lines.append(f"  Differences    : {changed}")
        lines.append("=" * 60)
        return "\n".join(lines)

    # ------------------------------------------------------------------
    def _flatten(self, node: PlanNode) -> List[str]:
        """Return a pre-order list of node labels."""
        result: List[str] = []
        self._walk(node, result)
        return result

    def _walk(self, node: PlanNode, acc: List[str]) -> None:
        label = node.node_type
        cost = node.estimated_cost
        rows = node.estimated_rows
        parts: List[str] = [label]
        if cost is not None:
            parts.append(f"cost={cost:.1f}")
        if rows is not None:
            parts.append(f"rows={rows}")
        acc.append(" ".join(parts))
        for child in node.children:
            self._walk(child, acc)
