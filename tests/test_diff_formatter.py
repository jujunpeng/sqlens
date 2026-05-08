"""Tests for DiffFormatter."""
from __future__ import annotations

import pytest

from sqlens.formatters.diff import DiffFormatter
from sqlens.parsers.base import PlanNode


def make_node(
    node_type: str,
    cost: float | None = None,
    rows: int | None = None,
    children: list | None = None,
) -> PlanNode:
    return PlanNode(
        node_type=node_type,
        estimated_cost=cost,
        estimated_rows=rows,
        actual_rows=None,
        actual_time=None,
        extra={},
        children=children or [],
    )


@pytest.fixture()
 def simple_left() -> PlanNode:
    child = make_node("Seq Scan", cost=10.0, rows=100)
    return make_node("Hash Join", cost=50.0, rows=50, children=[child])


@pytest.fixture()
def simple_right() -> PlanNode:
    child = make_node("Index Scan", cost=5.0, rows=80)
    return make_node("Nested Loop", cost=30.0, rows=40, children=[child])


class TestDiffFormatter:
    def setup_method(self) -> None:
        self.fmt = DiffFormatter()

    def test_format_diff_returns_string(self, simple_left, simple_right):
        result = self.fmt.format_diff(simple_left, simple_right)
        assert isinstance(result, str)

    def test_format_diff_contains_left_node(self, simple_left, simple_right):
        result = self.fmt.format_diff(simple_left, simple_right)
        assert "Hash Join" in result

    def test_format_diff_contains_right_node(self, simple_left, simple_right):
        result = self.fmt.format_diff(simple_left, simple_right)
        assert "Nested Loop" in result

    def test_format_diff_shows_differences_count(self, simple_left, simple_right):
        result = self.fmt.format_diff(simple_left, simple_right)
        assert "Differences" in result

    def test_format_diff_identical_plans_zero_diff(self, simple_left):
        result = self.fmt.format_diff(simple_left, simple_left)
        assert "Differences    : 0" in result

    def test_format_diff_different_plans_nonzero_diff(self, simple_left, simple_right):
        result = self.fmt.format_diff(simple_left, simple_right)
        assert "Differences    : 2" in result

    def test_format_diff_missing_node_shown(self):
        left = make_node("Seq Scan", cost=10.0, rows=100)
        right = make_node(
            "Hash Join",
            cost=50.0,
            rows=50,
            children=[make_node("Seq Scan", cost=10.0, rows=100)],
        )
        result = self.fmt.format_diff(left, right)
        assert "<missing>" in result

    def test_format_raises_on_single_node(self, simple_left):
        with pytest.raises(NotImplementedError):
            self.fmt.format(simple_left)

    def test_format_diff_contains_nodes_compared(self, simple_left, simple_right):
        result = self.fmt.format_diff(simple_left, simple_right)
        assert "Nodes compared" in result
