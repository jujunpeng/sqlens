from sqlens.parsers.base import PlanNode, is_leaf
from sqlens.formatters.base import BaseFormatter


BARS = " ▁▂▃▄▅▆▇█"


class SparklineFormatter(BaseFormatter):
    """Renders a sparkline bar chart of row estimates across all plan nodes."""

    def format(self, root: PlanNode) -> str:
        nodes: list[PlanNode] = []
        self._collect(root, nodes)

        if not nodes:
            return "(no nodes)"

        rows_list = [n.rows or 0 for n in nodes]
        max_rows = max(rows_list) if rows_list else 1

        lines: list[str] = []
        lines.append("Row Estimates Sparkline")
        lines.append("=" * 40)

        for node, rows in zip(nodes, rows_list):
            bar = self._sparkline_bar(rows, max_rows, width=20)
            label = node.node_type.ljust(28)
            rows_str = self._format_rows(rows)
            lines.append(f"  {label} {bar}  {rows_str} rows")

        lines.append("")
        lines.append(f"Peak: {self._format_rows(max_rows)} rows")
        lines.append(f"Nodes: {len(nodes)}")

        return "\n".join(lines)

    def _collect(self, node: PlanNode, out: list[PlanNode]) -> None:
        out.append(node)
        for child in node.children:
            self._collect(child, out)

    def _sparkline_bar(self, value: int, max_value: int, width: int = 20) -> str:
        if max_value == 0:
            filled = 0
        else:
            filled = round((value / max_value) * width)

        filled = max(1, min(filled, width))
        empty = width - filled

        intensity = (value / max_value) if max_value > 0 else 0
        bar_char_index = min(int(intensity * (len(BARS) - 1)), len(BARS) - 1)
        bar_char = BARS[bar_char_index]

        return f"[{bar_char * filled}{'.' * empty}]"
