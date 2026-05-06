import tempfile
from pathlib import Path

from repro.checker import ReproChecker


def test_matlab_addpath_without_startup_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "run_sim.m").write_text("addpath('/usr/local/toolbox');\ndisp('hello');\n")
        report = ReproChecker(tmp).run()
        assert any(i.category == "MATLAB" and "addpath" in i.message for i in report.issues)


def test_matlab_addpath_with_startup_not_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "run_sim.m").write_text("addpath('/usr/local/toolbox');\n")
        Path(tmp, "startup.m").write_text("addpath('/usr/local/toolbox');\n")
        report = ReproChecker(tmp).run()
        assert not any("addpath" in i.message for i in report.issues)


def test_matlab_version_missing_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "analysis.m").write_text("disp('hello');\n")
        Path(tmp, "README.md").write_text("# My project\nHow to run.\n")
        report = ReproChecker(tmp).run()
        assert any("MATLAB version" in i.message for i in report.issues)


def test_matlab_version_present_not_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "analysis.m").write_text("disp('hello');\n")
        Path(tmp, "README.md").write_text("# My project\nTested with MATLAB R2023b.\n")
        report = ReproChecker(tmp).run()
        assert not any("MATLAB version" in i.message for i in report.issues)


def test_matlab_hardcoded_path_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "solver.m").write_text("load('/home/alice/data.mat');\n")
        report = ReproChecker(tmp).run()
        assert any(i.category == "MATLAB" and "Hardcoded" in i.message for i in report.issues)


def test_matlab_random_seed_missing_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "monte_carlo.m").write_text("x = rand(100, 1);\ndisp(mean(x));\n")
        report = ReproChecker(tmp).run()
        assert any("rng" in i.fix for i in report.issues)


def test_matlab_random_seed_present_not_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "monte_carlo.m").write_text("rng(42);\nx = rand(100, 1);\n")
        report = ReproChecker(tmp).run()
        assert not any("rng" in i.fix for i in report.issues)


def test_no_matlab_files_no_matlab_issues():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "analysis.py").write_text("print('hello')\n")
        report = ReproChecker(tmp).run()
        assert not any(i.category == "MATLAB" for i in report.issues)


def test_python_random_seed_missing_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "simulate.py").write_text("import numpy as np\nx = np.random.rand(100)\n")
        report = ReproChecker(tmp).run()
        assert any(i.category == "Reproducibility" and "seed" in i.message.lower() for i in report.issues)


def test_python_random_seed_present_not_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "simulate.py").write_text(
            "import numpy as np\nnp.random.seed(42)\nx = np.random.rand(100)\n"
        )
        report = ReproChecker(tmp).run()
        assert not any(i.category == "Reproducibility" for i in report.issues)
