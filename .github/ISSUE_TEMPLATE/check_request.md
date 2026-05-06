---
name: New check request
about: Suggest a new reproducibility check to add
labels: enhancement
---

**What should be checked?**
Describe the reproducibility issue you want detected (e.g., "MATLAB scripts using `rand` without setting a seed").

**What tool / language / workflow does this apply to?**
e.g., Python, MATLAB, R, Snakemake, OpenFOAM

**What severity would you expect?**
- [ ] Critical
- [ ] High
- [ ] Medium
- [ ] Low

**Example of code or config that should trigger the check:**
```
paste example here
```

**Suggested fix message:**
What should `repro-check` tell the user to do?
