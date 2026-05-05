"""Tests for the sqlens CLI."""

import json
import textwrap
from pathlib import Path

import pytest

from sqlens.cli import main


POSTGRES_PLAN = [
    {
        "Plan": {
            "Node Type": "Seq Scan",
            "Relation Name": "users",
            "Startup Cost": 0.0,
            "Total Cost": 12.5,
            "Plan Rows": 100,
            "Plan Width": 8,
            "Plans": [],
        }
    }
]

MYSQL_PLAN = {
    "query_block": {
        "select_id": 1,
        "table": {
            "table_name": "orders",
            "access_type": "ALL",
            "rows_examined_per_scan": 500,
        },
    }
}


class TestMainPostgres:
    def test_returns_zero_on_success(self, tmp_path: Path) -> None:
        plan_file = tmp_path / "plan.json"
        plan_file.write_text(json.dumps(POSTGRES_PLAN))
        assert main([str(plan_file), "--dialect", "postgres"]) == 0

    def test_output_contains_node_type(self, tmp_path: Path, capsys) -> None:
        plan_file = tmp_path / "plan.json"
        plan_file.write_text(json.dumps(POSTGRES_PLAN))
        main([str(plan_file), "--dialect", "postgres"])
        captured = capsys.readouterr()
        assert "Seq Scan" in captured.out

    def test_missing_file_returns_one(self) -> None:
        assert main(["nonexistent_file.json", "--dialect", "postgres"]) == 1

    def test_invalid_json_returns_one(self, tmp_path: Path) -> None:
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("not json at all")
        assert main([str(bad_file)]) == 1


class TestMainMySQL:
    def test_returns_zero_on_success(self, tmp_path: Path) -> None:
        plan_file = tmp_path / "plan.json"
        plan_file.write_text(json.dumps(MYSQL_PLAN))
        assert main([str(plan_file), "--dialect", "mysql"]) == 0

    def test_output_contains_table_name(self, tmp_path: Path, capsys) -> None:
        plan_file = tmp_path / "plan.json"
        plan_file.write_text(json.dumps(MYSQL_PLAN))
        main([str(plan_file), "--dialect", "mysql"])
        captured = capsys.readouterr()
        assert "orders" in captured.out


class TestMainFlags:
    def test_unknown_format_returns_one(self, tmp_path: Path) -> None:
        plan_file = tmp_path / "plan.json"
        plan_file.write_text(json.dumps(POSTGRES_PLAN))
        assert main([str(plan_file), "--format", "unknown_fmt"]) == 1

    def test_default_dialect_is_postgres(self, tmp_path: Path, capsys) -> None:
        plan_file = tmp_path / "plan.json"
        plan_file.write_text(json.dumps(POSTGRES_PLAN))
        result = main([str(plan_file)])
        assert result == 0
