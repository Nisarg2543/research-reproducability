import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List


@dataclass
class Issue:
    severity: str  # critical | high | medium | low
    category: str
    file: str
    message: str
    fix: str


@dataclass
class ReproReport:
    path: str
    issues: List[Issue] = field(default_factory=list)

    @property
    def score(self) -> int:
        deductions = {"critical": 25, "high": 15, "medium": 8, "low": 3}
        total = sum(deductions.get(i.severity, 0) for i in self.issues)
        return max(0, 100 - total)

    def by_severity(self, severity: str) -> List[Issue]:
        return [i for i in self.issues if i.severity == severity]


class ReproChecker:
    def __init__(self, path: str):
        self.root = Path(path).resolve()

    def run(self) -> ReproReport:
        report = ReproReport(path=str(self.root))
        self._check_env_spec(report)
        self._check_version_pins(report)
        self._check_hardcoded_paths(report)
        self._check_readme(report)
        self._check_setup_docs(report)
        self._check_data_references(report)
        self._check_import_star(report)
        self._check_git_history(report)
        self._check_python_version(report)
        self._check_python_random_seed(report)
        self._check_matlab_toolboxes(report)
        self._check_matlab_version(report)
        self._check_matlab_hardcoded_paths(report)
        self._check_matlab_random_seed(report)
        return report

    def _check_env_spec(self, report: ReproReport):
        has_req = (self.root / "requirements.txt").exists()
        has_conda = (self.root / "environment.yml").exists()
        has_pyproject = (self.root / "pyproject.toml").exists()
        if not any([has_req, has_conda, has_pyproject]):
            report.issues.append(Issue(
                severity="critical",
                category="Environment",
                file="/",
                message="No environment specification found (requirements.txt, environment.yml, or pyproject.toml)",
                fix="Run: pip freeze > requirements.txt  — or: conda env export > environment.yml",
            ))

    def _check_version_pins(self, report: ReproReport):
        req = self.root / "requirements.txt"
        if not req.exists():
            return
        unpinned = []
        for line in req.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "==" not in line and ">=" not in line:
                unpinned.append(line)
        if unpinned:
            report.issues.append(Issue(
                severity="high",
                category="Environment",
                file="requirements.txt",
                message=f"Unpinned packages: {', '.join(unpinned[:5])}{'...' if len(unpinned) > 5 else ''}",
                fix="Pin versions: pip freeze > requirements.txt",
            ))

    def _check_hardcoded_paths(self, report: ReproReport):
        patterns = [
            r'["\'](?:/home/|/Users/|C:\\\\Users\\\\|/root/)[^"\']+["\']',
            r'["\'][A-Z]:\\\\[^"\']+["\']',
        ]
        for py_file in self.root.rglob("*.py"):
            if ".git" in py_file.parts or "__pycache__" in py_file.parts:
                continue
            try:
                text = py_file.read_text(errors="ignore")
            except (PermissionError, OSError):
                continue
            for pattern in patterns:
                matches = re.findall(pattern, text)
                if matches:
                    report.issues.append(Issue(
                        severity="high",
                        category="Portability",
                        file=str(py_file.relative_to(self.root)),
                        message=f"Hardcoded absolute path: {matches[0]}",
                        fix="Replace with Path(__file__).parent / 'relative/path' or os.path.join(base_dir, ...)",
                    ))
                    break

    def _check_readme(self, report: ReproReport):
        has_readme = any(self.root.glob("README*"))
        if not has_readme:
            report.issues.append(Issue(
                severity="medium",
                category="Documentation",
                file="/",
                message="No README found",
                fix="Create README.md with: what the code does, how to set up the environment, how to run it",
            ))

    def _check_setup_docs(self, report: ReproReport):
        has_setup = any(self.root.glob("SETUP*")) or any(self.root.glob("INSTALL*"))
        if not has_setup:
            report.issues.append(Issue(
                severity="medium",
                category="Documentation",
                file="/",
                message="No setup/install documentation found",
                fix="Create SETUP.md with step-by-step environment setup instructions",
            ))

    def _check_data_references(self, report: ReproReport):
        """Warn if Python files reference data files but no data/ directory or .gitignore exclusion exists."""
        data_patterns = [r'pd\.read_csv', r'np\.load', r'open\(.*\.dat', r'open\(.*\.csv']
        found_data_refs = False
        for py_file in self.root.rglob("*.py"):
            if ".git" in py_file.parts:
                continue
            try:
                text = py_file.read_text(errors="ignore")
            except (PermissionError, OSError):
                continue
            if any(re.search(p, text) for p in data_patterns):
                found_data_refs = True
                break
        if found_data_refs and not (self.root / "data").exists():
            report.issues.append(Issue(
                severity="medium",
                category="Data",
                file="/",
                message="Code references data files but no data/ directory found",
                fix="Create a data/ directory and document where data comes from (download link, DOI, or included in repo)",
            ))

    def _check_import_star(self, report: ReproReport):
        for py_file in self.root.rglob("*.py"):
            if ".git" in py_file.parts or "__pycache__" in py_file.parts:
                continue
            try:
                text = py_file.read_text(errors="ignore")
            except (PermissionError, OSError):
                continue
            if re.search(r'^\s*from\s+\S+\s+import\s+\*', text, re.MULTILINE):
                report.issues.append(Issue(
                    severity="medium",
                    category="Code Quality",
                    file=str(py_file.relative_to(self.root)),
                    message="Wildcard import (from X import *) makes dependencies invisible and breaks across versions",
                    fix="Replace with explicit imports: from module import SpecificClass, specific_function",
                ))

    def _check_git_history(self, report: ReproReport):
        if not (self.root / ".git").exists():
            report.issues.append(Issue(
                severity="medium",
                category="Version Control",
                file="/",
                message="No git repository found — code changes are not version controlled",
                fix="Run: git init && git add . && git commit -m 'Initial commit'",
            ))

    def _check_python_version(self, report: ReproReport):
        readme_files = list(self.root.glob("README*"))
        if not readme_files:
            return
        text = readme_files[0].read_text(errors="ignore")
        if not re.search(r'[Pp]ython\s*3\.\d+|python_requires|py3\d', text):
            report.issues.append(Issue(
                severity="low",
                category="Documentation",
                file=readme_files[0].name,
                message="Python version not specified in README",
                fix="Add a line like 'Requires Python 3.10+' to the README",
            ))

    def _check_python_random_seed(self, report: ReproReport):
        for py_file in self.root.rglob("*.py"):
            if ".git" in py_file.parts or "__pycache__" in py_file.parts:
                continue
            try:
                text = py_file.read_text(errors="ignore")
            except (PermissionError, OSError):
                continue
            uses_random = re.search(r'np\.random\.|random\.random|random\.randint|torch\.rand', text)
            sets_seed = re.search(r'np\.random\.seed|np\.random\.default_rng|random\.seed|torch\.manual_seed', text)
            if uses_random and not sets_seed:
                report.issues.append(Issue(
                    severity="medium",
                    category="Reproducibility",
                    file=str(py_file.relative_to(self.root)),
                    message="Random operations without seed — statistical results not reproducible",
                    fix="Add np.random.seed(42) or use np.random.default_rng(42) at script start",
                ))
                break

    def _check_matlab_toolboxes(self, report: ReproReport):
        m_files = list(self.root.rglob("*.m"))
        if not m_files:
            return
        for m_file in m_files:
            try:
                text = m_file.read_text(errors="ignore")
            except (PermissionError, OSError):
                continue
            if re.search(r'\baddpath\s*\(', text):
                has_startup = (self.root / "startup.m").exists() or (self.root / "setup.m").exists()
                if not has_startup:
                    report.issues.append(Issue(
                        severity="high",
                        category="MATLAB",
                        file=str(m_file.relative_to(self.root)),
                        message="addpath() calls found but no startup.m to document required toolbox paths",
                        fix="Create startup.m listing all addpath() calls so anyone can reproduce the toolbox setup",
                    ))
                break

    def _check_matlab_version(self, report: ReproReport):
        m_files = list(self.root.rglob("*.m"))
        if not m_files:
            return
        readme_files = list(self.root.glob("README*"))
        if not readme_files:
            return
        try:
            text = readme_files[0].read_text(errors="ignore")
        except (PermissionError, OSError):
            return
        if not re.search(r'MATLAB\s*R?\d{4}[ab]?', text, re.IGNORECASE):
            report.issues.append(Issue(
                severity="medium",
                category="MATLAB",
                file=readme_files[0].name,
                message="MATLAB files found but MATLAB version not documented in README",
                fix="Add 'Tested with MATLAB R2023b' (or your version) to the README",
            ))

    def _check_matlab_hardcoded_paths(self, report: ReproReport):
        patterns = [
            r"'(?:/home/|/Users/|/root/)[^']*'",
            r"'[A-Z]:\\\\[^']*'",
        ]
        for m_file in self.root.rglob("*.m"):
            try:
                text = m_file.read_text(errors="ignore")
            except (PermissionError, OSError):
                continue
            for pattern in patterns:
                if re.search(pattern, text):
                    report.issues.append(Issue(
                        severity="high",
                        category="MATLAB",
                        file=str(m_file.relative_to(self.root)),
                        message="Hardcoded absolute path in MATLAB script",
                        fix="Use fileparts(mfilename('fullpath')) for paths relative to the script",
                    ))
                    break

    def _check_matlab_random_seed(self, report: ReproReport):
        for m_file in self.root.rglob("*.m"):
            try:
                text = m_file.read_text(errors="ignore")
            except (PermissionError, OSError):
                continue
            uses_random = re.search(r'\brand\b|\brandn\b|\brandperm\b', text)
            sets_seed = re.search(r'\brng\s*\(', text)
            if uses_random and not sets_seed:
                report.issues.append(Issue(
                    severity="medium",
                    category="MATLAB",
                    file=str(m_file.relative_to(self.root)),
                    message="Random number generation without rng() seed — results not reproducible",
                    fix="Add rng(42) at the top of the script and document the seed value",
                ))
                break
