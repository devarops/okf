from pathlib import Path

_SUCCESS_MESSAGE = "🎉 OK! No errors found"


def validate(path="bundle"):
    errors = []
    bundle = Path(path)
    for md_file in sorted(bundle.glob("*.md")):
        text = md_file.read_text()
        frontmatter = _parse_frontmatter(text)
        if "type" not in frontmatter:
            errors.append(f"Missing type in {md_file.name}")
        if "title" not in frontmatter:
            errors.append(f"Missing title in {md_file.name}")
    if not errors:
        print(_SUCCESS_MESSAGE)
    return errors


def _parse_frontmatter(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}
    end = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        return {}
    front = lines[1:end]
    result = {}
    for line in front:
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result
