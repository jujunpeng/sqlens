import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.treemap import TreemapFormatter


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
    child = make_node("Seq Scan", rows=40, relation="users")
    return make_node("Nested Loop", rows=60, children=[child])


class TestTreemapFormatter:
    def setup_method(self):
        self.fmt = TreemapFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_contains_header(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Treemap" in result

    def test_output_contains_root_node(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Nested Loop" in result

    def test_output_contains_child_node(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Seq Scan" in result

    def test_relation_included(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "users" in result

    def test_bar_character_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "#" in result

    def test_percentage_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "%" in result

    def test_zero_rows_no_crash(self):
        node = make_node("Result", rows=0)
        result = self.fmt.format(node)
        assert isinstance(result, str)

    def test_single_node(self):
        node = make_node("Seq Scan", rows=100)
        result = self.fmt.format(node)
        assert "100.0%" in result
