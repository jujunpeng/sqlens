"""Tests for WaterfallFormatter."""

from __future__ import annotations

import pytest

from sqlens.parsers.base import PlanNode
from sqlens.formatters.waterfall import WaterfallFormatter
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
    child = make_node("Seq Scan", cost="0.00..8.00", rows=200, relation="items")
    return make_node("Merge Join", cost="8.00..30.00", rows=80, children=[child])


class TestWaterfallFormatter:
    def setup_method(self) -> None:
        self.fmt = WaterfallFormatter()

    def test_format_returns_string(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_header_present(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "Waterfall" in result

    def test_root_node_present(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "Merge Join" in result

    def test_child_node_present(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "Seq Scan" in result

    def test_relation_present(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "items" in result

    def test_bar_chars_present(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "█" in result

    def test_single_node_no_error(self) -> None:
        node = make_node("Index Scan", cost="0.00..2.50", relation="users")
        result = self.fmt.format(node)
        assert "Index Scan" in result

    def test_zero_cost_node(self) -> None:
        node = make_node("Result", cost="0.00..0.00")
        result = self.fmt.format(node)
        assert "Result" in result

    def test_registered_in_list(self) -> None:
        assert "waterfall" in list_formatters()

    def test_get_formatter_returns_waterfall(self) -> None:
        fmt = get_formatter("waterfall")
        assert isinstance(fmt, WaterfallFormatter)

    def test_get_formatter_case_insensitive(self) -> None:
        fmt = get_formatter("Waterfall")
        assert isinstance(fmt, WaterfallFormatter)
