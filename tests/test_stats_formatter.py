import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.stats import StatsFormatter
from sqlens.formatters import get_formatter


def make_node(node_type: str, cost: float = None, children=None) -> PlanNode:
    return PlanNode(
        node_type=node_type,
        cost=cost,
        rows=None,
        extra={},
        children=children or [],
    )


@pytest.fixture
def simple_root():
    child1 = make_node("Seq Scan", cost=10.5)
    child2 = make_node("Index Scan", cost=5.0)
    root = make_node("Hash Join", cost=20.0, children=[child1, child2])
    return root


class TestStatsFormatter:
    def setup_method(self):
        self.fmt = StatsFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_format_contains_total_nodes(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Total nodes" in result
        assert "3" in result

    def test_format_contains_node_types(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result
        assert "Seq Scan" in result
        assert "Index Scan" in result

    def test_format_contains_cost_section(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Cost" in result or "cost" in result

    def test_format_min_max_cost(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Min" in result
        assert "Max" in result

    def test_format_no_cost_nodes(self):
        root = make_node("Seq Scan", cost=None)
        result = self.fmt.format(root)
        assert "No cost data available" in result

    def test_format_single_node(self):
        root = make_node("Result", cost=1.0)
        result = self.fmt.format(root)
        assert "Total nodes" in result
        assert "1" in result

    def test_get_formatter_returns_stats(self):
        fmt = get_formatter("stats")
        assert isinstance(fmt, StatsFormatter)

    def test_percentage_shown(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "%" in result
