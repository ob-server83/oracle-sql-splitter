import json
import subprocess
import sys
from pathlib import Path

from oracle_sql_splitter import SQLSplitter, split_sql


def test_split_regular_sql_statements():
    sql = "SELECT 1 FROM dual;\nSELECT 2 FROM dual;\n"
    assert split_sql(sql) == [
        "SELECT 1 FROM dual\n",
        "SELECT 2 FROM dual\n",
    ]


def test_keep_plsql_block_together_until_slash():
    sql = "BEGIN\n  NULL;\nEND;\n/\n"
    assert split_sql(sql) == ["BEGIN\n  NULL;\nEND;\n"]


def test_skip_common_sqlplus_directives():
    sql = "SET SERVEROUTPUT ON\nSELECT 1 FROM dual;\nSET DEFINE OFF\n"
    assert split_sql(sql) == ["SELECT 1 FROM dual\n"]


def test_comment_semicolon_does_not_split_statement():
    sql = "-- comment;\nSELECT 1 FROM dual;\n"
    assert split_sql(sql) == ["-- comment;\nSELECT 1 FROM dual\n"]


def test_alias_is_kept_for_backward_compatibility():
    sql = "SELECT 1 FROM dual;\n"
    assert SQLSplitter(sql) == split_sql(sql)


def test_cli_json_output(tmp_path: Path):
    sql_file = tmp_path / "demo.sql"
    sql_file.write_text("SELECT 1 FROM dual;\n", encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, "-m", "oracle_sql_splitter.cli", str(sql_file), "--json"],
        capture_output=True,
        text=True,
        check=True,
    )

    assert json.loads(completed.stdout) == ["SELECT 1 FROM dual\n"]
