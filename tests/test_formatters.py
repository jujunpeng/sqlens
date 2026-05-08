import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters import get_formatter, list_formatters
from sqlens.formatters.tree import TreeFormatter
from sqlens.formatters.summary import SummaryFormatter
from sqlens.formatters.json_fmt import JsonFormatter
from sqlens.formatters.heatmap import HeatmapFormatter


def make_node(node_type, cost=None, rows=None, children=None):
    return PlanNode(
        node_type=node_type,
        cost=cost,
        rows=rows,
        extra={},
        children=children or [],
    )


class TestGetFormatter:
    def test_returns_tree_formatter(self):
        f = get_formatter("tree")
        assert isinstance(f, TreeFormatter)

    def test_returns_summary_formatter(self):
        f = get_formatter("summary")
        assert isinstance(f, SummaryFormatter)

    def test_returns_json_formatter(self):
        f = get_formatter("json")
        assert isinstance(f, JsonFormatter)

    def test_returns_heatmap_formatter(self):
        f = get_formatter("heatmap")
        assert isinstance(f, HeatmapFormatter)

    def test_case_insensitive(self):
        f = get_formatter("TREE")
        assert isinstance(f, TreeFormatter)

    def test_unknown_formatter_raises(self):
        with pytest.raises(ValueError, match="Unknown formatter"):
            get_formatter("nonexistent")

    def test_error_message_lists_available(self):
        with pytest.raises(ValueError, match="tree"):
            get_formatter("bogus")


class TestListFormatters:
    def test_returns_list(self):
        result = list_formatters()
        assert isinstance(result, list)

    def test_contains_tree(self):
        assert "tree" in list_formatters()

    def test_contains_heatmap(self):
        assert "heatmap" in list_formatters()

    def test_is_sorted(self):
        result = list_formatters()
        assert result == sorted(result)

    def test_all_formatters_instantiable(self):
        node = make_node("Seq Scan", cost="0.00..10.00", rows=50)
        for name in list_formatters():
            if name == "diff":
                continue
            f = get_formatter(name)
            out = f.format(node)
            assert isinstance(out, str), f"{name} formatter did not return str"
