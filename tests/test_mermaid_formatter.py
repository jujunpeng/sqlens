import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.mermaid import MermaidFormatter
from sqlens.formatters import get_formatter


def make_node(
    node_type: str,
    relation: str | None = None,
    estimated_cost: float | None = None,
    actual_rows: int | None = None,
    children: list | None = None,
) -> PlanNode:
    return PlanNode(
        node_type=node_type,
        relation=relation,
        estimated_cost=estimated_cost,
        actual_rows=actual_rows,
        children=children or [],
        extra={},
    )


@pytest.fixture
def simple_root() -> PlanNode:
    child = make_node("Seq Scan", relation="orders", estimated_cost=42.0, actual_rows=100)
    return make_node("Hash Join", estimated_cost=120.5, children=[child])


class TestMermaidFormatter:
    def setup_method(self):
        self.fmt = MermaidFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_starts_with_flowchart(self, simple_root):
        result = self.fmt.format(simple_root)
        assert result.startswith("flowchart TD")

    def test_contains_node_types(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash Join" in result
        assert "Seq Scan" in result

    def test_contains_relation(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "orders" in result

    def test_contains_arrow(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "-->" in result

    def test_single_node_no_arrow(self):
        node = make_node("Result", estimated_cost=1.0)
        result = self.fmt.format(node)
        assert "-->" not in result

    def test_node_ids_are_unique(self, simple_root):
        result = self.fmt.format(simple_root)
        lines = result.splitlines()
        ids = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("N") and '["' in stripped:
                node_id = stripped.split('[')[0].strip()
                ids.append(node_id)
        assert len(ids) == len(set(ids))

    def test_get_formatter_returns_mermaid(self):
        formatter = get_formatter("mermaid")
        assert isinstance(formatter, MermaidFormatter)

    def test_cost_appears_in_label(self):
        node = make_node("Seq Scan", estimated_cost=99.9)
        result = self.fmt.format(node)
        assert "99.9" in result
