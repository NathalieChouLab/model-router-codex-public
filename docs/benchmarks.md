# Benchmark protocol

**No performance results have been collected yet.** This document defines a proposed reproducible comparison, not a claim of savings.

Compare standard Codex without Model Router against Codex with the inherited-model router, using identical initial model settings, prompts, repository snapshots, permissions and time limits. Evaluate the optional model profile separately so differences in models are not confused with differences in routing.

Suggested task set: local code discovery, regression bug fix, small API integration, documentation update and architecture proposal. Keep public fixtures and independent acceptance tests fixed before running.

Run each condition multiple times in fresh sessions, alternate order, and record Codex version, commit, model settings, test commands, environment and limits. Avoid real production or personal data.

| Metric | Recording method |
|---|---|
| Correctness | Independent predeclared acceptance tests |
| Regressions | Previously passing tests that fail after changes |
| Latency | End-to-end elapsed time including delegation |
| Token use | Actual observable input/output/reasoning usage, including subagents |
| Cost | Observed billing or documented estimate with rate/date/assumptions |
| Completion | Completed, failed, timed out or unverified |

Do not substitute missing metrics with zero. If token or billing information is unavailable, report N/A. Include failed attempts and disclose variability and sample size. Use aggregate results and individual anonymized runs. Do not claim general superiority based on a small or cherry-picked sample.
