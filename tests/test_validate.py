import okf
from pathlib import Path

FIXTURES = Path(__file__).parent / "data"


def test_validate_reports_missing_type():
    errors = okf.validate(str(FIXTURES))
    assert isinstance(errors, list)
    assert len(errors) > 0
    assert "type" in errors[0].lower()
