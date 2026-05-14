"""Tests for MatrixFormatter."""

from __future__ import annotations

import pytest

from sqlens.parsers.base import PlanNode
from sqlens.formatters.matrix import MatrixFormatter
from sqlens.formatters import get_formatter, list_formatters


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


@pytest.fixture
def simple_root() -> PlanNode:
    child = make_node("Index Scan", cost="0.00..8.27", rows=1)
    return make_node("Seq Scan", cost="0.00..45.00", rows=1000, children=[child])


class TestMatrixFormatter:
    def setup_method(self):
        self.fmt = MatrixFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_contains_header(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Matrix" in result

    def test_output_contains_node_types(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Seq Scan" in result
        assert "Index Scan" in result

    def test_output_contains_bar_chars(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "[" in result and "]" in result

    def test_total_nodes_line(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Total nodes: 2" in result

    def test_single_node_no_children(self):
        node = make_node("Hash Join", cost="10.00..50.00", rows=200)
        result = self.fmt.format(node)
        assert "Hash Join" in result
        assert "Total nodes: 1" in result

    def test_empty_cost_handled(self):
        node = make_node("Result", cost=None, rows=None)
        result = self.fmt.format(node)
        assert "Result" in result

    def test_scale_bar_full(self):
        bar = self.fmt._scale_bar(10.0, 10.0, width=10)
        assert bar == "[##########]"

    def test_scale_bar_empty(self):
        bar = self.fmt._scale_bar(0.0, 10.0, width=10)
        assert bar == "[..........]"

    def test_scale_bar_half(self):
        bar = self.fmt._scale_bar(5.0, 10.0, width=10)
        assert bar == "[#####.....]" 

    def test_registered_in_list(self):
        assert "matrix" in list_formatters()

    def test_get_formatter_returns_matrix(self):
        fmt = get_formatter("matrix")
        assert isinstance(fmt, MatrixFormatter)

    def test_get_formatter_case_insensitive(self):
        fmt = get_formatter("Matrix")
        assert isinstance(fmt, MatrixFormatter)
