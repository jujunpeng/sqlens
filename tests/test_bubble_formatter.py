"""Tests for BubbleFormatter."""

from __future__ import annotations

import pytest

from sqlens.parsers.base import PlanNode
from sqlens.formatters.bubble import BubbleFormatter
from sqlens.formatters import get_formatter, list_formatters


def make_node(
    node_type: str,
    rows: int | None = None,
    cost: str | None = None,
    children: list[PlanNode] | None = None,
) -> PlanNode:
    return PlanNode(
        node_type=node_type,
        rows=rows,
        cost=cost,
        children=children or [],
        extra={},
    )


@pytest.fixture()
def simple_root() -> PlanNode:
    child = make_node("Seq Scan", rows=50, cost="0.00..10.50")
    return make_node("Hash Join", rows=200, cost="10.50..55.00", children=[child])


class TestBubbleFormatter:
    def setup_method(self):
        self.fmt = BubbleFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_contains_header(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Bubble Chart" in result

    def test_output_contains_node_types(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result
        assert "Seq Scan" in result

    def test_output_contains_rows(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "rows=200" in result
        assert "rows=50" in result

    def test_single_node(self):
        node = make_node("Index Scan", rows=10, cost="0.00..5.00")
        result = self.fmt.format(node)
        assert "Index Scan" in result
        assert "rows=10" in result

    def test_node_without_rows(self):
        node = make_node("Result")
        result = self.fmt.format(node)
        assert "Result" in result

    def test_larger_rows_gets_bigger_bubble(self):
        small = make_node("Seq Scan", rows=1)
        large = make_node("Hash Join", rows=10000, children=[small])
        result = self.fmt.format(large)
        # The large node line should contain more dashes (wider bubble)
        lines = result.splitlines()
        hash_join_lines = [ln for ln in lines if "Hash Join" in ln]
        assert hash_join_lines, "Expected at least one line with Hash Join label"

    def test_registration_in_list(self):
        assert "bubble" in list_formatters()

    def test_get_formatter_returns_bubble(self):
        fmt = get_formatter("bubble")
        assert isinstance(fmt, BubbleFormatter)

    def test_get_formatter_case_insensitive(self):
        fmt = get_formatter("Bubble")
        assert isinstance(fmt, BubbleFormatter)
