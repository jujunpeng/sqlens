import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters import get_formatter, DEFAULT_FORMAT
from sqlens.formatters.tree import TreeFormatter
from sqlens.formatters.summary import SummaryFormatter
from sqlens.formatters.json_fmt import JsonFormatter


def make_node(node_type, cost=None, rows=None, extra=None, children=None):
    return PlanNode(
        node_type=node_type,
        cost=cost,
        rows=rows,
        extra=extra or {},
        children=children or [],
    )


class TestGetFormatter:
    def test_returns_tree_formatter(self):
        assert isinstance(get_formatter("tree"), TreeFormatter)

    def test_returns_summary_formatter(self):
        assert isinstance(get_formatter("summary"), SummaryFormatter)

    def test_returns_json_formatter(self):
        assert isinstance(get_formatter("json"), JsonFormatter)

    def test_default_is_tree(self):
        assert isinstance(get_formatter(), TreeFormatter)

    def test_default_format_constant(self):
        assert DEFAULT_FORMAT == "tree"

    def test_case_insensitive_tree(self):
        assert isinstance(get_formatter("Tree"), TreeFormatter)

    def test_case_insensitive_json(self):
        assert isinstance(get_formatter("JSON"), JsonFormatter)

    def test_unknown_format_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown format"):
            get_formatter("xml")

    def test_error_message_lists_choices(self):
        with pytest.raises(ValueError, match="tree"):
            get_formatter("bogus")

    def test_all_formatters_have_format_method(self):
        for name in ("tree", "summary", "json"):
            formatter = get_formatter(name)
            assert callable(getattr(formatter, "format", None))

    def test_formatter_format_accepts_plan_node(self):
        node = make_node("Seq Scan", cost=1.0, rows=5)
        for name in ("tree", "summary", "json"):
            formatter = get_formatter(name)
            result = formatter.format(node)
            assert isinstance(result, str)
