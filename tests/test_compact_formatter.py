"""Tests for CompactFormatter."""

import pytest
from sqlens.formatters.compact import CompactFormatter
from sqlens.parsers.base import PlanNode


def make_node(
    node_type="Seq Scan",
    cost=None,
    estimated_rows=None,
    relation=None,
    index_name=None,
    children=None,
):
    return PlanNode(
        node_type=node_type,
        cost=cost,
        estimated_rows=estimated_rows,
        relation=relation,
        index_name=index_name,
        children=children or [],
        raw={},
    )


@pytest.fixture
def simple_root():
    child = make_node(
        node_type="Index Scan",
        cost="0.00..8.27",
        estimated_rows=1,
        relation="orders",
        index_name="orders_pkey",
    )
    return make_node(
        node_type="Nested Loop",
        cost="0.00..16.54",
        estimated_rows=10,
        children=[child],
    )


class TestCompactFormatter:
    def setup_method(self):
        self.fmt = CompactFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_root_node_type_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Nested Loop" in result

    def test_child_node_type_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Index Scan" in result

    def test_cost_shown(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "cost=" in result

    def test_rows_shown(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "rows=" in result

    def test_relation_shown(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "on=orders" in result

    def test_index_name_shown(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "idx=orders_pkey" in result

    def test_tree_connector_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "└─" in result or "├─" in result

    def test_single_node_no_connector(self):
        node = make_node(node_type="Seq Scan", cost="0.00..5.00", estimated_rows=50)
        result = self.fmt.format(node)
        assert "└─" not in result
        assert "Seq Scan" in result

    def test_multiple_children_connectors(self):
        children = [
            make_node(node_type="Seq Scan"),
            make_node(node_type="Hash"),
        ]
        root = make_node(node_type="Hash Join", children=children)
        result = self.fmt.format(root)
        assert "├─" in result
        assert "└─" in result

    def test_missing_optional_fields_omitted(self):
        node = make_node(node_type="Result")
        result = self.fmt.format(node)
        assert "cost=" not in result
        assert "rows=" not in result
        assert "on=" not in result
        assert "idx=" not in result
