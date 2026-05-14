"""Tests for NetworkFormatter."""

from __future__ import annotations

import pytest

from sqlens.parsers.base import PlanNode
from sqlens.formatters.network import NetworkFormatter


def make_node(
    node_type: str,
    cost: str = "0.00..1.00",
    rows: int = 1,
    children: list[PlanNode] | None = None,
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
    child = make_node("Seq Scan", cost="0.00..10.00", rows=500)
    return make_node("Hash Join", cost="10.00..30.00", rows=100, children=[child])


class TestNetworkFormatter:
    def setup_method(self) -> None:
        self.fmt = NetworkFormatter()

    def test_format_returns_string(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_contains_header(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "sqlens network format" in result

    def test_root_node_present(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "ROOT:" in result
        assert "Hash_Join" in result

    def test_edge_present(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "->" in result
        assert "Seq_Scan" in result

    def test_rows_annotated(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "rows=" in result

    def test_cost_annotated(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "cost=" in result

    def test_leaf_node_no_children_edges(self) -> None:
        root = make_node("Index Scan", rows=10)
        result = self.fmt.format(root)
        assert "->" not in result

    def test_multiple_children(self) -> None:
        left = make_node("Seq Scan", rows=200)
        right = make_node("Index Scan", rows=50)
        root = make_node("Merge Join", rows=80, children=[left, right])
        result = self.fmt.format(root)
        assert "Seq_Scan" in result
        assert "Index_Scan" in result
        assert result.count("->") == 2

    def test_node_ids_are_unique(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        # Hash_Join_0 and Seq_Scan_1 should appear
        assert "Hash_Join_0" in result
        assert "Seq_Scan_1" in result

    def test_deeply_nested(self) -> None:
        leaf = make_node("Seq Scan", rows=1000)
        mid = make_node("Sort", rows=1000, children=[leaf])
        root = make_node("Limit", rows=10, children=[mid])
        result = self.fmt.format(root)
        assert result.count("->") == 2
