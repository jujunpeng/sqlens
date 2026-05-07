import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.sparkline import SparklineFormatter
from sqlens.formatters import get_formatter


def make_node(
    node_type: str,
    rows: int = 100,
    cost: str = "0.00..10.00",
    children: list | None = None,
) -> PlanNode:
    return PlanNode(
        node_type=node_type,
        rows=rows,
        cost=cost,
        extra={},
        children=children or [],
    )


@pytest.fixture
def simple_root() -> PlanNode:
    child1 = make_node("Index Scan", rows=50)
    child2 = make_node("Seq Scan", rows=200)
    return make_node("Hash Join", rows=100, children=[child1, child2])


class TestSparklineFormatter:
    def setup_method(self):
        self.fmt = SparklineFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_contains_header(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Sparkline" in result

    def test_output_contains_node_types(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result
        assert "Index Scan" in result
        assert "Seq Scan" in result

    def test_output_contains_rows_label(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "rows" in result

    def test_output_contains_peak(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Peak:" in result

    def test_output_contains_node_count(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Nodes: 3" in result

    def test_single_node_no_children(self):
        node = make_node("Seq Scan", rows=500)
        result = self.fmt.format(node)
        assert "Seq Scan" in result
        assert "Nodes: 1" in result

    def test_zero_rows_handled(self):
        node = make_node("Result", rows=0)
        result = self.fmt.format(node)
        assert isinstance(result, str)
        assert "Result" in result

    def test_bar_brackets_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "[" in result and "]" in result

    def test_get_formatter_returns_sparkline(self):
        fmt = get_formatter("sparkline")
        assert isinstance(fmt, SparklineFormatter)
