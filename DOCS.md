# Documentation

## okf.validate(path)

Validates an OKF bundle against the v0.1 spec and extra requirements.

### okf.validate(path)

- Parameters:
  - `path`: path to the bundle root directory (string, default `"bundle"`)
- Returns: `list` of error strings. Empty list when the bundle is conformant.
- Prints: `🎉 OK! No errors found` to stdout when the bundle is clean.
- Errors:
  - Missing or empty `type` field in a concept document's frontmatter
  - Missing or empty `title` field in a concept document's frontmatter
  - Missing or empty `description` field in a concept document's frontmatter
- Notes:
  - Only `.md` files in the bundle root are inspected
  - Frontmatter must be delimited by `---` on its own line
  - The function is deterministic and has no external dependencies beyond the Python standard library
