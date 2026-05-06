import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.timeline import TimelineFormatter
from sqlens.formatters import get_formatter


def make_node(node_type, total_cost, startup_cost=0.0, rows=1, children=None):
    return PlanNode(
        node_type=node_type,
        total_cost=total_cost,
        startup_cost=startup_cost,
        plan_rows=rows,
        children=children or [],
        extra={},
    )


@pytest.fixture
def simple_root():
    child = make_node("Index Scan", total_cost=10.5, rows=5)
    return make_node("Nested Loop", total_cost=55.0, rows=20, children=[child])


class TestTimelineFormatter:
    def setup_method(self):
        self.fmt = TimelineFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_contains_header(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Execution Timeline" in result

    def test_output_contains_node_types(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Nested Loop" in result
        assert "Index Scan" in result

    def test_output_contains_max_cost(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Max cost" in result

    def test_bar_present_for_nonzero_cost(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "█" in result

    def test_single_node_no_children(self):
        node = make_node("Seq Scan", total_cost=7.0)
        result = self.fmt.format(node)
        assert "Seq Scan" in result
        assert "Max cost" in result

    def test_zero_cost_node(self):
        node = make_node("Result", total_cost=0.0)
        result = self.fmt.format(node)
        assert "Result" in result

    def test_get_formatter_returns_timeline(self):
        fmt = get_formatter("timeline")
        assert isinstance(fmt, TimelineFormatter)

    def test_long_node_type_truncated(self):
        node = make_node("A" * 50, total_cost=5.0)
        result = self.fmt.format(node)
        # label is capped at 22 chars, output should still render
        assert "A" * 22 in result
