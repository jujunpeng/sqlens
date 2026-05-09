"""Tests for RadarFormatter."""

import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.radar import RadarFormatter
from sqlens.formatters import get_formatter


def make_node(
    node_type: str,
    cost: str = "0.00..10.00",
    rows: int = 100,
    children: list | None = None,
) -> PlanNode:
    return PlanNode(
        node_type=node_type,
        cost=cost,
        rows=rows,
        children=children or [],
        extra={},
    )


@pytest.fixture
def simple_root() -> PlanNode:
    child = make_node("Seq Scan", cost="0.00..5.00", rows=50)
    return make_node("Hash Join", cost="0.00..20.00", rows=200, children=[child])


class TestRadarFormatter:
    def setup_method(self):
        self.fmt = RadarFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_format_contains_header(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Radar View" in result

    def test_format_contains_node_type(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result
        assert "Seq Scan" in result

    def test_format_contains_rows_label(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "rows" in result

    def test_format_contains_cost_label(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "cost" in result

    def test_bar_scales_correctly(self):
        node = make_node("Index Scan", cost="0.00..5000.00", rows=10_000)
        result = self.fmt.format(node)
        # Full bar should appear for max values
        assert "####################" in result

    def test_zero_rows_renders(self):
        node = make_node("Result", cost="0.00..0.01", rows=0)
        result = self.fmt.format(node)
        assert "Result" in result
        assert "0" in result

    def test_get_formatter_returns_radar(self):
        fmt = get_formatter("radar")
        assert isinstance(fmt, RadarFormatter)

    def test_get_formatter_case_insensitive(self):
        fmt = get_formatter("RADAR")
        assert isinstance(fmt, RadarFormatter)

    def test_radar_in_list_formatters(self):
        from sqlens.formatters import list_formatters
        assert "radar" in list_formatters()
