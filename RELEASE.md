# Release checklist

## Release contract

- Package name on index: `oracle-sql-splitter`
- Import/package name: `oracle_sql_splitter`
- CLI entry point: `oracle-sql-splitter`
- Release version source: `pyproject.toml`

## Before the first release

- Confirm the PyPI package name is available: https://pypi.org/project/oracle-sql-splitter/
- Review package metadata in `pyproject.toml`
- Review `README.md` examples and CLI usage
- Push the repository to GitHub: `https://github.com/ob-server83/oracle-sql-splitter`
- Create accounts on PyPI and optionally TestPyPI
- Decide on one publish path:
  - Trusted publishing through GitHub Actions
  - Manual upload with a PyPI API token

## Local validation

Run this before every release:

```bash
python -m pip install --upgrade pip
python -m pip install -e .[dev]
pytest
python -m build
python -m twine check dist/*
```

Recommended smoke tests after building:

```bash
python -m pip install --force-reinstall dist/*.whl
oracle-sql-splitter --json smoke.sql
python -c "from oracle_sql_splitter import split_sql; print(split_sql('SELECT 1 FROM dual;'))"
```

## TestPyPI dry run

Optional, but useful for the first release:

```bash
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Then verify install from TestPyPI:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps oracle-sql-splitter
```

## Option A: Trusted publishing through GitHub Actions

This repository already includes `.github/workflows/publish.yml`.

1. In PyPI, open your account publishing settings or the project settings for `oracle-sql-splitter`.
2. Add a trusted publisher with:
   - Owner: `ob-server83`
   - Repository: `oracle-sql-splitter`
   - Workflow file: `publish.yml`
   - Environment: leave empty unless you explicitly use one
3. Commit and push your release changes.
4. Create a GitHub Release for the version tag.
5. The `Publish to PyPI` workflow will build and publish automatically.

Notes:
- Trusted publishing does not require storing a long-lived PyPI token in GitHub secrets.
- PyPI/TestPyPI won’t allow re-uploading the same version.

## Option B: Manual upload with an API token

Create an API token in PyPI, then authenticate with:

### PowerShell

```powershell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-..."
python -m twine upload dist/*
```

### CMD

```bat
set TWINE_USERNAME=__token__
set TWINE_PASSWORD=pypi-...
python -m twine upload dist/*
```

To upload to TestPyPI instead:

```bash
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

## Versioning

- Bump `version` in `pyproject.toml`
- Rebuild distributions after every version change
- Tag releases consistently in Git, for example `v0.1.0`
- Never upload the same version twice to PyPI or TestPyPI

## Suggested release sequence

1. Update `version` in `pyproject.toml`.
2. Clear old build artifacts if needed.
3. Run local validation.
4. Optionally publish to TestPyPI and test install.
5. Publish to PyPI.
6. Create or verify the Git tag/release notes.
7. Confirm the project page and install command work from PyPI.
