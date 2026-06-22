import subprocess


def test_conformant_bundle_exits_zero():
    result = subprocess.run(
        ["python", "check_okf.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
