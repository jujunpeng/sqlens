import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.boxplot import BoxplotFormatter


def make_node(node_type, rows=None, cost=None, children=None):
    return PlanNode(
        node_type=node_type,
        rows=rows,
        cost=cost,
        extra={},
        children=children or [],
    )


@pytest.fixture
def simple_root():
    child1 = make_node("Seq Scan", rows=100, cost="0.00..10.00")
    child2 = make_node("Index Scan", rows=5, cost="0.00..2.50")
    root = make_node("Hash Join", rows=50, cost="10.00..30.00", children=[child1, child2])
    return root


class TestBoxplotFormatter:
    def setup_method(self):
        self.fmt = BoxplotFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_contains_header(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Box Plot" in result

    def test_output_contains_stats(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Min" in result
        assert "Max" in result
        assert "Median" in result
        assert "Mean" in result

    def test_output_contains_q1_q3(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Q1" in result
        assert "Q3" in result

    def test_node_count(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Nodes   : 3" in result

    def test_min_value(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Min     : 5" in result

    def test_max_value(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Max     : 100" in result

    def test_ascii_bar_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "=" in result
        assert "|" in result

    def test_no_rows_returns_fallback(self):
        node = make_node("Seq Scan", rows=None)
        result = self.fmt.format(node)
        assert "no row data" in result

    def test_single_node(self):
        node = make_node("Seq Scan", rows=42)
        result = self.fmt.format(node)
        assert "Nodes   : 1" in result
        assert "Min     : 42" in result
        assert "Max     : 42" in result

    def test_percentile_boundary(self):
        data = [1, 2, 3, 4, 5]
        assert self.fmt._percentile(data, 0) == 1
        assert self.fmt._percentile(data, 100) == 5
        assert self.fmt._percentile(data, 50) == 3
