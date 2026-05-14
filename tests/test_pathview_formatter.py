"""Tests for PathViewFormatter."""

import pytest
from sqlens.formatters.pathview import PathViewFormatter
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
    child = make_node("Seq Scan", cost="0.00..8.00", rows=40)
    return make_node("Hash Join", cost="8.00..25.00", rows=80, children=[child])


@pytest.fixture
def branching_root():
    left = make_node("Seq Scan", rows=10)
    right = make_node("Index Scan", rows=5)
    return make_node("Merge Join", rows=15, children=[left, right])


class TestPathViewFormatter:
    def setup_method(self):
        self.fmt = PathViewFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_format_contains_header(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Execution Paths" in result

    def test_single_path_label(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Path 1:" in result
        assert "Path 2:" not in result

    def test_path_contains_root_and_leaf(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result
        assert "Seq Scan" in result

    def test_branching_produces_two_paths(self, branching_root):
        result = self.fmt.format(branching_root)
        assert "Path 1:" in result
        assert "Path 2:" in result

    def test_branching_left_path(self, branching_root):
        result = self.fmt.format(branching_root)
        assert "Seq Scan" in result

    def test_branching_right_path(self, branching_root):
        result = self.fmt.format(branching_root)
        assert "Index Scan" in result

    def test_cost_shown_in_label(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "[" in result

    def test_rows_shown_in_label(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "rows" in result

    def test_leaf_only_node(self):
        leaf = make_node("Seq Scan", rows=5)
        result = self.fmt.format(leaf)
        assert "Path 1:" in result
        assert "Seq Scan" in result

    def test_empty_children_no_crash(self):
        root = make_node("Result")
        result = self.fmt.format(root)
        assert "Result" in result
