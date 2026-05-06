# Blueprint: Research Software Reproducibility Service

## The Problem

Engineering and science researchers lose enormous time to environment drift:
- A simulation that ran last year won't run today because a package changed
- A new PhD student can't reproduce results from a former student's thesis
- A collaborating lab can't run your code because their Python/MATLAB/library versions differ
- You can't remember what you installed 6 months ago to get the CFD setup working

This is not a niche problem. It is endemic to academic computing. Most labs have no one responsible for fixing it.

---

## The Opportunity

**Target clients (primary)**
- Academic research labs running simulation, FEA, or CFD code (FEniCS, OpenFOAM, Abaqus, ANSYS scripting, SU2, etc.)
- Engineering R&D departments using legacy Python or MATLAB workflows
- Research groups doing data analysis in Python who inherited undocumented codebases

**Target clients (secondary)**
- Small engineering consultancies with fragile internal tooling
- Labs transitioning from MATLAB to Python who have broken environments everywhere

**Why I am credible**
- I am this client. I work in this exact environment.
- I can speak to the problem as a researcher, not as a software vendor.
- I understand FEA/CFD tools, which most general software consultants do not.

---

## The Service

### Offering: Reproducibility Audit (fixed-fee)

**What I do**
1. Review the lab's simulation/analysis codebase (typically a GitHub repo or a folder of scripts)
2. Identify all environment dependencies (Python version, packages, MATLAB toolboxes, external solvers)
3. Identify reproducibility gaps (missing requirements files, hardcoded paths, undocumented steps)
4. Deliver a written report + fixed environment specification

**What the client gets**
- Written reproducibility report (PDF or Markdown)
- `requirements.txt` or `environment.yml` (conda) or `Dockerfile` — whichever fits their stack
- Step-by-step `SETUP.md` so anyone can reproduce the environment
- 30-minute walkthrough call

**Pricing**
- Small lab (1 codebase, <5k lines): $500–$800
- Medium lab (2–3 codebases, legacy MATLAB + Python): $1,200–$2,000
- First 2 clients: offer at cost or free in exchange for a testimonial and case study

### Offering: Reproducibility Retainer (monthly)

After the audit, some labs will want ongoing maintenance:
- Monthly environment health check
- Fix breaks when packages update
- Onboard new students to the environment

**Pricing**: $200–$400/month

---

## MVP Definition

The minimum I need to offer the audit service:

1. A standard checklist of reproducibility gaps to look for (write this first — it's also the core of the future toolkit)
2. A template `SETUP.md` I can customize per client
3. A template `environment.yml` structure I know how to build
4. A 1-page service description I can send to a potential client

Everything else can be learned as I do the first engagement.

---

## Path from Service to Product

After 3–5 audits, patterns will emerge:
- The same gaps appear in every lab (no `requirements.txt`, hardcoded paths, missing solver version documentation)
- The same fixes apply every time

At that point, build a tool:
- `repro-check` CLI: run it on a research repo and get a reproducibility score + gap report
- Open-source on GitHub — attracts inbound consulting leads
- Later: web version ("drop your repo URL, get a report")

---

## GitHub Strategy for This Project

**Public repo name**: `research-reproducibility-toolkit`
**What goes in it**:
- `checklist.md` — the reproducibility audit checklist (immediately useful to anyone)
- `templates/` — `environment.yml`, `Dockerfile`, `SETUP.md` templates for common research stacks
- `examples/` — anonymized before/after examples from real audits
- `README.md` — written like a product page, not a code dump

**Why this works for the portfolio**:
- Very specific and searchable ("research software reproducibility")
- Immediately useful even before the CLI tool exists
- Signals both domain knowledge (FEA/CFD) and software skills (environments, Docker)

---

## First 3 Action Steps

1. **Write the reproducibility checklist** — 1–2 hours. This is the core intellectual property. List every common failure mode from your own experience.
2. **Write the service one-pager** — 1 hour. One page: what the problem is, what you do, what the client gets, pricing.
3. **Reach out to 3 people** — Email 2–3 researchers you know (your lab, other groups at QUB, collaborators) and ask: "Is this a real pain for you? Would you pay someone to fix it?"

---

## Skills to Learn (with Claude's help)

| Skill | Needed for | When to learn |
|-------|-----------|---------------|
| `conda` / `environment.yml` | Environment spec | Now — start with this |
| `pip` / `requirements.txt` | Python packaging | Now |
| `Docker` basics | Containerized environments | After first client asks |
| `GitHub Actions` | Automated environment checks | Month 2 |
| Basic `pytest` | Verification tests | Month 2 |

---

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| No one wants to pay for this | Start free — gather testimonials first |
| I'm not experienced enough | I don't need to be a Docker expert; I need to be better than having nothing |
| Takes too long per client | Build templates + checklist to make it fast |
| Academic clients have no budget | Approach industrial R&D clients too; they do have budget |
