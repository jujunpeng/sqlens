from sqlens.formatters.base import BaseFormatter
from sqlens.parsers.base import PlanNode
from typing import List, Tuple


class StatsFormatter(BaseFormatter):
    """Formatter that outputs a statistical breakdown of plan nodes."""

    def format(self, root: PlanNode) -> str:
        lines: List[str] = []
        lines.append("=== Query Plan Statistics ===")
        lines.append("")

        nodes = self._collect_all(root)
        total = len(nodes)
        lines.append(f"Total nodes : {total}")

        total_cost = root.cost or 0.0
        lines.append(self._format_cost("Total cost  ", total_cost))

        avg_cost = total_cost / total if total else 0.0
        lines.append(self._format_cost("Avg cost    ", avg_cost))

        lines.append("")
        lines.append("--- Node type breakdown ---")
        type_counts = self._count_by_type(nodes)
        for node_type, count in sorted(type_counts, key=lambda x: -x[1]):
            pct = (count / total * 100) if total else 0
            lines.append(f"  {node_type:<30} {count:>4}  ({pct:.1f}%)")

        lines.append("")
        lines.append("--- Cost distribution ---")
        costs = [n.cost for n in nodes if n.cost is not None]
        if costs:
            lines.append(f"  Min : {min(costs):.2f}")
            lines.append(f"  Max : {max(costs):.2f}")
            lines.append(f"  Sum : {sum(costs):.2f}")
        else:
            lines.append("  No cost data available.")

        return "\n".join(lines)

    def _collect_all(self, node: PlanNode) -> List[PlanNode]:
        result = [node]
        for child in node.children:
            result.extend(self._collect_all(child))
        return result

    def _count_by_type(self, nodes: List[PlanNode]) -> List[Tuple[str, int]]:
        counts: dict = {}
        for node in nodes:
            counts[node.node_type] = counts.get(node.node_type, 0) + 1
        return list(counts.items())
