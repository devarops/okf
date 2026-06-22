# OKF Conformance Checker — Plan

Write a deterministic Python script `check_okf.py` that validates this
repository against the [OKF v0.1 Spec][spec] plus a small set of extra
requirements that do not contradict it.

## How it runs

- Single file, zero dependencies beyond the Python standard library.
- Accepts one optional argument: the bundle root directory (defaults to `.`).
- Exits with code 0 if the bundle is conformant, 1 if not.
- Prints one line per issue found: `ERROR:` or `WARN:` prefix.
- All file paths are printed relative to the bundle root.
- The script MUST be deterministic: same input → same output every time.

## Conformance criteria

### 1. File discovery

Walk the bundle tree collecting every `.md` file. Skip the `raw/`
directory entirely (extra requirement) — nothing inside it is checked.
Silently ignore all non-`.md` files.

### 2. Reserved filenames

Two filenames are reserved and MUST NOT appear in the concept set:

| Filename | Rule |
|----------|------|
| `index.md` | No frontmatter. Exception: a root `index.md` MAY contain a frontmatter block with a single key `okf_version`. |
| `log.md` | Date headings MUST be valid ISO 8601 (`YYYY-MM-DD`). Warn if a log entry uses a bold prefix other than the conventional set (`**Update**`, `**Creation**`, `**Deprecation**`, `**Initialization**`). |

If a reserved file does not parse as valid markdown, that is an error.

### 3. Concept documents

Every `.md` file that is not a reserved filename is a concept document.
This includes `README.md` at the bundle root.

**3a. Frontmatter parsing**

Every concept document MUST contain a parseable YAML frontmatter block
delimited by `---` on its own line at the start of the file and a
closing `---` on its own line. If the block is absent or unparseable,
that is an error.

**3b. Required field**

The frontmatter MUST contain a `type` key with a non-empty string value.
If `type` is missing, empty, or not a string, that is an error.

**3c. Optional fields**

No optional field is validated for format or presence. `tags` may be any
YAML value; `timestamp` may be any YAML value; `resource` may be any
YAML value. Unknown keys are silently accepted. This matches the spec's
requirement that consumers MUST NOT reject bundles for missing optional
fields or unknown keys.

**3d. Filename convention (extra requirement)**

Every concept document filename MUST match the pattern:

    <digits>[<letter>].<digits>[<letter>]....<digits>[<letter>].md

Where each segment is one or more digits optionally followed by a single
letter. One segment is the minimum. Examples: `1a.2b.1a.md`, `3a.md`,
`2.md`, `3a.3.md`.

Reserved files (`index.md`, `log.md`) and `README.md` are exempt from
this requirement.

### 4. Cross-link resolution (extra requirement)

The spec says consumers MUST tolerate broken links. This checker
**elevates that to an error**.

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

Reserved files (`index.md`, `log.md`) and `README.md` are exempt from
all three prose style rules.

### 6. Edge cases

| Situation | Handling |
|-----------|----------|
| Empty bundle (no `.md` files) | Passes (vacuously conformant). |
| `.md` file with only frontmatter and no body | Passes (body is optional). |
| `.md` file with only body and no frontmatter | Error. |
| Frontmatter with `type: ""` (empty string) | Error. |
| Frontmatter with `type: 42` (not a string) | Error (must be non-empty string). |
| Symlinks to `.md` files | Followed and validated. |
| `.md` file in `raw/` | Skipped entirely. |
| Non-`.md` file anywhere outside `raw/` | Ignored (no error, no warning). |
| Broken link to non-`.md` target | Error (link target must exist as a `.md` file). |

## Implementation plan

```
check_okf.py
├── main()
│   ├── parse_args()              # bundle root, optional path
│   ├── discover_files(root)      # walk tree, skip raw/, return file list
│   ├── classify(files)           # split into reserved vs concept
│   ├── validate_reserved(files)  # index.md + log.md rules
│   ├── validate_concepts(files)  # frontmatter + type field + filename
│   ├── validate_links(files)     # cross-link resolution (concepts only)
│   ├── validate_prose(files)     # sentence-per-line, ≤25 words, ≤200 total
│   └── report(errors, warnings)  # print, exit 0/1
```

Each function is a pure function of its inputs (file tree on disk).
No randomness, no network, no external state.

[spec]: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
