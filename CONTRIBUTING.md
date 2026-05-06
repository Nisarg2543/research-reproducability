# Contributing to repro-check

Thanks for your interest in improving repro-check.

## Dev setup

```bash
git clone https://github.com/Nisarg2543/research-reproducability
cd repro-check
pip install -e ".[dev]"
pytest tests/ -v
```

## How to add a new check

Each check is a method on `ReproChecker` in [src/repro/checker.py](src/repro/checker.py).

1. Add a method named `_check_<thing>(self, report: ReproReport)`
2. Call `report.issues.append(Issue(...))` for each problem found
3. Wire it into `ReproChecker.run()` 
4. Add at least two tests in `tests/` — one that triggers the issue, one that doesn't
5. Add the check to the table in `README.md`

**Issue fields:**

| Field | Description |
|---|---|
| `severity` | `"critical"` / `"high"` / `"medium"` / `"low"` |
| `category` | Short label shown in report (`"Environment"`, `"Portability"`, etc.) |
| `file` | Relative file path, or `"/"` if repo-level |
| `message` | One sentence: what's wrong |
| `fix` | One sentence: what to do |

**Severity guide:**

- **Critical** — prevents anyone from running the code at all
- **High** — will cause silent failures or different results on a different machine
- **Medium** — makes setup significantly harder for someone new
- **Low** — good practice but not blocking

## Running tests with coverage

```bash
pytest tests/ --cov=repro --cov-report=term-missing
```

## PR checklist

- [ ] New check has a corresponding test
- [ ] `README.md` checks table updated
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] `pytest tests/` passes
