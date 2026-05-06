import pytest

from sqlens.parsers.base import PlanNode
from sqlens.formatters.flamegraph import FlamegraphFormatter
from sqlens.formatters import get_formatter


def make_node(
    node_type: str,
    estimated_rows: float = 100.0,
    actual_rows: float | None = None,
    estimated_cost: float = 10.0,
    children: list[PlanNode] | None = None,
) -> PlanNode:
    return PlanNode(
        node_type=node_type,
        estimated_rows=estimated_rows,
        actual_rows=actual_rows,
        estimated_cost=estimated_cost,
        extra={},
        children=children or [],
    )


@pytest.fixture()
 def simple_root() -> PlanNode:
    child = make_node("Seq Scan", estimated_rows=50, actual_rows=48, estimated_cost=5.0)
    return make_node(
        "Hash Join",
        estimated_rows=200,
        actual_rows=195,
        estimated_cost=25.0,
        children=[child],
    )


class TestFlamegraphFormatter:
    def setup_method(self):
        self.fmt = FlamegraphFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_contains_header(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Flame Graph" in result

    def test_output_contains_node_types(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result
        assert "Seq Scan" in result

    def test_child_is_indented(self, simple_root):
        lines = self.fmt.format(simple_root).splitlines()
        parent_line = next(l for l in lines if "Hash Join" in l)
        child_line = next(l for l in lines if "Seq Scan" in l)
        parent_indent = len(parent_line) - len(parent_line.lstrip())
        child_indent = len(child_line) - len(child_line.lstrip())
        assert child_indent > parent_indent

    def test_bar_wider_for_more_rows(self, simple_root):
        lines = self.fmt.format(simple_root).splitlines()
        parent_line = next(l for l in lines if "Hash Join" in l)
        child_line = next(l for l in lines if "Seq Scan" in l)
        parent_bar = parent_line.count(FlamegraphFormatter.BAR_CHAR)
        child_bar = child_line.count(FlamegraphFormatter.BAR_CHAR)
        assert parent_bar >= child_bar

    def test_rows_label_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "rows=" in result

    def test_node_with_no_actual_rows_uses_estimated(self):
        node = make_node("Index Scan", estimated_rows=77, actual_rows=None)
        result = self.fmt.format(node)
        assert "77" in result

    def test_get_formatter_returns_flamegraph(self):
        fmt = get_formatter("flamegraph")
        assert isinstance(fmt, FlamegraphFormatter)
