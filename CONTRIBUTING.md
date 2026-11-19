# Contributing to Model Router for Codex

We welcome focused improvements to usability, cross-platform compatibility, routing clarity and documentation.

## Reporting a bug

Open a GitHub issue and provide:

- Operating system, Python and Codex versions.
- Installation scope, selected profile and exact command.
- Expected and actual behavior, with a minimal reproduction.
- Relevant error logs with API keys, personal paths, credentials and confidential project details removed.

For model compatibility reports, include the exact model ID, reasoning effort and whether an actual delegated task succeeded. Distinguish API model availability from Codex account access.

## Submitting a change

Keep pull requests small and describe the problem, approach, validation and remaining limitations. Use independent tests when changing installer behavior. Run:

```sh
python3 -m unittest discover -s tests -v
```

Do not assume that another account has access to the same models. Avoid adding dependencies, hard-coded credentials, unsupported performance claims or silent model fallback. Keep the default inherited configuration portable.

Report suspected security issues through an available private reporting channel rather than publishing sensitive details in an issue. Do not include private code or credentials.

By submitting a contribution, you agree that it is licensed under the project's MIT license.
