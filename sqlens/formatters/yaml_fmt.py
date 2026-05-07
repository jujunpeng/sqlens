"""YAML formatter for query execution plans."""
from typing import Any, Dict

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class YamlFormatter(BaseFormatter):
    """Renders a query plan as YAML."""

    def format(self, root: PlanNode) -> str:
        if not HAS_YAML:
            raise RuntimeError(
                "PyYAML is required for YAML output. "
                "Install it with: pip install pyyaml"
            )
        data = self._node_to_dict(root)
        return yaml.dump(data, default_flow_style=False, sort_keys=False).rstrip()

    def _node_to_dict(self, node: PlanNode) -> Dict[str, Any]:
        result: Dict[str, Any] = {"node_type": node.node_type}

        if node.cost is not None:
            result["cost"] = node.cost
        if node.rows is not None:
            result["rows"] = node.rows
        if node.extra:
            result["extra"] = node.extra
        if node.children:
            result["children"] = [
                self._node_to_dict(child) for child in node.children
            ]

        return result
