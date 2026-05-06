"""Tests for the DOT/Graphviz formatter."""

import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.dot import DotFormatter
from sqlens.formatters import get_formatter


def make_node(node_type, total_cost=None, actual_rows=None, relation=None, children=None):
    return PlanNode(
        node_type=node_type,
        total_cost=total_cost,
        startup_cost=None,
        actual_rows=actual_rows,
        actual_time=None,
        relation=relation,
        extra={},
        children=children or [],
    )


@pytest.fixture
def simple_root():
    child = make_node("Seq Scan", total_cost=10.0, actual_rows=100, relation="users")
    return make_node("Hash Join", total_cost=55.0, actual_rows=50, children=[child])


class TestDotFormatter:
    def setup_method(self):
        self.fmt = DotFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_starts_with_digraph(self, simple_root):
        result = self.fmt.format(simple_root)
        assert result.startswith("digraph query_plan {")

    def test_output_ends_with_closing_brace(self, simple_root):
        result = self.fmt.format(simple_root)
        assert result.strip().endswith("}")

    def test_contains_node_type(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result
        assert "Seq Scan" in result

    def test_contains_relation(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "users" in result

    def test_contains_edge(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "->" in result

    def test_single_node_no_edges(self):
        node = make_node("Seq Scan", total_cost=5.0, actual_rows=10)
        result = self.fmt.format(node)
        assert "->" not in result

    def test_node_ids_are_unique(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "n0 [" in result
        assert "n1 [" in result

    def test_get_formatter_returns_dot(self):
        formatter = get_formatter("dot")
        assert isinstance(formatter, DotFormatter)

    def test_actual_rows_in_edge_label(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "rows=" in result
