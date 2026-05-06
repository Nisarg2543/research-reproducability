# repro-check

**Audit any research codebase for reproducibility issues in seconds.**

[![CI](https://github.com/Nisarg2543/research-reproducability/actions/workflows/ci.yml/badge.svg)](https://github.com/Nisarg2543/research-reproducability/actions)
[![PyPI](https://img.shields.io/pypi/v/research-reproducability.svg)](https://pypi.org/project/research-reproducability/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://pypi.org/project/repro-check/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## The problem

A simulation that ran last year won't run today because a package changed.
A new PhD student can't reproduce results from a former student's thesis.
A collaborating lab can't run your code because their Python or MATLAB versions differ.

This is endemic to academic computing. Most labs have no one responsible for fixing it.

**repro-check** gives you a reproducibility score and a prioritised fix list in seconds.

---

## Install

```bash
pip install repro-check
# or
pipx install repro-check
```

Requires Python 3.10+.

---

## Quick start

```bash
# Audit the current directory
repro-check

# Audit a specific repo
repro-check --path /path/to/research/code

# Write a Markdown report
repro-check --path /path/to/code --output report.md

# Write a JSON report (for tooling / CI integration)
repro-check --path /path/to/code --output report.json

# Auto-generate missing environment files
repro-check --path /path/to/code --fix
```

### Example output

```
╭──────────────────────────────────────────╮
│ Reproducibility Audit                    │
│ Path: /home/alice/cfd-solver             │
│ Score: 52/100                            │
╰──────────────────────────────────────────╯

✗ CRITICAL (1)
  Environment — /
    No environment specification found
    Fix: Run: pip freeze > requirements.txt

⚠ HIGH (2)
  Environment — requirements.txt
    Unpinned packages: numpy, scipy, fenics
    Fix: Pin versions: pip freeze > requirements.txt
  Portability — solver/mesh.py
    Hardcoded absolute path: '/home/alice/data/mesh.msh'
    Fix: Replace with Path(__file__).parent / 'relative/path'

~ MEDIUM (3)
  Version Control — /
    No git repository found
    Fix: git init && git add . && git commit -m 'Initial commit'
  MATLAB — startup.m missing
    addpath() calls found but no startup.m to document toolbox paths
    Fix: Create startup.m listing all required toolbox paths
  Reproducibility — simulate.py
    Random operations without seed
    Fix: Add np.random.seed(42) at script start
```

---

## What it checks

| Check | Severity |
|---|---|
| No `requirements.txt` / `environment.yml` / `pyproject.toml` | Critical |
| Unpinned package versions | High |
| Hardcoded absolute paths (`/home/user/...`, `C:\Users\...`) | High |
| MATLAB `addpath()` without `startup.m` | High |
| Hardcoded paths in MATLAB `.m` files | High |
| No README | Medium |
| No setup/install documentation | Medium |
| Data file references but no `data/` directory | Medium |
| Wildcard imports (`from X import *`) | Medium |
| No git version control | Medium |
| MATLAB version not documented | Medium |
| Unseeded random operations (Python: numpy/random/torch) | Medium |
| Unseeded random operations (MATLAB: rand/randn/randperm) | Medium |
| Python version not specified in README | Low |

---

## `--fix`: auto-generate missing files

```bash
repro-check --path /your/code --fix
```

If critical files are missing, `--fix` generates them:
- `requirements.txt` — from `pip freeze`
- `environment.yml` — conda environment template with your Python version
- `SETUP.md` — step-by-step setup guide template

Review each file before committing — they are starting points, not finished documents.

---

## Who is this for?

- Academic research labs running simulation, FEA, or CFD code (FEniCS, OpenFOAM, Abaqus, SU2)
- Engineering R&D teams with legacy Python or MATLAB workflows
- Research groups doing data analysis who inherited undocumented codebases
- PhD students trying to hand over working code to their supervisor or a collaborator

---

## Roadmap

| Version | Feature |
|---|---|
| v0.1 | 14 checks, `--fix` flag, JSON/Markdown output |
| v0.2 | R / `renv` checks, Snakemake checks, `--min-score` exit code for CI |
| v1.0 | Web UI — drop a GitHub URL, get a report |

---

## Project structure

```
src/repro/
├── checker.py    ← all check logic; returns ReproReport
├── cli.py        ← click CLI entry point
├── fixer.py      ← --fix: generates missing files
├── report.py     ← terminal, Markdown, JSON, PDF output
└── templates/    ← SETUP.md and environment.yml templates
tests/            ← pytest suite
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a new check.

## License

MIT — see [LICENSE](LICENSE).
