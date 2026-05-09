from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class TreemapFormatter(BaseFormatter):
    """ASCII treemap showing proportional row counts per node."""

    TOTAL_COLS = 60

    def format(self, root: PlanNode) -> str:
        nodes: list[tuple[int, str, int]] = []
        self._collect(root, 0, nodes)
        total_rows = sum(r for _, _, r in nodes) or 1
        lines = ["Treemap (rows proportion)\n"]
        lines.append(f"  {'Node':<30} {'Share':>6}  Bar")
        lines.append("  " + "-" * 60)
        for depth, label, rows in nodes:
            share = rows / total_rows
            bar_len = max(1, int(share * self.TOTAL_COLS))
            bar = "#" * bar_len
            indent = "  " * depth
            lines.append(f"  {indent + label:<30} {share:>5.1%}  {bar}")
        return "\n".join(lines)

    def _collect(
        self,
        node: PlanNode,
        depth: int,
        out: list[tuple[int, str, int]],
    ) -> None:
        label = self._node_label(node)
        rows = node.rows or 0
        out.append((depth, label, rows))
        for child in node.children:
            self._collect(child, depth + 1, out)

    def _node_label(self, node: PlanNode) -> str:
        label = node.node_type
        if node.relation:
            label += f":{node.relation}"
        return label[:28]
