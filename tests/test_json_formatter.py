import json
import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.json_fmt import JsonFormatter
from sqlens.formatters import get_formatter


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
    child = make_node("Index Scan", cost=0.5, rows=10, extra={"index": "users_pkey"})
    return make_node("Nested Loop", cost=12.5, rows=100, children=[child])


class TestJsonFormatter:
    def setup_method(self):
        self.fmt = JsonFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_is_valid_json(self, simple_root):
        result = self.fmt.format(simple_root)
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    def test_root_node_type_present(self, simple_root):
        result = json.loads(self.fmt.format(simple_root))
        assert result["node_type"] == "Nested Loop"

    def test_cost_included_when_present(self, simple_root):
        result = json.loads(self.fmt.format(simple_root))
        assert result["cost"] == 12.5

    def test_rows_included_when_present(self, simple_root):
        result = json.loads(self.fmt.format(simple_root))
        assert result["rows"] == 100

    def test_children_are_nested(self, simple_root):
        result = json.loads(self.fmt.format(simple_root))
        assert len(result["children"]) == 1
        assert result["children"][0]["node_type"] == "Index Scan"

    def test_leaf_has_empty_children_list(self, simple_root):
        result = json.loads(self.fmt.format(simple_root))
        child = result["children"][0]
        assert child["children"] == []

    def test_extra_fields_preserved(self, simple_root):
        result = json.loads(self.fmt.format(simple_root))
        child = result["children"][0]
        assert child["extra"]["index"] == "users_pkey"

    def test_node_without_cost_omits_cost_key(self):
        node = make_node("Seq Scan")
        result = json.loads(self.fmt.format(node))
        assert "cost" not in result

    def test_get_formatter_returns_json_formatter(self):
        formatter = get_formatter("json")
        assert isinstance(formatter, JsonFormatter)
