## Conformance criteria

> High-level/user-facing specs moved to `specs/`:
> - `specs/error-output.spec.toml` — relative paths, determinism, message format
> - `specs/reserved-files.spec.toml` — reserved filename rules
> - `specs/concept-fields.spec.toml` — word count limits, field type checks

### 1. File discovery

Only the following files are part of the OKF bundle and subject to
validation:

- Root `index.md` (reserved directory listing).
- Root `log.md` (reserved change log).
- Every `.md` file under `bundle/` (concept documents).

Skip the `raw/` directory entirely (extra requirement) — nothing
inside it is checked. Silently ignore all other files at the repo
root: `README.md`, `AGENTS.md`, `DOCS.md`, `CHANGELOG.md`, `TODO.md`,
and any non-`.md` files everywhere.

### 2. Reserved filenames

> Spec defined in `specs/reserved-files.spec.toml`

`index.md` and `log.md` rules (frontmatter restriction, ISO 8601 headings,
bold prefix warnings). Implement per the spec criteria.

### 3. Concept documents

Every `.md` file under `bundle/` is a concept document. Files at the
repo root (except `index.md` and `log.md`) are not concepts.

**3a. Frontmatter parsing**

Every concept document MUST contain a parseable YAML frontmatter block
delimited by `---` on its own line at the start of the file and a
closing `---` on its own line. If the block is absent or unparseable,
that is an error.

**3b. Field word count limits (extra requirement)**

> Spec defined in `specs/concept-fields.spec.toml`

`title` ≤ 10 words, `description` ≤ 20 words. Implement per the spec criteria.

**3c. Filename convention (extra requirement)**

Every concept document filename MUST match the pattern:

    <digits>[<letter>].<digits>[<letter>]....<digits>[<letter>].md

Where each segment is one or more digits optionally followed by a single
letter. One segment is the minimum. Examples: `1a.2b.1a.md`, `3a.md`,
`2.md`, `3a.3.md`.

Reserved files (`index.md`, `log.md`) and all repo-root project files
(`README.md`, `AGENTS.md`, `DOCS.md`, `CHANGELOG.md`, `TODO.md`) are
exempt from this requirement.

### 4. Cross-link resolution (extra requirement)

The spec says consumers MUST tolerate broken links. This checker
elevates that to an error.

Parse every markdown link in every concept document body (both inline
`[text](url)` and reference-style `[text][ref]` forms). For each link:

- If the URL starts with `/`, resolve it relative to the bundle root.
- If the URL is a relative path (no leading `/`), resolve it relative
  to the containing file's directory.
- If the URL is an absolute URL (`https://...`, `http://...`), skip it
  (external references are not checked).
- If the URL contains a fragment (`#section`), strip the fragment before
  resolving.
- If the resolved target is a `.md` file that does not exist in the
  bundle, that is an error.
- If the resolved target is a directory, that is an error (links should
  point to files, not directories).

Links in reserved files (`index.md`, `log.md`) are NOT checked for
resolution — those files link to concepts, not the other way around.

### 5. Prose style (extra requirements)

These rules apply to the body of every concept document, excluding
frontmatter, headings, code blocks (fenced and indented), and tables.

**5a. One sentence per line**

Every prose line in the body MUST be a single complete sentence ending
in `.`, `?`, or `!`. A line with multiple sentences or a sentence split
across multiple lines is an error.

Exempted line types:
- Blank lines.
- Lines starting with `#` (headings).
- Fenced code blocks (delimited by ```` ``` ```` or ```` ~~~ ````).
- Indented code blocks (four spaces or one tab).
- Table rows (lines containing `|`).
- List items that are not complete sentences (e.g. `- Item name`).
- Frontmatter (already handled separately).

**5b. Sentence length limit**

Every prose sentence (line) MUST be 25 words or shorter. A sentence
exceeding 25 words is an error.

**5c. File word count limit**

The total word count of each concept document (excluding frontmatter)
MUST be 200 words or shorter. A file exceeding 200 words is an error.

Reserved files (`index.md`, `log.md`) and all repo-root project files
(`README.md`, `AGENTS.md`, `DOCS.md`, `CHANGELOG.md`, `TODO.md`) are
exempt from all three prose style rules.

### 6. Edge cases

| Situation | Handling |
|-----------|----------|
| `.md` file with only frontmatter and no body | Passes (body is optional). |
| `.md` file with only body and no frontmatter | Error. |
| Symlinks to `.md` files under `bundle/` | Followed and validated. |
| `.md` file in `raw/` | Skipped entirely. |
| Non-`.md` file anywhere | Ignored (no error, no warning). |
| Broken link to non-`.md` target | Error (link target must exist as a `.md` file). |
| Repo-root project file (`README.md`, etc.) | Silently skipped (not a concept). |

## Implementation plan

```
okf/validate.py
└── validate(path)  ✅  # entry point + basic frontmatter + required fields
    ├── discover_files(root)      # walk tree, skip raw/, return file list  ❌
    ├── validate_concepts(files)  # frontmatter + required fields ✅ / filename ❌
    ├── validate_reserved(files)  # spec/s/reserved-files.spec.toml  ❌
    ├── validate_links(files)     # cross-link resolution (concepts only)  ❌
    ├── validate_prose(files)     # sentence-per-line, ≤25 words, ≤200 total  ❌
    └── return errors             # caller prints success if empty ✅ / error.md spec ❌
```

High-level specs now live in `specs/`:
- `specs/reserved-files.spec.toml` — reserved filename rules
- `specs/concept-fields.spec.toml` — word count limits, field type checks
- `specs/error-output.spec.toml` — relative paths, determinism, message format

---

## Naming utility: `next_child_filename(parent, bundle_path="bundle")`

### Location
New module `okf/naming.py`.

### Signature
```python
def next_child_filename(parent: str, bundle_path: str = "bundle") -> str
```

Returns a bare filename with `.md` extension, e.g. `"1a.md"`. No directory prefix.

### Algorithm

1. **Parse last segment**: `parent.split('.')[-1]`
2. **Branch** on last segment type:
   - **All digits** (e.g. `"1"`) → child candidate = `parent + "a"` (bijective base-26 suffix starting at `"a"`)
   - **Digits + letter** (e.g. `"1a"`) → child candidate = `parent + ".1"` (numeric suffix starting at `1`)
3. **Collision resolution**: scan `bundle_path` for existing `*.md` filenames once, then increment the appended suffix (letter sequence or numeric sequence) until a gap is found. Both sequences are infinite — a gap always exists.
4. **Input assumptions**: parent is already OKF-conformant; no validation. Non-conformant input is caller's responsibility.

### Rules of thumb
- The parent acts as a fixed prefix; only the appended suffix (letter or numeric) is incremented on collision.
- Multi-letter suffixes (`aa`, `ab`, ...) and multi-digit numbers (`10`, `11`, ...) are produced as needed.
- The `AGENTS.md` spec currently says one trailing letter per segment — that description will need updating to reflect the broader convention.

[spec]: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
