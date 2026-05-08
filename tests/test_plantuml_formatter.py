import pytest
from sqlens.parsers.base import PlanNode
from sqlens.formatters.plantuml import PlantUMLFormatter


def make_node(node_type, relation=None, cost=None, rows=None, children=None):
    return PlanNode(
        node_type=node_type,
        relation=relation,
        cost=cost,
        rows=rows,
        children=children or [],
        extra={},
    )


@pytest.fixture
def simple_root():
    child = make_node("Seq Scan", relation="users", cost="0.00..10.00", rows=100)
    return make_node("Hash Join", cost="10.00..30.00", rows=50, children=[child])


class TestPlantUMLFormatter:
    def setup_method(self):
        self.fmt = PlantUMLFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_starts_with_startuml(self, simple_root):
        result = self.fmt.format(simple_root)
        assert result.startswith("@startuml")

    def test_ends_with_enduml(self, simple_root):
        result = self.fmt.format(simple_root)
        assert result.strip().endswith("@enduml")

    def test_contains_node_type(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Hash_Join" in result or "Hash Join" in result

    def test_contains_child_node(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "Seq_Scan" in result or "Seq Scan" in result

    def test_contains_relation(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "users" in result

    def test_contains_arrow_for_child(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "-->" in result

    def test_single_node_no_arrow(self):
        node = make_node("Seq Scan", relation="orders", cost="0.00..5.00", rows=10)
        result = self.fmt.format(node)
        assert "-->" not in result

    def test_contains_rectangle_keyword(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "rectangle" in result

    def test_skinparam_present(self, simple_root):
        result = self.fmt.format(simple_root)
        assert "skinparam" in result
