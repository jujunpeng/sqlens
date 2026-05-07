import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.table import TableFormatter


def make_node(node_type, rows=100, cost="0.00..10.00", extra=None, children=None):
    return PlanNode(
        node_type=node_type,
        rows=rows,
        cost=cost,
        extra=extra or {},
        children=children or [],
    )


@pytest.fixture
def simple_root():
    child = make_node("Seq Scan", rows=50, cost="0.00..5.00", extra={"relation": "users"})
    return make_node("Hash Join", rows=100, cost="5.00..20.00", children=[child])


class TestTableFormatter:
    def setup_method(self):
        self.fmt = TableFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_contains_headers(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Node Type" in result
        assert "Rows" in result
        assert "Cost" in result
        assert "Depth" in result
        assert "Extra" in result

    def test_output_contains_node_types(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result
        assert "Seq Scan" in result

    def test_output_contains_relation(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "users" in result

    def test_separator_lines_present(self, simple_root):
        result = self.fmt.format(simple_root)
        lines = result.splitlines()
        sep_lines = [l for l in lines if l.startswith("+")]
        assert len(sep_lines) >= 3

    def test_single_node(self):
        node = make_node("Index Scan", rows=10, cost="0.00..1.00")
        result = self.fmt.format(node)
        assert "Index Scan" in result

    def test_depth_column_values(self, simple_root):
        result = self.fmt.format(simple_root)
        assert " 0 " in result
        assert " 1 " in result

    def test_empty_extra_when_no_relation(self):
        node = make_node("Sort", rows=200, cost="1.00..3.00")
        result = self.fmt.format(node)
        assert "Sort" in result

    def test_name_attribute(self):
        assert self.fmt.name == "table"

    def test_rows_formatted(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "100" in result
