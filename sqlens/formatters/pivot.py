"""Pivot formatter: cross-tabulates node types against cost/rows metrics."""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple

from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class PivotFormatter(BaseFormatter):
    """Display a pivot table of node types vs. aggregated metrics."""

    name = "pivot"

    def format(self, root: PlanNode) -> str:
        rows = self._collect(root)
        if not rows:
            return "(no data)"

        # Aggregate per node type
        agg: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
        for node_type, cost, est_rows in rows:
            agg[node_type]["cost"].append(cost)
            agg[node_type]["rows"].append(est_rows)

        node_types = sorted(agg.keys())
        col_w = max(len(t) for t in node_types)
        col_w = max(col_w, 20)

        header = f"{'Node Type':<{col_w}}  {'Count':>6}  {'Total Cost':>12}  {'Avg Cost':>10}  {'Total Rows':>12}  {'Avg Rows':>10}"
        sep = "-" * len(header)

        lines: List[str] = ["Pivot: Node Type Metrics", sep, header, sep]

        for node_type in node_types:
            costs = agg[node_type]["cost"]
            est_rows_list = agg[node_type]["rows"]
            count = len(costs)
            total_cost = sum(costs)
            avg_cost = total_cost / count if count else 0.0
            total_rows = sum(est_rows_list)
            avg_rows = total_rows / count if count else 0.0
            lines.append(
                f"{node_type:<{col_w}}  {count:>6}  {total_cost:>12.2f}  {avg_cost:>10.2f}  {total_rows:>12.0f}  {avg_rows:>10.0f}"
            )

        lines.append(sep)
        lines.append(f"Total node types: {len(node_types)}")
        return "\n".join(lines)

    def _collect(self, node: PlanNode) -> List[Tuple[str, float, float]]:
        """Walk tree and return (node_type, cost, rows) tuples."""
        results: List[Tuple[str, float, float]] = []
        stack = [node]
        while stack:
            current = stack.pop()
            try:
                cost = float(current.cost) if current.cost is not None else 0.0
            except (TypeError, ValueError):
                cost = 0.0
            try:
                est_rows = float(current.rows) if current.rows is not None else 0.0
            except (TypeError, ValueError):
                est_rows = 0.0
            results.append((current.node_type, cost, est_rows))
            stack.extend(current.children)
        return results
