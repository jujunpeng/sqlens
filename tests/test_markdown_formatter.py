import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.markdown import MarkdownFormatter
from sqlens.formatters import get_formatter


def make_node(
    node_type="Seq Scan",
    relation=None,
    index_name=None,
    startup_cost=0.0,
    total_cost=10.0,
    rows=100,
    width=8,
    actual_rows=None,
    actual_time=None,
    children=None,
):
    return PlanNode(
        node_type=node_type,
        relation=relation,
        index_name=index_name,
        startup_cost=startup_cost,
        total_cost=total_cost,
        rows=rows,
        width=width,
        actual_rows=actual_rows,
        actual_time=actual_time,
        children=children or [],
    )


@pytest.fixture
def simple_root():
    child = make_node(node_type="Seq Scan", relation="orders", rows=50)
    return make_node(
        node_type="Hash Join",
        startup_cost=1.0,
        total_cost=42.5,
        rows=100,
        children=[child],
    )


class TestMarkdownFormatter:
    def setup_method(self):
        self.fmt = MarkdownFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_starts_with_heading(self, simple_root):
        result = self.fmt.format(simple_root)
        assert result.startswith("# Query Execution Plan")

    def test_root_node_type_in_output(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result

    def test_child_node_type_in_output(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Seq Scan" in result

    def test_relation_in_output(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "orders" in result

    def test_cost_in_output(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Cost" in result
        assert "42.5" in result

    def test_rows_in_output(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Rows" in result

    def test_actual_time_shown_when_present(self):
        node = make_node(actual_time=3.14159)
        result = self.fmt.format(node)
        assert "3.142" in result

    def test_get_formatter_returns_markdown(self):
        fmt = get_formatter("markdown")
        assert isinstance(fmt, MarkdownFormatter)
