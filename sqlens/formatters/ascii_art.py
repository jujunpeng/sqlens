from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter

_CORNER = "\u2514"
_TEE = "\u251c"
_PIPE = "\u2502"
_DASH = "\u2500"


class AsciiArtFormatter(BaseFormatter):
    """Renders a query plan as a Unicode box-drawing tree."""

    name = "ascii_art"

    def format(self, root: PlanNode) -> str:
        lines: list[str] = []
        self._render_node(root, lines, prefix="", is_last=True)
        return "\n".join(lines)

    def _render_node(
        self, node: PlanNode, lines: list, prefix: str, is_last: bool
    ) -> None:
        connector = f"{_CORNER}{_DASH}{_DASH} " if is_last else f"{_TEE}{_DASH}{_DASH} "
        label = self._build_label(node)
        lines.append(f"{prefix}{connector}{label}")
        child_prefix = prefix + ("    " if is_last else f"{_PIPE}   ")
        for i, child in enumerate(node.children):
            self._render_node(
                child, lines, child_prefix, is_last=(i == len(node.children) - 1)
            )

    def _build_label(self, node: PlanNode) -> str:
        parts = [node.node_type]
        if node.relation:
            parts.append(f"on {node.relation}")
        cost = self._format_cost(node.cost)
        if cost:
            parts.append(cost)
        rows = self._format_rows(node.rows)
        if rows:
            parts.append(rows)
        return "  ".join(parts)
