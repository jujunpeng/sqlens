"""PathView formatter: shows execution path from root to each leaf node."""

from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class PathViewFormatter(BaseFormatter):
    """Render all root-to-leaf paths in the plan tree."""

    name = "pathview"

    def format(self, root: PlanNode) -> str:
        paths = []
        self._collect_paths(root, [], paths)
        lines = ["Execution Paths", "=" * 40]
        for idx, path in enumerate(paths, 1):
            lines.append(f"Path {idx}:")
            for step, node in enumerate(path):
                connector = "  └─ " if step > 0 else "  "
                label = self._step_label(node)
                lines.append(f"  {'  ' * step}{connector}{label}")
            lines.append("")
        if not paths:
            lines.append("  (no nodes)")
        return "\n".join(lines).rstrip()

    def _collect_paths(
        self,
        node: PlanNode,
        current: list,
        paths: list,
    ) -> None:
        current = current + [node]
        if not node.children:
            paths.append(current)
        else:
            for child in node.children:
                self._collect_paths(child, current, paths)

    def _step_label(self, node: PlanNode) -> str:
        parts = [node.node_type]
        if node.cost:
            parts.append(f"[{self._format_cost(node.cost)}]")
        if node.rows is not None:
            parts.append(f"→ {self._format_rows(node.rows)} rows")
        return " ".join(parts)
