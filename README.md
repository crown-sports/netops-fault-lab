# NetOps Fault Lab

Rank suspect network links and choose where to probe next.

[![CI](https://github.com/crown-sports/netops-fault-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/crown-sports/netops-fault-lab/actions/workflows/ci.yml)
[Python 3.10+](pyproject.toml) · [v0.2.1 preview](https://github.com/crown-sports/netops-fault-lab/releases/tag/v0.2.1) · [MIT](LICENSE)

[中文](README.zh-CN.md) · [Input format](docs/input.md) · [How it works](docs/method.md) · [Experiments](docs/experiments.md)

Two probes to the database fail; probes to the cache pass. Is the fault on the
core link or the database link? With those paths, either fault explains the
observations. This offline tool shows the ambiguity and suggests a measurement
that can tell the candidates apart.

## Before: two links fit

![Before the extra probe: core and database each have 49.8 percent model probability; probe r1 to r2 next](docs/assets/probe-before-v0.2.png)

*Actual v0.2.1 report from `examples/ambiguous.json`. Both candidates have 49.8% model probability. The suggested next probe is `r1 → r2`.*

## After: one extra observation

![After adding the scripted failed r1 to r2 probe, core rises to 96.7 percent](docs/assets/probe-after-v0.2.png)

*`examples/after-probe.json` adds a failed `r1 → r2` result; core rises to 96.7%. Both inputs are synthetic. The tool sends no network probes.*

## Run the example

```bash
git clone --branch v0.2.1 https://github.com/crown-sports/netops-fault-lab.git
cd netops-fault-lab
python -m venv .venv
```

Activate with `source .venv/bin/activate` on macOS/Linux or `.venv\Scripts\Activate.ps1` in PowerShell, then:

```bash
python -m pip install .
netops-fault-lab diagnose examples/ambiguous.json --format html --output before.html
netops-fault-lab diagnose examples/after-probe.json --format html --output after.html
```

Open the two HTML files. Below the topology, each report shows which observations
separate the candidates and which measurement to try next. Output filenames must
be new. Omit `--format` and `--output` for a terminal summary, or use `--format json`
for scripts. Core inference uses only the Python standard library.

## Use your own paths and measurements

Copy `examples/ambiguous.json` to `incident.json`. Replace the links, probe paths
and outcomes with one observation window from your network. Include only candidate
probes you can actually run. The [input guide](docs/input.md) lists the fields.

```bash
netops-fault-lab diagnose incident.json --format html --output incident-report.html
```

Run the suggested measurement with your existing tooling, add its outcome, and
repeat. Exit `0` means a valid report, including an ambiguous one; invalid inputs
return `2`.

The model assumes known, unchanged paths and at most one failed link. Default
noise parameters are illustrative. Fit them on labeled incidents and check them
on held-out data before interpreting the probability magnitudes.
[Model assumptions and fitting](docs/method.md).

## Forwarded copies should not count twice

```bash
netops-fault-lab diagnose examples/replayed-event.json --format json
```

This example has five records from four measurements. Copies of one event share
`event_id`; the report keeps one and marks one ignored copy. Each record's `id`
stays unique. Conflicting paths or outcomes for one event are rejected.
Independent repeated measurements need different event IDs; untagged records
are treated as independent.

## Explore the experiments

The synthetic benchmark compares failed-path voting, logistic regression and
Bayesian ranking under missing probes, duplicate alarms and changing noise.
Bayesian ranking is close to logistic regression. In the separate active-probe
experiment, information-gain selection reaches **72.5% Top-1**, versus **57.2%**
for random selection with the same four-probe budget.

These are simulation results, not production-network accuracy.
[Data, per-case results and reproduction commands](docs/experiments.md).

[Implementation notes](docs/product.md) · [Image sources](docs/screenshots.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [Citation](CITATION.cff)
