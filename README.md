# Model Router for Codex

Nine focused native Codex subagents with checkpoint-based routing, optional four-model profile and a dependency-free installer. Unofficial, MIT-licensed.

## Quick start

Requires Python 3.11+ and a Codex release supporting custom subagents.

```sh
git clone https://github.com/NathalieChouLab/model-router-codex-public.git
cd model-router-codex-public
python3 install.py --global --dry-run
python3 install.py --global
```

Use `--project /path/to/project` instead of `--global` for project scope. Restart Codex. Ask it to use mr_scout for evidence and mr_reviewer for independent review.

## Roles and optional latest profile

| Agent | Model ID | Reasoning effort | Role |
|---|---|---|---|
| mr_scout | gpt-6-luna | low | Local exploration |
| mr_researcher | gpt-6.1-terra | medium | External evidence |
| mr_writer | gpt-6.2-sol | medium | Documentation |
| mr_builder | gpt-6.2-sol | high | Implementation |
| mr_tester | gpt-6.2-sol | high | Independent tests |
| mr_debugger | gpt-6.2-sol | xhigh | Root cause |
| mr_designer | gpt-6.1-terra | high | Visual review |
| mr_architect | gpt-6.2-astra | xhigh | Architecture |
| mr_reviewer | gpt-6.2-astra | high | Independent review |

Model IDs verified against the [OpenAI API catalog](https://developers.openai.com/api/docs/models) on 2026-11-19. Account-specific Codex access is not guaranteed. These are suggested assignments, not measured benchmarks.

The default profile inherits the active Codex model and effort. To opt into the four-model profile after confirming all IDs and effort levels in your Codex installation:

```sh
python3 install.py --global --profile latest --dry-run
python3 install.py --global --profile latest
```

Override individual model groups with `--fast-model`, `--research-model`, `--build-model` and `--astra-model`. For custom models, keep inherited effort unless you confirm compatibility and explicitly use `--recommended-efforts`. The latest profile includes recommended efforts. No automatic paid model probes or fallback. Reinstall with the same options to keep model overrides.

[Codex subagent documentation](https://developers.openai.com/codex/subagents)

## Routing

Start with the smallest useful phase. Delegate evidence to scout/researcher, bounded edits to builder, tests to tester and review to reviewer. Unknown failures go to debugger; architectural decisions go to architect. Writer and designer handle dedicated content and visual work. Reassess after failures, scope changes and new evidence. No nested delegation or automatic deployment. Routing is guidance, not deterministic enforcement.

## Safety and migration

The installer backs up changed files, refuses unmanaged name collisions and replaces only the marked router block in AGENTS.md. It does not modify authentication or config.toml. Upgrading from the previous five-role version retires the managed mr_planner file and adds mr_architect. Unmanaged files remain untouched. Reinstalling resets managed agent files, so preserve local overrides.

Uninstall using `python3 install.py --global --uninstall` or the original project scope. Preview with `--dry-run`.

For cloud environments, clone a trusted revision then run the same installer in the target environment.

## Validation

```sh
python3 -m unittest discover -s tests -v
```

Static and installer checks are not proof of live Codex compatibility. Smoke-test a small read-only delegated task with your selected profile before important work.

MIT.
