import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.summary import SummaryFormatter
from sqlens.formatters import get_formatter


def make_node(
    node_type: str,
    children: list[PlanNode] | None = None,
    **extra,
) -> PlanNode:
    return PlanNode(node_type=node_type, children=children or [], extra=extra)


@pytest.fixture()
def simple_root() -> PlanNode:
    child = make_node(
        "Seq Scan",
        **{"Relation Name": "orders", "Total Cost": 120.5, "Plan Rows": 500},
    )
    return make_node(
        "Hash Join",
        children=[child],
        **{"Total Cost": 350.75, "Startup Cost": 0.0, "Plan Rows": 1000},
    )


class TestSummaryFormatter:
    def setup_method(self):
        self.fmt = SummaryFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_contains_root_node_type(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result

    def test_contains_total_nodes(self, simple_root):
        result = self.fmt.format(simple_root)
        # root + 1 child = 2
        assert "2" in result

    def test_contains_cost(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "350" in result or "350.75" in result

    def test_contains_estimated_rows(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "1000" in result

    def test_seq_scan_warning(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Sequential scan" in result
        assert "orders" in result

    def test_high_cost_warning(self):
        node = make_node("Index Scan", **{"Total Cost": 50_000.0})
        result = self.fmt.format(node)
        assert "High cost" in result

    def test_no_warnings_for_clean_plan(self):
        node = make_node("Index Scan", **{"Total Cost": 10.0})
        result = self.fmt.format(node)
        assert "Warnings" not in result

    def test_node_breakdown_lists_types(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result
        assert "Seq Scan" in result


class TestGetFormatterSummary:
    def test_get_summary_formatter(self):
        fmt = get_formatter("summary")
        assert isinstance(fmt, SummaryFormatter)

    def test_get_formatter_case_insensitive(self):
        fmt = get_formatter("Summary")
        assert isinstance(fmt, SummaryFormatter)
