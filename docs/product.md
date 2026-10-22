# Product value and evidence

[English README](../README.md) · [中文首页](../README.zh-CN.md)

## The decision this supports

For a network researcher or operator with a known path snapshot and pass/fail
probe observations: which link hypotheses remain plausible, and which available
measurement would best distinguish them? The output is a reviewable offline
incident report and a proposed next probe. No probe is executed and no device is
changed.

The useful first result may be “these two links are indistinguishable.” A tool
that states that uncertainty can help plan a measurement without inventing a
unique root cause.

## Current advantages, with inspectable evidence

| Capability | Why it matters | Implementation and evidence |
| --- | --- | --- |
| Use passed and failed path evidence and expose indistinguishable signatures | More alarms do not necessarily distinguish two possible fault locations | [inference.py](../src/netops_fault_lab/inference.py), [inference tests](../tests/test_inference.py) |
| Rank supplied probes by expected information gain per cost | Turn ambiguity into a concrete next measurement within a supplied candidate pool | [inference.py](../src/netops_fault_lab/inference.py), [experimental protocol and results](experiments.md) |
| Explicit upstream event identity during diagnosis and noise fitting | Forwarded copies of one event should not multiply the evidence; independent new measurements remain separate | [schema.py](../src/netops_fault_lab/schema.py), [event tests](../tests/test_events.py) |
| Preserve input fingerprints, model parameters and per-case records | Review what produced a ranking and inspect failures instead of relying only on average accuracy | [CLI](../src/netops_fault_lab/cli.py), [benchmark.py](../src/netops_fault_lab/benchmark.py), [contract tests](../tests/test_contract.py) |

Bayesian inference and information gain are established methods. Recorded
synthetic experiments show a benefit from active probe selection in the tested
setting; Bayesian ranking does not clearly beat the logistic baseline. This is
not evidence of production root-cause accuracy or reduced recovery time.

## Connect one real incident

1. Export the actual undirected link/path snapshot for one stable observation
   window. Do not silently substitute shortest paths for observed routes.
2. Map probe outcomes to `pass`, `fail` or `missing`. Preserve collector event IDs
   across retransmissions; assign different IDs to independent measurements.
3. Supply only probes your operators could actually perform, with their relative
   costs. Run diagnosis, inspect ambiguity, then perform the chosen measurement
   using your existing tooling. Add the resulting observation and rerun.
4. Before interpreting probabilities operationally, fit noise parameters using
   separate labeled incidents and check calibration on held-out incidents. The
   bundled default parameters and training file are demonstrations.

See the [complete JSON contract](input.md), including optional `event_id`, output
fields and `fit`. CLI success means a report was produced; an ambiguous result
also exits 0. It is not an automatic remediation approval.

## Limits and what could become a durable advantage

Known static routes, at most one faulty link, and conditional independence remain
model assumptions. Event deduplication fixes known retransmissions; it does not
infer dependence between different alarms. Correlated noise, simultaneous faults,
route changes and application causes need other models.

A growing collection of controlled measurements with known causes, repeatable
collector mappings and evaluated probe policies could become a durable advantage.
The present benchmark is synthetic; real-network validation and those integrations
are future work, not existing product coverage. [Research roadmap](roadmap.zh-CN.md).
