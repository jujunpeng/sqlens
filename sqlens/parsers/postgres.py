"""PostgreSQL EXPLAIN (FORMAT JSON) plan parser."""

from __future__ import annotations
from typing import Any
import json

from sqlens.parsers.base import BasePlanParser, PlanNode


class PostgresPlanParser(BasePlanParser):
    """Parses PostgreSQL JSON-format EXPLAIN output into a PlanNode tree."""

    @property
    def dialect(self) -> str:
        return "postgres"

    def parse(self, raw: Any) -> PlanNode:
        """Accept a JSON string or already-decoded list/dict."""
        if isinstance(raw, str):
            raw = json.loads(raw)
        # PostgreSQL wraps the plan in a list with a single dict
        if isinstance(raw, list):
            raw = raw[0]
        plan_dict = raw.get("Plan", raw)
        return self._parse_node(plan_dict)

    def _parse_node(self, data: dict[str, Any]) -> PlanNode:
        startup = data.get("Startup Cost", 0.0)
        total = data.get("Total Cost", 0.0)
        actual = data.get("Actual Total Time")

        node = PlanNode(
            node_type=data.get("Node Type", "Unknown"),
            cost=total - startup,
            actual_time=actual,
            rows=data.get("Plan Rows") or data.get("Actual Rows"),
            width=data.get("Plan Width"),
            relation=data.get("Relation Name"),
            index_name=data.get("Index Name"),
            join_type=data.get("Join Type"),
            extra={
                "startup_cost": startup,
                "total_cost": total,
                "parallel_aware": data.get("Parallel Aware", False),
                "filter": data.get("Filter"),
                "index_cond": data.get("Index Cond"),
            },
        )

        for child_data in data.get("Plans", []):
            node.children.append(self._parse_node(child_data))

        return node
