"""Tests for the ColorFormatter."""
from __future__ import annotations

import pytest

from sqlens.parsers.base import PlanNode
from sqlens.formatters.color import ColorFormatter, colorize, COLORS, RESET
from sqlens.formatters import get_formatter


def make_node(
    node_type: str,
    cost: str | None = None,
    rows: int | None = None,
    children: list | None = None,
) -> PlanNode:
    return PlanNode(
        node_type=node_type,
        cost=cost,
        rows=rows,
        extra={},
        children=children or [],
    )


@pytest.fixture()
def simple_root() -> PlanNode:
    child = make_node("Index Scan", cost="0.00..8.27", rows=1)
    return make_node("Seq Scan", cost="0.00..35.50", rows=1000, children=[child])


class TestColorFormatter:
    def setup_method(self):
        self.fmt = ColorFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_contains_node_type(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Seq Scan" in result
        assert "Index Scan" in result

    def test_output_contains_cost(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "cost=" in result

    def test_output_contains_rows(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "rows=" in result

    def test_ansi_codes_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "\033[" in result

    def test_warn_color_for_seq_scan(self, simple_root):
        result = self.fmt.format(simple_root)
        # Seq Scan should use the warn color code
        assert COLORS["warn"] in result

    def test_multiline_output(self, simple_root):
        result = self.fmt.format(simple_root)
        lines = result.splitlines()
        assert len(lines) >= 2

    def test_leaf_node_no_children_branch(self):
        node = make_node("Hash", cost="1.00..2.00", rows=5)
        result = self.fmt.format(node)
        assert "Hash" in result
        assert "├──" not in result

    def test_get_formatter_returns_color(self):
        fmt = get_formatter("color")
        assert isinstance(fmt, ColorFormatter)

    def test_colorize_helper(self):
        out = colorize("hello", "header")
        assert out.startswith(COLORS["header"])
        assert out.endswith(RESET)

    def test_colorize_unknown_key(self):
        out = colorize("hello", "nonexistent")
        assert out == "hello"
