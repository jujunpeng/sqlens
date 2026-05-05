import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters import get_formatter
from sqlens.formatters.tree import TreeFormatter


def make_node(node_type, relation=None, children=None, stats=None, extra=None):
    return PlanNode(
        node_type=node_type,
        relation=relation,
        children=children or [],
        stats=stats or {},
        extra=extra or {},
    )


class TestGetFormatter:
    def test_returns_tree_formatter(self):
        fmt = get_formatter("tree")
        assert isinstance(fmt, TreeFormatter)

    def test_default_is_tree(self):
        fmt = get_formatter()
        assert isinstance(fmt, TreeFormatter)

    def test_unknown_style_raises(self):
        with pytest.raises(ValueError, match="Unknown formatter style"):
            get_formatter("unknown")


class TestTreeFormatter:
    def setup_method(self):
        self.fmt = TreeFormatter()

    def test_single_node_no_children(self):
        node = make_node("Seq Scan", relation="users")
        result = self.fmt.format(node)
        assert "Seq Scan on users" in result

    def test_tree_with_children(self):
        child1 = make_node("Seq Scan", relation="orders")
        child2 = make_node("Index Scan", relation="users", extra={"index_name": "users_pkey"})
        root = make_node("Hash Join", children=[child1, child2])
        result = self.fmt.format(root)
        assert "Hash Join" in result
        assert "Seq Scan on orders" in result
        assert "Index Scan on users [users_pkey]" in result

    def test_stats_shown_in_output(self):
        node = make_node("Seq Scan", stats={"actual_rows": 42, "actual_time": 1.5})
        result = self.fmt.format(node)
        assert "rows=42" in result
        assert "time=1.5ms" in result

    def test_join_type_in_label(self):
        node = make_node("Nested Loop", extra={"join_type": "inner"})
        result = self.fmt.format(node)
        assert "(inner join)" in result

    def test_branch_connectors_present(self):
        child = make_node("Seq Scan")
        root = make_node("Aggregate", children=[child])
        result = self.fmt.format(root)
        assert "└──" in result

    def test_multiple_children_use_branch_and_last(self):
        children = [make_node(f"Scan {i}") for i in range(3)]
        root = make_node("Merge Join", children=children)
        result = self.fmt.format(root)
        assert "├──" in result
        assert "└──" in result
