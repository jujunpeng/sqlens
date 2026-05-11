"""Tests for SequenceFormatter."""

from __future__ import annotations

import pytest

from sqlens.parsers.base import PlanNode
from sqlens.formatters.sequence import SequenceFormatter
from sqlens.formatters import get_formatter, list_formatters


def make_node(
    node_type: str,
    cost: str = "0.00..1.00",
    rows: int = 1,
    relation: str | None = None,
    children: list[PlanNode] | None = None,
) -> PlanNode:
    return PlanNode(
        node_type=node_type,
        cost=cost,
        rows=rows,
        relation=relation,
        children=children or [],
        extra={},
    )


@pytest.fixture()
def simple_root() -> PlanNode:
    child = make_node("Seq Scan", cost="0.00..5.00", rows=100, relation="orders")
    return make_node("Hash Join", cost="5.00..20.00", rows=50, children=[child])


class TestSequenceFormatter:
    def setup_method(self) -> None:
        self.fmt = SequenceFormatter()

    def test_format_returns_string(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_header_present(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "Sequence Diagram" in result

    def test_root_node_labelled(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result

    def test_child_node_labelled(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "Seq Scan" in result

    def test_relation_in_output(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "orders" in result

    def test_arrow_present(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "->" in result

    def test_single_node(self) -> None:
        node = make_node("Index Scan", relation="users")
        result = self.fmt.format(node)
        assert "Index Scan" in result
        assert "root" in result

    def test_rows_shown(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "rows=" in result

    def test_cost_shown(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "cost=" in result

    def test_registered_in_list(self) -> None:
        assert "sequence" in list_formatters()

    def test_get_formatter_returns_sequence(self) -> None:
        fmt = get_formatter("sequence")
        assert isinstance(fmt, SequenceFormatter)

    def test_get_formatter_case_insensitive(self) -> None:
        fmt = get_formatter("Sequence")
        assert isinstance(fmt, SequenceFormatter)
