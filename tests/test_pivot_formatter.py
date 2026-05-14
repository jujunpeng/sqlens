"""Tests for PivotFormatter."""

from __future__ import annotations

import pytest

from sqlens.parsers.base import PlanNode
from sqlens.formatters.pivot import PivotFormatter
from sqlens.formatters import get_formatter, list_formatters


def make_node(
    node_type: str,
    cost=None,
    rows=None,
    children=None,
) -> PlanNode:
    return PlanNode(
        node_type=node_type,
        cost=cost,
        rows=rows,
        extra={},
        children=children or [],
    )


@pytest.fixture
def simple_root() -> PlanNode:
    child1 = make_node("Index Scan", cost=5.0, rows=10)
    child2 = make_node("Index Scan", cost=3.0, rows=20)
    return make_node("Hash Join", cost=15.0, rows=30, children=[child1, child2])


class TestPivotFormatter:
    def setup_method(self):
        self.fmt = PivotFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_format_contains_header(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Node Type" in result
        assert "Total Cost" in result
        assert "Avg Rows" in result

    def test_format_contains_node_types(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result
        assert "Index Scan" in result

    def test_index_scan_count_is_two(self, simple_root):
        result = self.fmt.format(simple_root)
        lines = [l for l in result.splitlines() if "Index Scan" in l]
        assert len(lines) == 1
        # count column should show 2
        assert "2" in lines[0]

    def test_total_cost_aggregated(self, simple_root):
        result = self.fmt.format(simple_root)
        # Index Scan total cost = 5.0 + 3.0 = 8.00
        assert "8.00" in result

    def test_single_node_no_children(self):
        node = make_node("Seq Scan", cost=10.0, rows=100)
        result = self.fmt.format(node)
        assert "Seq Scan" in result
        assert "10.00" in result

    def test_none_cost_treated_as_zero(self):
        node = make_node("Seq Scan", cost=None, rows=None)
        result = self.fmt.format(node)
        assert "Seq Scan" in result
        assert "0.00" in result

    def test_empty_children_list(self):
        node = make_node("Result", cost=1.0, rows=1)
        result = self.fmt.format(node)
        assert "Result" in result

    def test_total_node_types_line(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Total node types:" in result
        assert "2" in result.splitlines()[-1]

    def test_get_formatter_returns_pivot(self):
        fmt = get_formatter("pivot")
        assert isinstance(fmt, PivotFormatter)

    def test_pivot_in_list_formatters(self):
        names = list_formatters()
        assert "pivot" in names

    def test_get_formatter_case_insensitive(self):
        fmt = get_formatter("PIVOT")
        assert isinstance(fmt, PivotFormatter)
