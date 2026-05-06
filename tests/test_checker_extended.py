import tempfile
from pathlib import Path

from repro.checker import ReproChecker


def test_hardcoded_unix_path_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "run.py").write_text('data = open("/home/alice/data.csv")\n')
        report = ReproChecker(tmp).run()
        assert any(i.category == "Portability" for i in report.issues)


def test_hardcoded_windows_path_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "run.py").write_text('f = open("C:\\\\Users\\\\john\\\\data.csv")\n')
        report = ReproChecker(tmp).run()
        assert any(i.category == "Portability" for i in report.issues)


def test_hardcoded_path_in_comment_not_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        # Path appears only in a comment string — should not flag
        Path(tmp, "run.py").write_text("# See /home/user/README for instructions\nprint('ok')\n")
        report = ReproChecker(tmp).run()
        assert not any(i.category == "Portability" for i in report.issues)


def test_data_references_flagged_without_data_dir():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "analysis.py").write_text("import pandas as pd\ndf = pd.read_csv('results.csv')\n")
        report = ReproChecker(tmp).run()
        assert any(i.category == "Data" for i in report.issues)


def test_data_references_not_flagged_with_data_dir():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "analysis.py").write_text("import pandas as pd\ndf = pd.read_csv('data/results.csv')\n")
        Path(tmp, "data").mkdir()
        report = ReproChecker(tmp).run()
        assert not any(i.category == "Data" for i in report.issues)


def test_readme_absence_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        report = ReproChecker(tmp).run()
        assert any("README" in i.message for i in report.issues)


def test_install_md_satisfies_setup_docs():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "INSTALL.md").write_text("# Install\npip install .\n")
        report = ReproChecker(tmp).run()
        assert not any("setup/install" in i.message.lower() for i in report.issues)


def test_score_floor_at_zero():
    with tempfile.TemporaryDirectory() as tmp:
        # Add multiple .py files with hardcoded paths to pile up issues
        for i in range(10):
            Path(tmp, f"script{i}.py").write_text(f'f = open("/home/user/data{i}.csv")\n')
        report = ReproChecker(tmp).run()
        assert report.score >= 0


def test_score_100_clean_repo():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, ".git").mkdir()
        Path(tmp, "requirements.txt").write_text("numpy==1.24.0\nscipy==1.11.0\n")
        Path(tmp, "README.md").write_text("# Project\nRequires Python 3.10+\n")
        Path(tmp, "SETUP.md").write_text("# Setup\n")
        report = ReproChecker(tmp).run()
        assert report.score == 100
        assert len(report.issues) == 0
