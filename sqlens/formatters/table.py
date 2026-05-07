from sqlens.formatters.base import BaseFormatter
from sqlens.parsers.base import PlanNode


class TableFormatter(BaseFormatter):
    """Renders the query plan as an ASCII table."""

    name = "table"

    def format(self, root: PlanNode) -> str:
        rows = self._collect_rows(root, depth=0)
        if not rows:
            return ""

        headers = ["Node Type", "Depth", "Rows", "Cost", "Extra"]
        col_widths = [len(h) for h in headers]

        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        sep = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
        header_line = "|" + "|".join(
            f" {h:<{col_widths[i]}} " for i, h in enumerate(headers)
        ) + "|"

        lines = [sep, header_line, sep]
        for row in rows:
            line = "|" + "|".join(
                f" {str(cell):<{col_widths[i]}} " for i, cell in enumerate(row)
            ) + "|"
            lines.append(line)
        lines.append(sep)
        return "\n".join(lines)

    def _collect_rows(self, node: PlanNode, depth: int) -> list:
        indent = "  " * depth
        node_type = indent + node.node_type
        rows_val = self._format_rows(node.rows)
        cost_val = self._format_cost(node.cost)
        extra = node.extra.get("relation", "") or node.extra.get("index", "") or ""
        rows = [[node_type, depth, rows_val, cost_val, extra]]
        for child in node.children:
            rows.extend(self._collect_rows(child, depth + 1))
        return rows
