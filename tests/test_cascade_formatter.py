"""Tests for CascadeFormatter."""

from __future__ import annotations

import pytest

from sqlens.formatters.cascade import CascadeFormatter
from sqlens.parsers.base import PlanNode


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
    child = make_node("Seq Scan", cost="0.00..4.10", rows=100)
    return make_node("Hash Join", cost="0.00..8.49", rows=50, children=[child])


class TestCascadeFormatter:
    def setup_method(self) -> None:
        self.fmt = CascadeFormatter()

    def test_format_returns_string(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_header_present(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "Cascade cost view" in result

    def test_root_node_type_present(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result

    def test_child_node_type_present(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "Seq Scan" in result

    def test_bar_characters_present(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "█" in result or "░" in result

    def test_cost_label_present(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "cost=" in result

    def test_rows_label_present(self, simple_root: PlanNode) -> None:
        result = self.fmt.format(simple_root)
        assert "rows=" in result

    def test_child_indented(self, simple_root: PlanNode) -> None:
        lines = self.fmt.format(simple_root).splitlines()
        seq_lines = [l for l in lines if "Seq Scan" in l]
        assert seq_lines, "Seq Scan line not found"
        assert seq_lines[0].startswith("  "), "child should be indented"

    def test_zero_cost_node(self) -> None:
        node = make_node("Result", cost="", rows=1)
        result = self.fmt.format(node)
        assert "Result" in result
        assert "░" * 36 in result

    def test_single_node_full_bar(self) -> None:
        node = make_node("Index Scan", cost="0.00..10.00", rows=5)
        result = self.fmt.format(node)
        assert "█" * 36 in result

    def test_multiline_output(self, simple_root: PlanNode) -> None:
        lines = [l for l in self.fmt.format(simple_root).splitlines() if l.strip()]
        assert len(lines) >= 3
