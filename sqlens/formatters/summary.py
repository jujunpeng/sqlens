from sqlens.formatters.base import BaseFormatter
from sqlens.parsers.base import PlanNode, total_nodes


class SummaryFormatter(BaseFormatter):
    """Formats a query plan as a compact summary with key statistics."""

    dialect = "summary"

    def format(self, root: PlanNode) -> str:
        lines = []
        lines.append(self._section("Query Plan Summary"))
        lines.append(f"  Total nodes : {total_nodes(root)}")
        lines.append(f"  Root node   : {root.node_type}")

        total_cost = root.extra.get("Total Cost") or root.extra.get("total_cost")
        startup_cost = root.extra.get("Startup Cost") or root.extra.get("startup_cost")
        if total_cost is not None:
            lines.append(f"  Total cost  : {self._format_cost(float(total_cost))}")
        if startup_cost is not None:
            lines.append(f"  Startup cost: {self._format_cost(float(startup_cost))}")

        rows = root.extra.get("Plan Rows") or root.extra.get("rows")
        if rows is not None:
            lines.append(f"  Est. rows   : {rows}")

        lines.append("")
        lines.append(self._section("Node Breakdown"))
        counts: dict[str, int] = {}
        self._count_nodes(root, counts)
        for node_type, count in sorted(counts.items(), key=lambda x: -x[1]):
            lines.append(f"  {node_type:<30} x{count}")

        warnings = self._collect_warnings(root)
        if warnings:
            lines.append("")
            lines.append(self._section("Warnings"))
            for w in warnings:
                lines.append(f"  ⚠  {w}")

        return "\n".join(lines)

    def _section(self, title: str) -> str:
        return f"{'─' * 4} {title} {'─' * (40 - len(title))}"

    def _count_nodes(self, node: PlanNode, counts: dict[str, int]) -> None:
        counts[node.node_type] = counts.get(node.node_type, 0) + 1
        for child in node.children:
            self._count_nodes(child, counts)

    def _collect_warnings(self, node: PlanNode) -> list[str]:
        warnings: list[str] = []
        self._walk_warnings(node, warnings)
        return warnings

    def _walk_warnings(self, node: PlanNode, warnings: list[str]) -> None:
        if "Seq Scan" in node.node_type:
            table = node.extra.get("Relation Name", "unknown table")
            warnings.append(f"Sequential scan on '{table}'")
        cost = node.extra.get("Total Cost") or node.extra.get("total_cost")
        if cost is not None and float(cost) > 10_000:
            warnings.append(f"High cost node: {node.node_type} (cost={float(cost):.2f})")
        for child in node.children:
            self._walk_warnings(child, warnings)
