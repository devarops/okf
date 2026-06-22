import okf
from pathlib import Path

FIXTURES = Path(__file__).parent / "data"


def test_validate_reports_missing_type():
    errors = okf.validate(str(FIXTURES))
    assert isinstance(errors, list)
    assert len(errors) > 0
    assert "type" in errors[0].lower()


def test_validate_defaults_to_bundle():
    errors = okf.validate()
    assert isinstance(errors, list)


def test_validate_reports_missing_title():
    errors = okf.validate(str(FIXTURES))
    assert any("title" in err.lower() for err in errors)


def test_validate_reports_empty_type():
    errors = okf.validate(str(FIXTURES))
    assert any("type" in err.lower() and "empty" in err.lower() for err in errors)


def test_validate_prints_success_message_when_clean(capsys):
    okf.validate()
    captured = capsys.readouterr()
    assert "🎉 OK! No errors found" in captured.out
