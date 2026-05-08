"""Tests for SankeyFormatter."""
import pytest
from sqlens.formatters.sankey import SankeyFormatter
from sqlens.parsers.base import PlanNode


def make_node(node_type, rows=None, cost=None, relation=None, index=None, children=None):
    return PlanNode(
        node_type=node_type,
        rows=rows,
        cost=cost,
        relation=relation,
        index=index,
        children=children or [],
        extra={},
    )


@pytest.fixture
def simple_root():
    child = make_node("Seq Scan", rows=500, cost="0.00..10.00", relation="orders")
    return make_node("Aggregate", rows=1, cost="10.00..10.01", children=[child])


class TestSankeyFormatter:
    def setup_method(self):
        self.fmt = SankeyFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_contains_header(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Sankey" in result

    def test_contains_root_node_type(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Aggregate" in result

    def test_contains_child_node_type(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Seq Scan" in result

    def test_contains_relation(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "orders" in result

    def test_contains_rows(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "500" in result

    def test_flow_bar_present_for_large_rows(self):
        node = make_node("Seq Scan", rows=1000)
        result = self.fmt.format(node)
        assert "▶" in result

    def test_flow_bar_absent_for_none_rows(self):
        node = make_node("Seq Scan", rows=None)
        result = self.fmt.format(node)
        assert "?" in result

    def test_node_with_index(self):
        node = make_node("Index Scan", rows=10, index="idx_users_email", relation="users")
        result = self.fmt.format(node)
        assert "idx_users_email" in result
        assert "users" in result

    def test_no_children(self):
        node = make_node("Result", rows=1, cost="0.00..0.01")
        result = self.fmt.format(node)
        assert "Result" in result
        assert isinstance(result, str)
