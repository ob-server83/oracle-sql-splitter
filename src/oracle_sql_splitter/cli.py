from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .splitter import split_sql


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Split Oracle SQL/PLSQL scripts into executable statements.")
    parser.add_argument("path", nargs="?", help="Path to a .sql file")
    parser.add_argument("--stdin", action="store_true", help="Read SQL text from standard input")
    parser.add_argument("--json", action="store_true", help="Print the statements as a JSON array")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.stdin:
        sql_data = sys.stdin.read()
    elif args.path:
        sql_data = Path(args.path).read_text(encoding="utf-8")
    else:
        parser.error("provide a file path or use --stdin")

    statements = split_sql(sql_data)

    if args.json:
        json.dump(statements, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    for idx, statement in enumerate(statements, start=1):
        sys.stdout.write(f"-- statement {idx}\n")
        sys.stdout.write(statement)
        if not statement.endswith("\n"):
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
