from __future__ import annotations

import re
from typing import List

_DIRECTIVE_RE = re.compile(
    r"^\s*(?:SET\s+SERVEROUTPUT(?:\s+ON|\s+OFF)?|WHENEVER\s+SQLERROR\s+EXIT\s+FAILURE|SET\s+DEFINE\s+OFF)\b",
    re.IGNORECASE,
)
_BLOCK_START_RE = re.compile(r"^\s*(?:CREATE\s+OR\s+REPLACE|DECLARE|BEGIN)\b", re.IGNORECASE)
_COMMENT_WITH_SEMICOLON_RE = re.compile(r"^\s*--|^\s*\*.*;", re.IGNORECASE)


def _emit(buffer: list[str], statements: list[str]) -> None:
    statement = "\n".join(buffer).rstrip()
    if statement:
        statements.append(statement + "\n")
    buffer.clear()


def split_sql(sql_data: str) -> List[str]:
    """Split Oracle SQL/PLSQL text into executable statements.

    - Regular SQL is split on `;`
    - PL/SQL blocks are kept together until a standalone `/`
    - Common SQL*Plus directives are skipped

    """

    lines = sql_data.splitlines()
    statements: list[str] = []
    buffer: list[str] = []

    x = 0
    while x < len(lines):
        line = lines[x]
        stripped = line.strip()

        if _DIRECTIVE_RE.search(line):
            x += 1
            continue

        if _BLOCK_START_RE.search(line):
            while x < len(lines):
                block_line = lines[x]
                block_stripped = block_line.strip()
                if block_stripped == "/":
                    _emit(buffer, statements)
                    break
                buffer.append(block_line)
                x += 1
            x += 1
            continue

        if ";" in line and not _COMMENT_WITH_SEMICOLON_RE.search(line):
            before_semicolon, _sep, after_semicolon = line.partition(";")
            current_line = before_semicolon.rstrip()
            if current_line:
                buffer.append(current_line)
            _emit(buffer, statements)
            if after_semicolon.strip():
                buffer.append(after_semicolon)
            x += 1
            continue

        buffer.append(line)
        x += 1

    _emit(buffer, statements)
    return statements


SQLSplitter = split_sql
