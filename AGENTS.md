# Agents

## Repo identity

This is an OKF v0.1 conformant knowledge bundle and a personal LLM Wiki.
Concept documents live under `bundle/`.  Root-level `.md` files (README,
AGENTS, DOCS, CHANGELOG, TODO) are project infrastructure, not concepts.
The `raw/` directory holds source documents and is exempt from all checks.

## Concept document rules

| Rule | Constraint |
|------|-----------|
| Frontmatter | Parseable YAML delimited by `---`. |
| Required fields | `type` (non-empty string), `title` (≤10 words), `description` (≤20 words). |
| Optional fields | `resource`, `tags`, `timestamp` — no format validation. |
| Body prose | One sentence per line. Each sentence ≤25 words. Total ≤200 words. |
| Filename | Pattern `xy.xy...xy.md` where each segment is digits plus optional trailing letter. |

## Cross-links

Every markdown link in a concept body must resolve to an existing `.md`
file in the bundle.  Broken links are errors.  External URLs are skipped.
Links in `index.md` and `log.md` are not checked.

## Reserved files

- `index.md` — no frontmatter.  Root `index.md` may contain only
  `okf_version` in its frontmatter.
- `log.md` — date headings must be ISO 8601 (`YYYY-MM-DD`).
  Warn on bold prefixes outside the conventional set.

## Planned tooling

`check_okf.py` — deterministic Python script, standard library only.
Validates the bundle against the SPEC and extra requirements above.
Usage: `python check_okf.py [bundle_root]`.

## Commit style

Prefix every commit with a gitmoji followed by an imperative verb.
First line under 72 characters.  Blank line then body.

## Current focus

The Gold is implementing `check_okf.py`.
