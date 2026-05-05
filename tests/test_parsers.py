"""Tests for PostgreSQL and MySQL plan parsers."""

import json
import pytest

from sqlens.parsers.base import PlanNode
from sqlens.parsers.postgres import PostgresPlanParser
from sqlens.parsers.mysql import MySQLPlanParser


PG_PLAN_JSON = json.dumps([
    {
        "Plan": {
            "Node Type": "Hash Join",
            "Join Type": "Inner",
            "Startup Cost": 10.5,
            "Total Cost": 120.0,
            "Plan Rows": 500,
            "Plan Width": 32,
            "Plans": [
                {
                    "Node Type": "Seq Scan",
                    "Relation Name": "orders",
                    "Startup Cost": 0.0,
                    "Total Cost": 45.0,
                    "Plan Rows": 1000,
                    "Plan Width": 16,
                    "Plans": [],
                },
                {
                    "Node Type": "Hash",
                    "Startup Cost": 5.0,
                    "Total Cost": 30.0,
                    "Plan Rows": 200,
                    "Plan Width": 8,
                    "Plans": [],
                },
            ],
        }
    }
])

MYSQL_PLAN_JSON = json.dumps({
    "query_block": {
        "select_id": 1,
        "table": {
            "table_name": "users",
            "access_type": "ref",
            "key": "idx_email",
            "key_length": "102",
            "rows_examined_per_scan": 1,
            "filtered": "100.00",
            "cost_info": {"read_cost": "1.00", "query_cost": "1.20"},
        },
    }
})


class TestPostgresPlanParser:
    def setup_method(self):
        self.parser = PostgresPlanParser()

    def test_dialect(self):
        assert self.parser.dialect == "postgres"

    def test_parse_returns_plan_node(self):
        root = self.parser.parse(PG_PLAN_JSON)
        assert isinstance(root, PlanNode)

    def test_root_node_type(self):
        root = self.parser.parse(PG_PLAN_JSON)
        assert root.node_type == "Hash Join"

    def test_children_count(self):
        root = self.parser.parse(PG_PLAN_JSON)
        assert len(root.children) == 2

    def test_leaf_relation(self):
        root = self.parser.parse(PG_PLAN_JSON)
        seq_scan = root.children[0]
        assert seq_scan.relation == "orders"
        assert seq_scan.is_leaf()

    def test_total_nodes(self):
        root = self.parser.parse(PG_PLAN_JSON)
        assert root.total_nodes() == 3

    def test_cost_calculation(self):
        root = self.parser.parse(PG_PLAN_JSON)
        assert root.cost == pytest.approx(120.0 - 10.5)

    def test_parse_accepts_dict(self):
        data = json.loads(PG_PLAN_JSON)
        root = self.parser.parse(data)
        assert root.node_type == "Hash Join"


class TestMySQLPlanParser:
    def setup_method(self):
        self.parser = MySQLPlanParser()

    def test_dialect(self):
        assert self.parser.dialect == "mysql"

    def test_parse_returns_plan_node(self):
        root = self.parser.parse(MYSQL_PLAN_JSON)
        assert isinstance(root, PlanNode)

    def test_node_type_uppercased(self):
        root = self.parser.parse(MYSQL_PLAN_JSON)
        assert root.node_type == "REF"

    def test_relation_name(self):
        root = self.parser.parse(MYSQL_PLAN_JSON)
        assert root.relation == "users"

    def test_index_name(self):
        root = self.parser.parse(MYSQL_PLAN_JSON)
        assert root.index_name == "idx_email"

    def test_cost_parsed(self):
        root = self.parser.parse(MYSQL_PLAN_JSON)
        assert root.cost == pytest.approx(1.20)

    def test_no_children_for_single_table(self):
        root = self.parser.parse(MYSQL_PLAN_JSON)
        assert root.is_leaf()
