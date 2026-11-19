# Compatibility matrix

## Installer validation

At public V2 merge commit `30237aa1935daa2eb29b651da8a95dbd21474d7e`, [main-branch CI](https://github.com/NathalieChouLab/model-router-codex-public/actions/runs/44544669909) passed.

| Environment | Installer tests | Live Codex delegation |
|---|---|---|
| Ubuntu, Python 3.11 | Passed | Not tested |
| macOS, Python 3.11 | Passed | Not tested |
| Windows, Python 3.11 | Passed | Not tested |

## Model profile

| Bundled model identifier | Role assignment | Actual Codex runtime |
|---|---|---|
| gpt-6-luna | Scout | Unverified |
| gpt-6.1-terra | Researcher, Designer | Unverified |
| gpt-6.2-sol | Writer, Builder, Tester, Debugger | Unverified |
| gpt-6.2-astra | Architect, Reviewer | Unverified |
| Inherited model | All roles by default | Unverified |

The installer can generate settings; this does not establish that the Codex runtime accepts them. Check exact identifiers, effort options and account entitlements against your installed Codex. Start with inherited settings. Do not assume API availability establishes Codex compatibility.

## Report a result

Use a disposable repository. Record date, OS, Python version, Codex version, commit, selected profile, model ID/effort (if observable), task, actual delegation evidence, result and sanitized error logs. Never include credentials or confidential project data. If actual model identity is unavailable, mark it unverified.
