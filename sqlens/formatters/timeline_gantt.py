from sqlens.parsers.base import PlanNode, is_leaf
from sqlens.formatters.base import BaseFormatter


class TimelineGanttFormatter(BaseFormatter):
    """Renders a Gantt-style horizontal timeline of node costs."""

    WIDTH = 60

    def format(self, root: PlanNode) -> str:
        nodes: list[tuple[str, float, float]] = []
        self._collect(root, nodes)
        if not nodes:
            return "(no nodes)"

        max_end = max(end for _, _, end in nodes) or 1.0
        lines = ["Gantt Timeline (cost units)\n"]
        lines.append(f"  {'Node':<28} {'0':>1}{' ' * (self.WIDTH - 2)}{'max':>3}")
        lines.append("  " + "-" * (28 + self.WIDTH + 4))

        for label, start, end in nodes:
            bar = self._gantt_bar(start, end, max_end)
            lines.append(f"  {label:<28} {bar}  {end:.1f}")

        return "\n".join(lines)

    def _collect(
        self,
        node: PlanNode,
        out: list[tuple[str, float, float]],
    ) -> None:
        label = self._node_label(node)
        try:
            parts = (node.cost or "").split("..")
            start = float(parts[0]) if parts else 0.0
            end = float(parts[1]) if len(parts) > 1 else start
        except (ValueError, AttributeError):
            start, end = 0.0, 0.0
        out.append((label, start, end))
        for child in node.children:
            self._collect(child, out)

    def _gantt_bar(self, start: float, end: float, max_end: float) -> str:
        s = int(start / max_end * self.WIDTH)
        e = int(end / max_end * self.WIDTH)
        e = max(e, s + 1)
        bar = " " * s + "=" * (e - s) + " " * (self.WIDTH - e)
        return f"[{bar}]"

    def _node_label(self, node: PlanNode) -> str:
        label = node.node_type
        if node.relation:
            label += f" ({node.relation})"
        return label[:28]
