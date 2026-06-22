from pathlib import Path

_SUCCESS_MESSAGE = "🎉 OK! No errors found"
_REQUIRED_FIELDS = {
    "description": "Missing or empty description in {file}",
    "title": "Missing or empty title in {file}",
    "type": "Missing or empty type in {file}",
}


def validate(path="bundle"):
    errors = []
    bundle = Path(path)
    for md_file in sorted(bundle.glob("*.md")):
        text = md_file.read_text()
        frontmatter = _parse_frontmatter(text)
        for field, template in _REQUIRED_FIELDS.items():
            if field not in frontmatter or not frontmatter[field].strip():
                errors.append(template.format(file=md_file.name))
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
    frontmatter_lines = lines[1:end]
    result = {}
    for line in frontmatter_lines:
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result
