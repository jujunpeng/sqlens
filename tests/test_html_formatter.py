import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.html import HtmlFormatter
from sqlens.formatters import get_formatter


def make_node(
    node_type: str,
    cost: str = "0.00..10.00",
    rows: int = 100,
    children: list | None = None,
) -> PlanNode:
    return PlanNode(
        node_type=node_type,
        cost=cost,
        rows=rows,
        extra={},
        children=children or [],
    )


@pytest.fixture
def simple_root() -> PlanNode:
    child = make_node("Seq Scan", cost="0.00..5.00", rows=50)
    return make_node("Hash Join", cost="5.00..20.00", rows=200, children=[child])


class TestHtmlFormatter:
    def setup_method(self):
        self.fmt = HtmlFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_starts_with_doctype(self, simple_root):
        result = self.fmt.format(simple_root)
        assert result.startswith("<!DOCTYPE html>")

    def test_output_contains_node_type(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result
        assert "Seq Scan" in result

    def test_output_contains_cost(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "5.00..20.00" in result

    def test_output_contains_rows(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "200" in result

    def test_leaf_node_has_leaf_class(self, simple_root):
        result = self.fmt.format(simple_root)
        assert 'class="leaf"' in result

    def test_non_leaf_has_details_open(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "<details open>" in result

    def test_single_node_plan(self):
        node = make_node("Seq Scan")
        result = self.fmt.format(node)
        assert "Seq Scan" in result
        assert "<!DOCTYPE html>" in result

    def test_get_formatter_returns_html_formatter(self):
        fmt = get_formatter("html")
        assert isinstance(fmt, HtmlFormatter)
