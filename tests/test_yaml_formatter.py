"""Tests for YamlFormatter."""
import pytest
from unittest.mock import patch
from sqlens.parsers.base import PlanNode
from sqlens.formatters.yaml_fmt import YamlFormatter


def make_node(node_type, cost=None, rows=None, extra=None, children=None):
    return PlanNode(
        node_type=node_type,
        cost=cost,
        rows=rows,
        extra=extra or {},
        children=children or [],
    )


@pytest.fixture
def simple_root():
    child = make_node("Seq Scan", cost="0.00..10.00", rows=100, extra={"table": "orders"})
    return make_node("Hash Join", cost="10.00..50.00", rows=200, children=[child])


class TestYamlFormatter:
    def setup_method(self):
        self.formatter = YamlFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.formatter.format(simple_root)
        assert isinstance(result, str)

    def test_output_contains_node_type(self, simple_root):
        result = self.formatter.format(simple_root)
        assert "Hash Join" in result

    def test_output_contains_child_node_type(self, simple_root):
        result = self.formatter.format(simple_root)
        assert "Seq Scan" in result

    def test_output_contains_cost(self, simple_root):
        result = self.formatter.format(simple_root)
        assert "cost" in result

    def test_output_contains_rows(self, simple_root):
        result = self.formatter.format(simple_root)
        assert "rows" in result

    def test_output_contains_extra_fields(self, simple_root):
        result = self.formatter.format(simple_root)
        assert "table" in result
        assert "orders" in result

    def test_leaf_node_no_children_key(self):
        node = make_node("Index Scan", cost="0.00..5.00", rows=1)
        result = self.formatter.format(node)
        assert "children" not in result

    def test_node_with_children_key(self, simple_root):
        result = self.formatter.format(simple_root)
        assert "children" in result

    def test_raises_without_pyyaml(self, simple_root):
        with patch("sqlens.formatters.yaml_fmt.HAS_YAML", False):
            with pytest.raises(RuntimeError, match="PyYAML is required"):
                self.formatter.format(simple_root)

    def test_valid_yaml_structure(self, simple_root):
        import yaml
        result = self.formatter.format(simple_root)
        parsed = yaml.safe_load(result)
        assert isinstance(parsed, dict)
        assert parsed["node_type"] == "Hash Join"
        assert len(parsed["children"]) == 1
        assert parsed["children"][0]["node_type"] == "Seq Scan"
