import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.text import TextFormatter


def make_node(node_type, cost=None, rows=None, relation=None, extra=None, children=None):
    return PlanNode(
        node_type=node_type,
        cost=cost,
        rows=rows,
        relation=relation,
        extra=extra or {},
        children=children or [],
    )


@pytest.fixture
def simple_root():
    child = make_node("Seq Scan", cost="0.00..10.00", rows=100, relation="users")
    return make_node("Hash Join", cost="10.00..30.00", rows=50, children=[child])


class TestTextFormatter:
    def setup_method(self):
        self.fmt = TextFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_contains_header(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Query Execution Plan" in result

    def test_output_contains_root_node_type(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result

    def test_output_contains_child_node_type(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Seq Scan" in result

    def test_output_contains_relation(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "users" in result

    def test_output_contains_cost(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "cost=" in result

    def test_output_contains_rows(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "rows=" in result

    def test_child_is_indented(self, simple_root):
        lines = self.fmt.format(simple_root).splitlines()
        child_lines = [l for l in lines if "Seq Scan" in l]
        assert child_lines, "Expected a line with Seq Scan"
        assert child_lines[0].startswith("  "), "Child should be indented"

    def test_leaf_node_no_children(self):
        node = make_node("Index Scan", cost="0.00..5.00", rows=1, relation="orders")
        result = self.fmt.format(node)
        assert "Index Scan" in result
        assert "orders" in result

    def test_extra_fields_rendered(self):
        node = make_node("Sort", extra={"Sort Key": "id"})
        result = self.fmt.format(node)
        assert "Sort Key" in result
        assert "id" in result

    def test_separator_line_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "=" * 10 in result
