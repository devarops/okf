# LLM Wiki in the Open Knowledge Format

## Commit style

Prefix every commit with a gitmoji followed by an imperative verb.
First line under 72 characters.  Blank line then body.
TDD phases: `🛑 🧪` (Red), `✅ 🧪` (Green), `♻️` (Refactor).
Config/tooling: `🔧`, lint fix: `🚨`, goal update: `🎯`.

## Package structure

Validation logic lives in the `okf/` Python package (not a standalone script).
Entry point: `okf.validate(path="bundle")` — returns a list of error strings.
Prints `🎉 OK! No errors found` to stdout when the bundle is clean.
Required fields: `type`, `title`, `description` — checked for presence and
non-empty value via a lookup table in `okf/validate.py`.

## Test fixtures

Non-conformant concept documents go under `tests/data/`.
Each file tests one violation (e.g. missing type, empty value, missing title).
The fixture directory `tests/data/` is validated by most tests.

## Developer workflow

- `make setup` — clean build caches, install package in editable mode.
- `make tests` — run `pytest --verbose tests` inside the `okf_ci` Docker container.
- `docker exec okf_ci make tests` — run tests if container is already running.
- `make validate` — run `okf.validate()` on the default `bundle/` directory.
- `make check` — lint (black, flake8, mypy) across `okf/` and `tests/`.
- `make format` — auto-format with black.
- `make clean` — remove `tests/__pycache__` (root-owned from Docker runs).

---

## Repo identity

This is an OKF conformant personal LLM Wiki.
Read this: https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/refs/heads/main/okf/SPEC.md
Concept documents live under `bundle/`.
Root-level `.md` files (README, AGENTS, DOCS, CHANGELOG, TODO) are project infrastructure, not concepts.
The `raw/` directory holds source documents and is exempt from all checks.

## Concept document rules

| Rule | Constraint |
|------|-----------|
| Frontmatter | Parseable YAML delimited by `---`. |
| Required fields | `type` (non-empty string), `title` (≤10 words), `description` (≤20 words). |
| Optional fields | `resource` (A URI that uniquely identifies the underlying asset the concept describes), `tags` (YAML list of short strings for cross-cutting categorization), `timestamp` (ISO 8601 datetime of last meaningful change) |
| Body prose | One sentence per line. Each sentence ≤25 words. Total ≤200 words. |
| Filename | Pattern `xy.xy...xy.md` where each segment is a digit (`x`) plus optional trailing letter (`y`). For instance: `1a.2b.md`, `1a.3.md`, `4.md` |

## Cross-links

Every markdown link in a concept body must resolve to an existing `.md` file in the bundle.
Broken links are errors.
External URLs are skipped.
Links in `index.md` and `log.md` are not checked.

## Reserved files

- `index.md` — no frontmatter.  Root `index.md` may contain only
  `okf_version` in its frontmatter.
- `log.md` — date headings must be ISO 8601 (`YYYY-MM-DD`).
  Warn on bold prefixes outside the conventional set.
