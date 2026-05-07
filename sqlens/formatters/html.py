from __future__ import annotations

from sqlens.parsers.base import PlanNode, is_leaf
from sqlens.formatters.base import BaseFormatter


class HtmlFormatter(BaseFormatter):
    """Render a query plan as a self-contained HTML page."""

    def format(self, root: PlanNode) -> str:
        body = self._render_node(root, depth=0)
        return (
            "<!DOCTYPE html>\n"
            "<html lang=\"en\">\n"
            "<head>\n"
            "  <meta charset=\"UTF-8\">\n"
            "  <title>Query Plan</title>\n"
            "  <style>\n"
            "    body { font-family: monospace; padding: 1rem; }\n"
            "    details { margin-left: 1.5rem; }\n"
            "    summary { cursor: pointer; }\n"
            "    .node-type { font-weight: bold; color: #2563eb; }\n"
            "    .cost { color: #6b7280; font-size: 0.9em; }\n"
            "    .rows { color: #059669; font-size: 0.9em; }\n"
            "    .leaf summary { list-style: disc; }\n"
            "  </style>\n"
            "</head>\n"
            "<body>\n"
            "<h2>Query Execution Plan</h2>\n"
            f"{body}\n"
            "</body>\n"
            "</html>"
        )

    def _render_node(self, node: PlanNode, depth: int) -> str:
        cost_str = self._format_cost(node.cost)
        rows_str = self._format_rows(node.rows)
        label = (
            f"<span class=\"node-type\">{node.node_type}</span>"
            f" <span class=\"cost\">{cost_str}</span>"
            f" <span class=\"rows\">{rows_str}</span>"
        )
        if is_leaf(node):
            return f"<details class=\"leaf\"><summary>{label}</summary></details>"

        children_html = "\n".join(
            self._render_node(child, depth + 1) for child in node.children
        )
        return (
            f"<details open>\n"
            f"  <summary>{label}</summary>\n"
            f"  {children_html}\n"
            f"</details>"
        )
