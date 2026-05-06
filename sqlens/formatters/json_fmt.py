import json
from sqlens.formatters.base import BaseFormatter
from sqlens.parsers.base import PlanNode


class JsonFormatter(BaseFormatter):
    """Formats a query plan as a JSON structure for machine-readable output."""

    def format(self, root: PlanNode) -> str:
        return json.dumps(self._node_to_dict(root), indent=2)

    def _node_to_dict(self, node: PlanNode) -> dict:
        result = {
            "node_type": node.node_type,
            "extra": node.extra,
        }

        if node.cost is not None:
            result["cost"] = node.cost

        if node.rows is not None:
            result["rows"] = node.rows

        if node.children:
            result["children"] = [self._node_to_dict(child) for child in node.children]
        else:
            result["children"] = []

        return result
