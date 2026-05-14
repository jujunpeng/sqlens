"""Tests for TreeListFormatter."""

import pytest
from sqlens.formatters.treelist import TreeListFormatter
from sqlens.parsers.base import PlanNode


def make_node(node_type, cost=None, rows=None, children=None, **extra):
    return PlanNode(
        node_type=node_type,
        cost=cost,
        rows=rows,
        children=children or [],
        extra=extra,
    )


@pytest.fixture
def simple_root():
    child = make_node("Seq Scan", cost="0.00..10.00", rows=50, relation="users")
    return make_node("Hash Join", cost="10.00..30.00", rows=100, children=[child])


class TestTreeListFormatter:
    def setup_method(self):
        self.fmt = TreeListFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_format_contains_header(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Plan Node List" in result

    def test_format_contains_root_node(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result

    def test_format_contains_child_node(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Seq Scan" in result

    def test_format_numbers_nodes(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "1." in result
        assert "2." in result

    def test_child_is_indented(self, simple_root):
        lines = self.fmt.format(simple_root).splitlines()
        root_line = next(l for l in lines if "Hash Join" in l)
        child_line = next(l for l in lines if "Seq Scan" in l)
        assert len(child_line) - len(child_line.lstrip()) > len(
            root_line
        ) - len(root_line.lstrip())

    def test_relation_in_label(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "users" in result

    def test_cost_in_label(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "cost=" in result

    def test_rows_in_label(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "rows=" in result

    def test_leaf_node_no_children(self):
        leaf = make_node("Index Scan", cost="0.00..5.00", rows=1)
        result = self.fmt.format(leaf)
        assert "1." in result
        assert "Index Scan" in result

    def test_deep_nesting(self):
        grandchild = make_node("Seq Scan", rows=10)
        child = make_node("Sort", rows=20, children=[grandchild])
        root = make_node("Aggregate", rows=1, children=[child])
        result = self.fmt.format(root)
        assert "1." in result
        assert "2." in result
        assert "3." in result
        assert "Aggregate" in result
        assert "Sort" in result
        assert "Seq Scan" in result
