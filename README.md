# oracle-sql-splitter

Small Python library and CLI for splitting Oracle SQL and PL/SQL scripts into executable statements.

## Features

- Splits regular SQL statements terminated by `;`
- Keeps Oracle PL/SQL blocks together until a standalone `/`
- Skips common SQL*Plus directives such as `SET SERVEROUTPUT ON`
- Preserves comments and blank lines that belong to a statement
- Exposes both a Python API and a CLI
- Includes GitHub Actions for CI and PyPI publishing

## Install

```bash
pip install oracle-sql-splitter
```

## Python usage

```python
from oracle_sql_splitter import split_sql

sql = """
SET SERVEROUTPUT ON
CREATE TABLE demo (id NUMBER);
BEGIN
  NULL;
END;
/
"""

parts = split_sql(sql)
for part in parts:
    print("---")
    print(part)
```

## CLI usage

Split a file:

```bash
oracle-sql-splitter path/to/script.sql
```

Read from stdin:

```bash
type script.sql | oracle-sql-splitter --stdin
```

Print as JSON:

```bash
oracle-sql-splitter path/to/script.sql --json
```

## Development

```bash
python -m pip install -e .[dev]
pytest
python -m build
python -m twine check dist/*
```

## GitHub Actions

- `.github/workflows/ci.yml` runs tests and package build checks
- `.github/workflows/publish.yml` publishes to PyPI via trusted publishing on GitHub Releases

## Publish to PyPI

See `RELEASE.md` for the full release checklist.

Quick summary:

1. Confirm the package name `oracle-sql-splitter` is still available on PyPI, or rename it before the first release.
2. Bump `version` in `pyproject.toml`.
3. Build and validate distributions locally.
4. Publish to TestPyPI first if you want a dry run.
5. Publish to PyPI either manually with `twine` or by creating a GitHub release after configuring trusted publishing.
