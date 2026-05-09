import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.timeline_gantt import TimelineGanttFormatter


def make_node(
    node_type: str,
    cost: str = "0.00..10.00",
    rows: int = 100,
    relation: str | None = None,
    children: list | None = None,
) -> PlanNode:
    return PlanNode(
        node_type=node_type,
        cost=cost,
        rows=rows,
        relation=relation,
        children=children or [],
        extra={},
    )


@pytest.fixture
def simple_root() -> PlanNode:
    child = make_node("Seq Scan", cost="0.00..5.00", rows=50, relation="orders")
    return make_node("Hash Join", cost="5.00..20.00", rows=200, children=[child])


class TestTimelineGanttFormatter:
    def setup_method(self):
        self.fmt = TimelineGanttFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_contains_gantt_header(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Gantt" in result

    def test_output_contains_root_node_type(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result

    def test_output_contains_child_node_type(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Seq Scan" in result

    def test_output_contains_relation(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "orders" in result

    def test_bar_characters_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "=" in result

    def test_single_node_no_children(self):
        node = make_node("Index Scan", cost="0.00..8.00", rows=10)
        result = self.fmt.format(node)
        assert "Index Scan" in result
        assert "=" in result

    def test_empty_cost_handled_gracefully(self):
        node = make_node("Custom Scan", cost="", rows=0)
        result = self.fmt.format(node)
        assert isinstance(result, str)

    def test_zero_max_cost_no_crash(self):
        node = make_node("Result", cost="0.00..0.00", rows=1)
        result = self.fmt.format(node)
        assert isinstance(result, str)
