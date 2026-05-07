"""Tests for formatter registry."""
import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters import get_formatter, list_formatters
from sqlens.formatters.tree import TreeFormatter
from sqlens.formatters.summary import SummaryFormatter
from sqlens.formatters.json_fmt import JsonFormatter
from sqlens.formatters.yaml_fmt import YamlFormatter


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

    def test_returns_yaml_formatter(self):
        assert isinstance(get_formatter("yaml"), YamlFormatter)

    def test_case_insensitive(self):
        assert isinstance(get_formatter("YAML"), YamlFormatter)
        assert isinstance(get_formatter("Tree"), TreeFormatter)

    def test_raises_on_unknown_formatter(self):
        with pytest.raises(ValueError, match="Unknown formatter"):
            get_formatter("nonexistent")

    def test_error_message_lists_available(self):
        with pytest.raises(ValueError, match="yaml"):
            get_formatter("bogus")


class TestListFormatters:
    def test_returns_list(self):
        result = list_formatters()
        assert isinstance(result, list)

    def test_contains_expected_formatters(self):
        result = list_formatters()
        for name in ("tree", "summary", "json", "yaml", "dot", "markdown", "mermaid"):
            assert name in result

    def test_is_sorted(self):
        result = list_formatters()
        assert result == sorted(result)

    def test_yaml_included(self):
        assert "yaml" in list_formatters()
