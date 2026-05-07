import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.outline import OutlineFormatter


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
        extra={},
        children=children or [],
    )


@pytest.fixture
def simple_root() -> PlanNode:
    child1 = make_node("Seq Scan", relation="orders", children=[])
    child2 = make_node("Index Scan", relation="customers", children=[])
    return make_node("Hash Join", children=[child1, child2])


class TestOutlineFormatter:
    def setup_method(self):
        self.fmt = OutlineFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_header_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Query Plan Outline" in result
        assert "==================" in result

    def test_root_section_number(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "1. Hash Join" in result

    def test_child_section_numbers(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "1.1. Seq Scan" in result
        assert "1.2. Index Scan" in result

    def test_relation_shown(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "on orders" in result
        assert "on customers" in result

    def test_cost_shown(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "cost=" in result

    def test_rows_shown(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "rows=" in result

    def test_single_node(self):
        node = make_node("Seq Scan", relation="users")
        result = self.fmt.format(node)
        assert "1. Seq Scan" in result
        assert "on users" in result

    def test_deep_nesting(self):
        leaf = make_node("Seq Scan")
        mid = make_node("Sort", children=[leaf])
        root = make_node("Limit", children=[mid])
        result = self.fmt.format(root)
        assert "1. Limit" in result
        assert "1.1. Sort" in result
        assert "1.1.1. Seq Scan" in result

    def test_name_attribute(self):
        assert self.fmt.name == "outline"
