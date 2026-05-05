"""MySQL EXPLAIN FORMAT=JSON plan parser."""

from __future__ import annotations
from typing import Any
import json

from sqlens.parsers.base import BasePlanParser, PlanNode


class MySQLPlanParser(BasePlanParser):
    """Parses MySQL JSON-format EXPLAIN output into a PlanNode tree."""

    @property
    def dialect(self) -> str:
        return "mysql"

    def parse(self, raw: Any) -> PlanNode:
        """Accept a JSON string or already-decoded dict."""
        if isinstance(raw, str):
            raw = json.loads(raw)
        query_block = raw.get("query_block", raw)
        return self._parse_block(query_block)

    def _parse_block(self, block: dict[str, Any]) -> PlanNode:
        table = block.get("table", {})
        node_type = table.get("access_type", "query_block").upper()

        node = PlanNode(
            node_type=node_type,
            rows=table.get("rows_examined_per_scan") or block.get("select_id"),
            relation=table.get("table_name"),
            index_name=table.get("key"),
            extra={
                "possible_keys": table.get("possible_keys", []),
                "key_length": table.get("key_length"),
                "filtered": table.get("filtered"),
                "using_index": table.get("using_index", False),
                "cost_info": table.get("cost_info", {}),
            },
        )

        cost_info = table.get("cost_info", {})
        if "read_cost" in cost_info:
            try:
                node.cost = float(cost_info.get("query_cost", 0.0))
            except (TypeError, ValueError):
                node.cost = None

        for nested in block.get("nested_loop", []):
            child_block = nested if "table" in nested else nested.get("query_block", nested)
            node.children.append(self._parse_block(child_block))

        for sub_key in ("ordering_operation", "grouping_operation"):
            if sub_key in block:
                node.children.append(self._parse_block(block[sub_key]))

        return node
