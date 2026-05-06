# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.0] — 2025-05-06

### Added

**9 reproducibility checks:**
- Missing environment specification (`requirements.txt`, `environment.yml`, `pyproject.toml`) — Critical
- Unpinned package versions in `requirements.txt` — High
- Hardcoded absolute paths in Python files (`/home/`, `/Users/`, `C:\Users\`) — High
- Missing README — Medium
- Missing setup/install documentation — Medium
- Data file references without a `data/` directory — Medium
- Wildcard imports (`from X import *`) — Medium
- No git version control (`.git` directory absent) — Medium
- Python version not documented in README — Low

**CLI:**
- `repro-check --path <dir>` — audit any directory
- `repro-check --output <file>` — write Markdown or JSON report
- `repro-check --fix` — auto-generate `requirements.txt`, `environment.yml`, and `SETUP.md`
- `repro-check --version`

**Reporting:**
- Colour-coded terminal output with severity grouping
- Reproducibility score (0–100)
- Markdown export
- JSON export

**Packaging:**
- Installable via `pip install repro-check` and `pipx install repro-check`
- CI on Python 3.10, 3.11, 3.12, 3.13
- Automated PyPI publish on tagged release
