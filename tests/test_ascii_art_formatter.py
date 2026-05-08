import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.ascii_art import AsciiArtFormatter


def make_node(node_type, relation=None, cost=None, rows=None, children=None):
    return PlanNode(
        node_type=node_type,
        relation=relation,
        cost=cost,
        rows=rows,
        children=children or [],
        extra={},
    )


@pytest.fixture
def simple_root():
    child = make_node("Index Scan", relation="orders", cost="0.00..8.00", rows=20)
    return make_node("Nested Loop", cost="8.00..25.00", rows=40, children=[child])


class TestAsciiArtFormatter:
    def setup_method(self):
        self.fmt = AsciiArtFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_contains_root_node_type(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Nested Loop" in result

    def test_contains_child_node_type(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Index Scan" in result

    def test_contains_relation(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "orders" in result

    def test_uses_box_drawing_chars(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "\u2514" in result or "\u251c" in result

    def test_single_node_no_pipe(self):
        node = make_node("Seq Scan", relation="items", cost="0.00..3.00", rows=5)
        result = self.fmt.format(node)
        assert "\u2502" not in result

    def test_multiple_children_indentation(self):
        c1 = make_node("Seq Scan", relation="a", rows=10)
        c2 = make_node("Seq Scan", relation="b", rows=20)
        root = make_node("Hash Join", children=[c1, c2])
        result = self.fmt.format(root)
        lines = result.splitlines()
        assert len(lines) == 3

    def test_cost_in_output(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "25.00" in result or "8.00" in result

    def test_rows_in_output(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "40" in result or "20" in result

    def test_deep_nesting(self):
        leaf = make_node("Seq Scan", relation="t", rows=1)
        mid = make_node("Sort", children=[leaf])
        root = make_node("Aggregate", children=[mid])
        result = self.fmt.format(root)
        assert "Seq Scan" in result
        assert "Sort" in result
        assert "Aggregate" in result
