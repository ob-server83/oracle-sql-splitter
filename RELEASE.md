# Release checklist

## Before the first release

- Update author and GitHub URLs in `pyproject.toml`
- Confirm the PyPI package name is available
- Review `README.md` examples
- Push the repository to GitHub
- Create a PyPI project or prepare trusted publishing

## Local validation

```bash
python -m pip install -e .[dev]
pytest
python -m build
python -m twine check dist/*
```

## Publish options

### Option A: Trusted publishing through GitHub Actions

1. Create the package on PyPI, or set up the project for pending publisher configuration.
2. In PyPI project settings, add a trusted publisher:
   - Owner: your GitHub user or org
   - Repository: your repository name
   - Workflow: `publish.yml`
   - Environment: leave empty unless you use one
3. Create a GitHub release.
4. The `Publish to PyPI` workflow will build and publish automatically.

### Option B: Manual upload with an API token

```bash
python -m build
python -m twine upload dist/*
```

Set credentials with:

```bash
TWINE_USERNAME=__token__
TWINE_PASSWORD=<your-pypi-token>
```

## Versioning

- Bump `version` in `pyproject.toml`
- Rebuild distributions after every version change
- Never upload the same version twice to PyPI
