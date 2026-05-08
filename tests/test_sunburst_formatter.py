import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.sunburst import SunburstFormatter


def make_node(
    node_type: str,
    rows: int | None = None,
    cost: str | None = None,
    children: list[PlanNode] | None = None,
) -> PlanNode:
    return PlanNode(
        node_type=node_type,
        rows=rows,
        cost=cost,
        children=children or [],
        extra={},
    )


@pytest.fixture
def simple_root() -> PlanNode:
    child = make_node("Seq Scan", rows=50, cost="0.00..10.00")
    return make_node("Hash Join", rows=200, cost="10.00..30.00", children=[child])


class TestSunburstFormatter:
    def setup_method(self):
        self.fmt = SunburstFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_header_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Sunburst Plan View" in result

    def test_root_node_type_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result

    def test_child_node_type_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Seq Scan" in result

    def test_child_indented(self, simple_root):
        lines = self.fmt.format(simple_root).splitlines()
        root_line = next(l for l in lines if "Hash Join" in l)
        child_line = next(l for l in lines if "Seq Scan" in l)
        root_indent = len(root_line) - len(root_line.lstrip())
        child_indent = len(child_line) - len(child_line.lstrip())
        assert child_indent > root_indent

    def test_arc_bar_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "[" in result and "]" in result

    def test_rows_shown(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "rows=200" in result

    def test_cost_shown(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "cost=" in result

    def test_single_node_no_crash(self):
        node = make_node("Index Scan", rows=1, cost="0.00..1.00")
        result = self.fmt.format(node)
        assert "Index Scan" in result

    def test_zero_rows_no_crash(self):
        node = make_node("Seq Scan", rows=0)
        result = self.fmt.format(node)
        assert "Seq Scan" in result

    def test_none_rows_no_crash(self):
        node = make_node("Seq Scan", rows=None)
        result = self.fmt.format(node)
        assert "Seq Scan" in result
