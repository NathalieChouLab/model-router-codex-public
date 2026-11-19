# Model Router for Codex

Five focused native Codex subagents and quality-first routing guidance. Unofficial, dependency-free installer; no hard-coded model IDs.

## Install

Requires Python 3.11+ and a Codex release with custom subagents. Clone this repository, inspect the files, then run:

```sh
python3 install.py --global --dry-run
python3 install.py --global
```

For one project use `--project /path/to/project` instead of `--global`. Restart Codex. Ask it to use mr_scout for evidence and mr_reviewer for an independent review.

| Agent | Role |
|---|---|
| mr_scout | Evidence and research |
| mr_planner | Architecture and diagnosis |
| mr_builder | Bounded implementation |
| mr_tester | Independent testing |
| mr_reviewer | Independent review |

## Model configuration

The agent files intentionally omit model and reasoning effort. Codex resolves these from explicit spawn settings, agent defaults and the parent session. Users can set supported model and effort values in Codex configuration or customize installed TOML files. Reinstalling resets managed files, so back up overrides first. No model availability or token savings are guaranteed.

[Official Codex subagent documentation](https://developers.openai.com/codex/subagents)

### Optional model tiers, including Astra

| Role | Suggested family when available in your account |
|---|---|
| Scout | Luna / fast model |
| Builder, tester | Terra or Sol / implementation model |
| Planner, reviewer | Astra / advanced reasoning model |

The family labels above are suggestions, not guaranteed CLI identifiers or benchmark claims. Check Codex's model picker or official model documentation for the exact model IDs available to your account. Pass those IDs explicitly:

```sh
python3 install.py --global --fast-model "$FAST_MODEL" --build-model "$BUILD_MODEL" --astra-model "$ASTRA_MODEL" --dry-run
```

Set FAST_MODEL, BUILD_MODEL and ASTRA_MODEL first to the exact supported IDs. Remove --dry-run when satisfied. Omitted or empty flags inherit the session model. No automatic downgrade or probing of a paid model is performed. Reinstall with the same flags to retain overrides.

## Safety, updates and migration

The installer backs up modified files, refuses unmanaged name collisions, and changes only the marked router block in AGENTS.md. It does not change config.toml or authentication. Re-run to update. Previously installed unprefixed agent files are deliberately left untouched; back them up and remove manually only if no longer needed. Review changes before using on important projects. Delegation guidance is not a security boundary.

Uninstall with `python3 install.py --global --uninstall`, or use the original project scope. Run with `--dry-run` to preview. For cloud environments clone and inspect a trusted revision and execute the same installer in the target environment.

## Test

```sh
python3 -m unittest discover -s tests -v
```

Installer tests do not establish live Codex account compatibility. Smoke-test a small read-only delegated task before use.

MIT.
