import tempfile
from pathlib import Path
from repro.checker import ReproChecker


def test_missing_env_spec():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "main.py").write_text("print('hello')")
        report = ReproChecker(tmp).run()
        severities = [i.severity for i in report.issues]
        assert "critical" in severities


def test_no_issues_when_env_spec_present():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "requirements.txt").write_text("numpy==1.24.0\nscipy==1.11.0\n")
        Path(tmp, "README.md").write_text("# My project")
        Path(tmp, "SETUP.md").write_text("# Setup")
        report = ReproChecker(tmp).run()
        critical = report.by_severity("critical")
        assert len(critical) == 0


def test_unpinned_packages():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "requirements.txt").write_text("numpy\nscipy\n")
        report = ReproChecker(tmp).run()
        high = report.by_severity("high")
        assert any("Unpinned" in i.message for i in high)


def test_score_decreases_with_issues():
    with tempfile.TemporaryDirectory() as tmp:
        report = ReproChecker(tmp).run()
        assert report.score < 100


def test_import_star_detected():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "analysis.py").write_text("from numpy import *\nimport os\n")
        report = ReproChecker(tmp).run()
        assert any("Wildcard" in i.message for i in report.issues)


def test_import_star_not_flagged_for_explicit_imports():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "analysis.py").write_text("from numpy import array, zeros\nimport os\n")
        report = ReproChecker(tmp).run()
        assert not any("Wildcard" in i.message for i in report.issues)


def test_no_git_history_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        report = ReproChecker(tmp).run()
        assert any("version controlled" in i.message for i in report.issues)


def test_git_history_present_not_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, ".git").mkdir()
        Path(tmp, "requirements.txt").write_text("numpy==1.24.0\n")
        Path(tmp, "README.md").write_text("# Project\nRequires Python 3.10+\n")
        Path(tmp, "SETUP.md").write_text("# Setup\n")
        report = ReproChecker(tmp).run()
        assert not any("version controlled" in i.message for i in report.issues)


def test_python_version_missing_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "README.md").write_text("# My project\nHow to run the code.\n")
        report = ReproChecker(tmp).run()
        assert any("Python version" in i.message for i in report.issues)


def test_python_version_present_not_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "README.md").write_text("# My project\nRequires Python 3.10+\n")
        Path(tmp, "requirements.txt").write_text("numpy==1.24.0\n")
        Path(tmp, "SETUP.md").write_text("# Setup\n")
        report = ReproChecker(tmp).run()
        assert not any("Python version" in i.message for i in report.issues)
