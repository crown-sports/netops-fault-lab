# README report screenshots

`assets/probe-before-v0.2.png` and `assets/probe-after-v0.2.png` are direct browser
screenshots of the v0.2.0 CLI output. Each captures the top 1200 × 965 viewport:
the diagnosis, topology, ranking and next measurement. The report is not modified
for the screenshots; open the HTML to see the remaining evidence table and
model assumptions.

Reproduce from the repository root with NetOps Fault Lab installed:

```bash
netops-fault-lab diagnose examples/ambiguous.json --format html --output before.html
netops-fault-lab diagnose examples/after-probe.json --format html --output after.html
```

The first fixture has four observations, leaving core/database indistinguishable
at 49.8% each. The second adds a scripted failed `r1 → r2` measurement, after which
core has 96.7% model probability. Both fixtures are synthetic; the CLI never sends
a probe. The probabilities use the illustrative default model parameters.

Older screenshots and HTML examples are kept for existing documentation links.
