import tempfile
from pathlib import Path

from click.testing import CliRunner

from repro.cli import main


def test_cli_version():
    result = CliRunner().invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0." in result.output


def test_cli_help():
    result = CliRunner().invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Audit" in result.output


def test_cli_nonexistent_path():
    result = CliRunner().invoke(main, ["--path", "/nonexistent/12345xyz"])
    assert result.exit_code == 1
    assert "does not exist" in result.output.lower()


def test_cli_file_path_rejected(tmp_path):
    f = tmp_path / "not_a_dir.txt"
    f.write_text("hello")
    result = CliRunner().invoke(main, ["--path", str(f)])
    assert result.exit_code == 1
    assert "directory" in result.output.lower()


def test_cli_default_path_runs():
    result = CliRunner().invoke(main, [])
    assert result.exit_code == 0
    assert "Score" in result.output


def test_cli_output_markdown(tmp_path):
    out = tmp_path / "report.md"
    result = CliRunner().invoke(main, ["--path", str(tmp_path), "--output", str(out)])
    assert result.exit_code == 0
    assert out.exists()
    assert "Score" in out.read_text()


def test_cli_output_json(tmp_path):
    out = tmp_path / "report.json"
    result = CliRunner().invoke(main, ["--path", str(tmp_path), "--output", str(out)])
    assert result.exit_code == 0
    assert out.exists()
    import json
    data = json.loads(out.read_text())
    assert "score" in data
    assert "issues" in data


def test_cli_fix_generates_files(tmp_path):
    result = CliRunner().invoke(main, ["--path", str(tmp_path), "--fix"])
    assert result.exit_code == 0
    # requirements.txt or SETUP.md should be generated
    generated = list(tmp_path.iterdir())
    assert len(generated) > 0


def test_cli_fix_idempotent(tmp_path):
    CliRunner().invoke(main, ["--path", str(tmp_path), "--fix"])
    result = CliRunner().invoke(main, ["--path", str(tmp_path), "--fix"])
    assert result.exit_code == 0
    assert "Nothing to fix" in result.output or "Generated" in result.output
