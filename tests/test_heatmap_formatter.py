import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.heatmap import HeatmapFormatter


def make_node(node_type, cost=None, rows=None, children=None):
    return PlanNode(
        node_type=node_type,
        cost=cost,
        rows=rows,
        extra={},
        children=children or [],
    )


@pytest.fixture
def simple_root():
    child = make_node("Seq Scan", cost="0.00..10.00", rows=100)
    return make_node("Hash Join", cost="10.00..50.00", rows=500, children=[child])


class TestHeatmapFormatter:
    def setup_method(self):
        self.formatter = HeatmapFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.formatter.format(simple_root)
        assert isinstance(result, str)

    def test_output_contains_header(self, simple_root):
        result = self.formatter.format(simple_root)
        assert "Heatmap" in result

    def test_output_contains_node_types(self, simple_root):
        result = self.formatter.format(simple_root)
        assert "Hash Join" in result
        assert "Seq Scan" in result

    def test_output_contains_cost(self, simple_root):
        result = self.formatter.format(simple_root)
        assert "cost" in result

    def test_output_contains_rows(self, simple_root):
        result = self.formatter.format(simple_root)
        assert "rows" in result

    def test_heat_char_zero_rows(self):
        node = make_node("Seq Scan", rows=0)
        result = self.formatter.format(node)
        assert result is not None

    def test_heat_char_max_rows(self):
        node = make_node("Seq Scan", rows=10000)
        result = self.formatter.format(node)
        assert "█" in result

    def test_heat_char_none_rows(self):
        node = make_node("Seq Scan", rows=None)
        result = self.formatter.format(node)
        assert "rows=?" in result

    def test_child_indented(self, simple_root):
        lines = self.formatter.format(simple_root).splitlines()
        child_lines = [l for l in lines if "Seq Scan" in l]
        assert child_lines, "Expected Seq Scan line"
        assert child_lines[0].startswith("  ")

    def test_single_node_no_children(self):
        node = make_node("Index Scan", cost="0.00..5.00", rows=10)
        result = self.formatter.format(node)
        assert "Index Scan" in result
        assert "\n" in result
