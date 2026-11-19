#!/usr/bin/env python3
"""Install nine managed Codex agents. Python 3.11+."""
import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parent
ROLES = ("scout", "researcher", "writer", "builder", "tester", "debugger", "designer", "architect", "reviewer")
LEGACY = ("planner",)
LATEST_MODELS = {"scout": "gpt-6-luna", "researcher": "gpt-6.1-terra", "writer": "gpt-6.2-sol", "builder": "gpt-6.2-sol", "tester": "gpt-6.2-sol", "debugger": "gpt-6.2-sol", "designer": "gpt-6.1-terra", "architect": "gpt-6.2-astra", "reviewer": "gpt-6.2-astra"}
EFFORTS = {"scout": "low", "researcher": "medium", "writer": "medium", "builder": "high", "tester": "high", "debugger": "xhigh", "designer": "high", "architect": "xhigh", "reviewer": "high"}
START, END = "<!-- model-router:start -->", "<!-- model-router:end -->"
HEADER = b"# Managed by model-router-codex\n"

def read(path):
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError(f"Not a regular file: {path}")
    return path.read_bytes() if path.exists() else None

def rules(before, block, remove=False):
    text = (before or b"").decode()
    if text.count(START) != text.count(END) or text.count(START) > 1:
        raise ValueError("Repair malformed or duplicate router markers before installation.")
    if START in text:
        left, tail = text.split(START, 1)
        if END not in tail:
            raise ValueError("Router markers out of order.")
        _, right = tail.split(END, 1)
        return (left + ("" if remove else block) + right).encode()
    return (text if remove else text + ("\n\n" if text else "") + block + "\n").encode()

def plan(home, ag, remove=False, models=None, efforts=None):
    efforts = efforts or {}
    models = models or {}
    if home.is_symlink() or (home / "agents").is_symlink():
        raise ValueError("Refusing symlinked target directories.")
    changes = {}
    for role in ROLES + LEGACY:
        path = home / "agents" / f"mr_{role}.toml"
        before = read(path)
        if before is not None and not before.startswith(HEADER):
            if remove or role in LEGACY:
                continue
            raise ValueError(f"Refusing unmanaged agent collision: {path}")
        after = None if remove or role in LEGACY else (ROOT / "agents" / path.name).read_bytes()
        if after is not None:
            if models.get(role):
                after = after.replace(b'developer_instructions =', ('model = ' + json.dumps(models[role], ensure_ascii=False) + '\n' + 'developer_instructions =').encode(), 1)
            if efforts.get(role):
                after = after.replace(b'developer_instructions =', ('model_reasoning_effort = ' + json.dumps(efforts[role]) + '\n' + 'developer_instructions =').encode(), 1)
            config = tomllib.loads(after.decode())
            if config["name"] != path.stem or not config["developer_instructions"].strip():
                raise ValueError(f"Invalid agent: {path.name}")
        if before != after:
            changes[path] = (before, after)
    before = read(ag)
    after = rules(before, (ROOT / "AGENTS.md").read_text().rstrip("\n"), remove)
    if (before is not None or after) and before != after:
        changes[ag] = (before, after)
    return changes

def write(path, data):
    if data is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as f:
        name = Path(f.name)
        try:
            f.write(data)
        except BaseException:
            f.close()
            name.unlink(missing_ok=True)
            raise
    try:
        if path.exists():
            shutil.copymode(path, name)
        os.replace(name, path)
    finally:
        name.unlink(missing_ok=True)

def apply(home, changes):
    if not changes:
        print("No changes needed.")
        return
    home.mkdir(parents=True, exist_ok=True)
    backup = Path(tempfile.mkdtemp(prefix="model-router-backup-", dir=home))
    for path, (before, _) in changes.items():
        if before is not None:
            (backup / path.name).write_bytes(before)
    print(f"Backup: {backup}")
    done = []
    try:
        for path, (before, after) in changes.items():
            if read(path) != before:
                raise ValueError(f"File changed during installation: {path}")
            write(path, after)
            done.append(path)
    except (Exception, KeyboardInterrupt):
        for path in reversed(done):
            before, after = changes[path]
            try:
                if read(path) == after:
                    write(path, before)
                else:
                    print(f"Concurrent change; restore manually: {path}", file=sys.stderr)
            except (OSError, ValueError):
                print(f"Restore manually: {path}", file=sys.stderr)
        raise
    print(f"Updated {len(changes)} files.")

def main():
    p = argparse.ArgumentParser(description=__doc__)
    scope = p.add_mutually_exclusive_group(required=True)
    scope.add_argument("--global", dest="global_scope", action="store_true")
    scope.add_argument("--project", type=Path)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--uninstall", action="store_true")
    p.add_argument("--fast-model", help="Exact Codex model ID for scout (e.g. account-supported Luna)")
    p.add_argument("--build-model", help="Exact Codex model ID for builder, tester, writer and debugger (e.g. account-supported Sol or Terra)")
    p.add_argument("--astra-model", help="Exact Codex Astra model ID for architect and reviewer")
    p.add_argument("--profile", choices=("inherit", "latest"), default="inherit", help="Opt in to current official API model IDs; confirm Codex account access first")
    p.add_argument("--research-model", help="Exact Codex model ID for researcher and designer")
    p.add_argument("--recommended-efforts", action="store_true", help="Opt in to role-specific efforts only if supported by selected models")
    a = p.parse_args()
    try:
        if a.project:
            project = a.project.expanduser().absolute()
            if not project.is_dir() or project.is_symlink():
                raise ValueError("Project must be an existing non-symlink directory.")
            home, ag = project / ".codex", project / "AGENTS.md"
        else:
            home = Path(os.environ.get("CODEX_HOME") or "~/.codex").expanduser().absolute()
            ag = home / "AGENTS.md"
        models = LATEST_MODELS.copy() if a.profile == "latest" else {}
        overrides = {"scout": a.fast_model, "researcher": a.research_model, "designer": a.research_model, "builder": a.build_model, "tester": a.build_model, "writer": a.build_model, "debugger": a.build_model, "architect": a.astra_model, "reviewer": a.astra_model}
        models.update({role: model for role, model in overrides.items() if model})
        changes = plan(home, ag, a.uninstall, models, EFFORTS if a.recommended_efforts or a.profile == "latest" else None)
        if a.dry_run:
            for path, (_, after) in changes.items():
                print(("REMOVE " if after is None else "WRITE ") + str(path))
            if not changes:
                print("No changes needed.")
        else:
            apply(home, changes)
    except (OSError, ValueError, KeyError) as e:
        print(f"model-router: {e}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
