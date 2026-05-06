"""CSV formatter: exports plan nodes as comma-separated values."""

from __future__ import annotations

import csv
import io
from typing import List

from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class CsvFormatter(BaseFormatter):
    """Render a query plan as a flat CSV table.

    Each row represents one node in the plan tree.  Columns:
        depth, node_type, rows, cost_start, cost_total, extra
    """

    COLUMNS = ["depth", "node_type", "rows", "cost_start", "cost_total", "extra"]

    def format(self, root: PlanNode) -> str:  # type: ignore[override]
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=self.COLUMNS, lineterminator="\n")
        writer.writeheader()
        for row in self._collect_rows(root, depth=0):
            writer.writerow(row)
        return buf.getvalue()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _collect_rows(self, node: PlanNode, depth: int) -> List[dict]:
        cost_start, cost_total = self._split_cost(node.cost)
        extra_parts = []
        for key in ("index_name", "filter", "join_type"):
            val = node.extra.get(key)
            if val:
                extra_parts.append(f"{key}={val}")

        rows: List[dict] = [
            {
                "depth": depth,
                "node_type": node.node_type,
                "rows": node.rows if node.rows is not None else "",
                "cost_start": cost_start,
                "cost_total": cost_total,
                "extra": " | ".join(extra_parts),
            }
        ]
        for child in node.children:
            rows.extend(self._collect_rows(child, depth + 1))
        return rows

    @staticmethod
    def _split_cost(cost: str | None) -> tuple[str, str]:
        """Return (startup, total) strings from a cost like '0.00..8.27'."""
        if not cost:
            return "", ""
        if ".." in cost:
            parts = cost.split("..")
            return parts[0].strip(), parts[1].strip()
        return "", cost.strip()
