import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters import get_formatter
from sqlens.formatters.tree import TreeFormatter
from sqlens.formatters.summary import SummaryFormatter


def make_node(
    node_type: str,
    children: list[PlanNode] | None = None,
    **extra,
) -> PlanNode:
    return PlanNode(node_type=node_type, children=children or [], extra=extra)


class TestGetFormatter:
    def test_returns_tree_formatter(self):
        fmt = get_formatter("tree")
        assert isinstance(fmt, TreeFormatter)

    def test_returns_summary_formatter(self):
        fmt = get_formatter("summary")
        assert isinstance(fmt, SummaryFormatter)

    def test_default_is_tree(self):
        fmt = get_formatter()
        assert isinstance(fmt, TreeFormatter)

    def test_none_is_tree(self):
        fmt = get_formatter(None)
        assert isinstance(fmt, TreeFormatter)

    def test_unknown_style_raises(self):
        with pytest.raises(ValueError, match="Unknown formatter style"):
            get_formatter("json")

    def test_case_insensitive(self):
        assert isinstance(get_formatter("Tree"), TreeFormatter)
        assert isinstance(get_formatter("SUMMARY"), SummaryFormatter)


class TestTreeFormatter:
    def setup_method(self):
        self.fmt = TreeFormatter()

    def test_format_single_node(self):
        node = make_node("Seq Scan", **{"Relation Name": "users"})
        result = self.fmt.format(node)
        assert "Seq Scan" in result

    def test_format_nested_nodes(self):
        child = make_node("Index Scan")
        root = make_node("Nested Loop", children=[child])
        result = self.fmt.format(root)
        assert "Nested Loop" in result
        assert "Index Scan" in result

    def test_format_returns_string(self):
        node = make_node("Hash Join")
        assert isinstance(self.fmt.format(node), str)

    def test_child_indented_relative_to_parent(self):
        child = make_node("Seq Scan")
        root = make_node("Hash Join", children=[child])
        result = self.fmt.format(root)
        lines = result.splitlines()
        root_line = next(l for l in lines if "Hash Join" in l)
        child_line = next(l for l in lines if "Seq Scan" in l)
        root_indent = len(root_line) - len(root_line.lstrip())
        child_indent = len(child_line) - len(child_line.lstrip())
        assert child_indent > root_indent
