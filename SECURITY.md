# Security policy

## Supported version

Security reports are welcome for the current public main branch. The project is an early release; support for older snapshots is best effort.

## Reporting a vulnerability

Use the repository's private vulnerability reporting feature if it is enabled (Security → Report a vulnerability). If unavailable, open a minimal issue asking for a private contact method, without disclosing the vulnerability, exploit, secrets or personal data.

Include affected commit, operating system, reproduction using non-sensitive test files, expected impact and any suggested mitigation. No guaranteed response time is promised.

## Security boundaries

The installer writes local managed agent definitions and a marked AGENTS.md block. Use trusted commits, inspect the dry-run and backups, and use least-privilege permissions. Agent instructions are not a sandbox or enforcement mechanism; actual safety depends on the Codex runtime and configuration.

Do not grant write access to sensitive systems based solely on routing instructions. Do not use production secrets in examples, issues, logs or benchmarks. Live runtime isolation and model compatibility have not been independently certified.
