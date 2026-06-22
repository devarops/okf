# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/).
This project adheres to [Semantic Versioning](https://semver.org/) with
0.y.z — increment the minor version for every release.

## [Unreleased]

### Added

- `okf` Python package with `okf.validate()` function for bundle validation
- Required field checks for `type`, `title`, and `description` in concept
  document frontmatter (presence and non-empty value)
- Success message printed to stdout when the bundle is clean
- `make validate` target to run validation from the command line
- `make check` target for linting (black, flake8, mypy)
- `make format` target for auto-formatting with black
- `make setup` target for clean install
- Test fixtures in `tests/data/` for non-conformant concept documents
- `pyproject.toml` with flit build configuration
- Dependencies: Dockerfile for CI (pytest, black, flake8, mypy, mutmut,
  pylint, pytest-cov)
- AGENTS.md with repo conventions, document rules, and workflow guidance
- DOCS.md with `okf.validate()` interface reference
- CHANGELOG.md following Keep a Changelog
- README describing the repo as an OKF v0.1 conformant personal knowledge
  wiki
