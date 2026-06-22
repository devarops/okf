# Documentation

## check_okf.py

Validates an OKF bundle against the v0.1 spec and extra requirements.

### check_okf [bundle_root]

- Parameters:
  - `bundle_root`: path to the bundle directory (default `.`)
- Returns: exit code 0 if conformant, 1 if not
- Errors:
  - Missing or unparseable YAML frontmatter on a concept document
  - Missing or empty `type`, `title`, or `description` fields
  - Title longer than 10 words
  - Description longer than 20 words
  - Filename not matching the `xy.xy...xy.md` pattern
  - Broken cross-link in a concept body
  - Sentence split across multiple lines
  - Sentence exceeding 25 words
  - File exceeding 200 words (excluding frontmatter)
  - `index.md` with frontmatter (except root `okf_version`)
  - `log.md` with non-ISO-8601 date headings
- Notes:
  - Only validates files under `bundle/` and root `index.md` / `log.md`
  - Skips `raw/` directory entirely
  - Ignores all non-`.md` files
  - Root-level project files (README.md, AGENTS.md, etc.) are exempt
  - All output goes to stdout with `ERROR:` or `WARN:` prefixes
  - The script is deterministic with no external dependencies
