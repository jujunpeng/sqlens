"""Color/ANSI formatter — wraps another formatter's output with terminal colors."""
from __future__ import annotations

from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


RESET = "\033[0m"

COLORS = {
    "header": "\033[1;36m",   # bold cyan
    "node_type": "\033[1;33m",  # bold yellow
    "cost": "\033[0;32m",       # green
    "rows": "\033[0;34m",       # blue
    "warn": "\033[1;31m",       # bold red
    "dim": "\033[2m",           # dim
}

WARN_KEYWORDS = ("Seq Scan", "Hash Join", "Nested Loop", "Bitmap Heap Scan")


def colorize(text: str, key: str) -> str:
    code = COLORS.get(key, "")
    return f"{code}{text}{RESET}" if code else text


class ColorFormatter(BaseFormatter):
    """Applies ANSI color codes to tree output for terminal display."""

    name = "color"

    def format(self, root: PlanNode) -> str:  # type: ignore[override]
        lines = self._render_node(root, prefix="", is_last=True)
        return "\n".join(lines)

    def _render_node(self, node: PlanNode, prefix: str, is_last: bool) -> list[str]:
        connector = "└── " if is_last else "├── "
        label = self._node_label(node)
        lines = [prefix + connector + label]

        child_prefix = prefix + ("    " if is_last else "│   ")
        children = node.children or []
        for i, child in enumerate(children):
            lines.extend(
                self._render_node(child, child_prefix, i == len(children) - 1)
            )
        return lines

    def _node_label(self, node: PlanNode) -> str:
        ntype = node.node_type or "Unknown"
        color_key = "warn" if any(k in ntype for k in WARN_KEYWORDS) else "node_type"
        colored_type = colorize(ntype, color_key)

        parts = [colored_type]
        if node.cost:
            parts.append(colorize(f"cost={node.cost}", "cost"))
        if node.rows is not None:
            parts.append(colorize(f"rows={node.rows}", "rows"))
        return "  ".join(parts)
