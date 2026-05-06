import subprocess
import sys
from importlib.resources import files
from pathlib import Path

from .checker import ReproReport


class ReproFixer:
    def __init__(self, root: Path, report: ReproReport):
        self.root = root
        self.report = report
        self.generated: list[str] = []

    def run(self) -> list[str]:
        needs_env = any(
            "No environment specification" in i.message for i in self.report.issues
        )
        needs_setup = any(
            "setup/install" in i.message.lower() for i in self.report.issues
        )

        if needs_env:
            self._generate_requirements()
            self._generate_environment_yml()
        if needs_setup:
            self._generate_setup_md()

        return self.generated

    def _generate_requirements(self):
        dest = self.root / "requirements.txt"
        if dest.exists():
            return
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            dest.write_text(result.stdout)
            self.generated.append("requirements.txt")

    def _generate_environment_yml(self):
        dest = self.root / "environment.yml"
        if dest.exists():
            return
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        template = (
            files("repro.templates").joinpath("environment.yml").read_text()
        )
        dest.write_text(template.replace("{python_version}", python_version))
        self.generated.append("environment.yml")

    def _generate_setup_md(self):
        dest = self.root / "SETUP.md"
        if dest.exists():
            return
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        template = (
            files("repro.templates").joinpath("SETUP.md").read_text()
        )
        dest.write_text(template.replace("{python_version}", python_version))
        self.generated.append("SETUP.md")
