import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.indent import IndentFormatter
from sqlens.formatters import get_formatter


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
    return make_node("Hash Join", cost="10.00..50.00", rows=200, children=[child])


class TestIndentFormatter:
    def setup_method(self):
        self.formatter = IndentFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.formatter.format(simple_root)
        assert isinstance(result, str)

    def test_root_node_present(self, simple_root):
        result = self.formatter.format(simple_root)
        assert "Hash Join" in result

    def test_child_node_present(self, simple_root):
        result = self.formatter.format(simple_root)
        assert "Seq Scan" in result

    def test_child_is_indented(self, simple_root):
        result = self.formatter.format(simple_root)
        lines = result.splitlines()
        seq_line = next(l for l in lines if "Seq Scan" in l)
        assert seq_line.startswith("  ")

    def test_root_not_indented(self, simple_root):
        result = self.formatter.format(simple_root)
        lines = result.splitlines()
        root_line = lines[0]
        assert not root_line.startswith(" ")

    def test_relation_shown(self, simple_root):
        result = self.formatter.format(simple_root)
        assert "users" in result

    def test_cost_shown(self, simple_root):
        result = self.formatter.format(simple_root)
        assert "cost=" in result

    def test_rows_shown(self, simple_root):
        result = self.formatter.format(simple_root)
        assert "rows=" in result

    def test_index_name_shown(self):
        node = make_node("Index Scan", extra={"Index Name": "idx_users_email"})
        result = self.formatter.format(node)
        assert "idx_users_email" in result

    def test_filter_shown(self):
        node = make_node("Seq Scan", extra={"Filter": "(active = true)"})
        result = self.formatter.format(node)
        assert "filter=" in result
        assert "active" in result

    def test_get_formatter_returns_indent(self):
        formatter = get_formatter("indent")
        assert isinstance(formatter, IndentFormatter)

    def test_leaf_node_no_children_lines(self):
        node = make_node("Result", rows=1)
        result = self.formatter.format(node)
        assert len(result.splitlines()) == 1
