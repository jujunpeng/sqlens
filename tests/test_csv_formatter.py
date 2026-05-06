"""Tests for CsvFormatter."""

from __future__ import annotations

import csv
import io

import pytest

from sqlens.parsers.base import PlanNode
from sqlens.formatters.csv import CsvFormatter
from sqlens.formatters import get_formatter


def make_node(
    node_type: str = "Seq Scan",
    rows: int | None = 100,
    cost: str | None = "0.00..10.00",
    extra: dict | None = None,
    children: list | None = None,
) -> PlanNode:
    return PlanNode(
        node_type=node_type,
        rows=rows,
        cost=cost,
        extra=extra or {},
        children=children or [],
    )


@pytest.fixture()
def simple_root() -> PlanNode:
    child = make_node("Index Scan", rows=50, cost="0.00..5.00",
                      extra={"index_name": "users_pkey"})
    return make_node("Nested Loop", rows=200, cost="0.00..20.00", children=[child])


class TestCsvFormatter:
    def setup_method(self):
        self.fmt = CsvFormatter()

    def test_format_returns_string(self, simple_root):
        result = self.fmt.format(simple_root)
        assert isinstance(result, str)

    def test_output_has_header(self, simple_root):
        result = self.fmt.format(simple_root)
        first_line = result.splitlines()[0]
        assert "node_type" in first_line
        assert "depth" in first_line

    def test_row_count_matches_nodes(self, simple_root):
        result = self.fmt.format(simple_root)
        reader = csv.DictReader(io.StringIO(result))
        rows = list(reader)
        # root + 1 child
        assert len(rows) == 2

    def test_depth_values(self, simple_root):
        result = self.fmt.format(simple_root)
        reader = csv.DictReader(io.StringIO(result))
        rows = list(reader)
        assert rows[0]["depth"] == "0"
        assert rows[1]["depth"] == "1"

    def test_cost_split(self, simple_root):
        result = self.fmt.format(simple_root)
        reader = csv.DictReader(io.StringIO(result))
        rows = list(reader)
        assert rows[0]["cost_start"] == "0.00"
        assert rows[0]["cost_total"] == "20.00"

    def test_extra_index_name(self, simple_root):
        result = self.fmt.format(simple_root)
        reader = csv.DictReader(io.StringIO(result))
        rows = list(reader)
        assert "users_pkey" in rows[1]["extra"]

    def test_node_with_no_cost(self):
        node = make_node(cost=None)
        result = self.fmt.format(node)
        reader = csv.DictReader(io.StringIO(result))
        row = list(reader)[0]
        assert row["cost_start"] == ""
        assert row["cost_total"] == ""

    def test_get_formatter_returns_csv(self):
        fmt = get_formatter("csv")
        assert isinstance(fmt, CsvFormatter)
