import tempfile
import unittest
from pathlib import Path
import tomllib
import install

class RouterTests(unittest.TestCase):
    def test_matrix(self):
        files = sorted((install.ROOT / "agents").glob("*.toml"))
        self.assertEqual(len(files), 9)
        for path in files:
            data = tomllib.loads(path.read_text())
            self.assertEqual(data["name"], path.stem)
            self.assertNotIn("model", data)
            self.assertNotIn("model_reasoning_effort", data)

    def test_install_update_uninstall(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home, ag = root / ".codex", root / "AGENTS.md"
            ag.write_text("Keep existing rules.\n")
            changes = install.plan(home, ag)
            self.assertEqual(len(changes), 10)
            install.apply(home, changes)
            self.assertFalse(install.plan(home, ag))
            self.assertEqual(len(list((home / "agents").glob("*.toml"))), 9)
            install.apply(home, install.plan(home, ag, True))
            self.assertIn("Keep existing rules.", ag.read_text())
            self.assertFalse(list((home / "agents").glob("*.toml")))

    def test_collision(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / "agents").mkdir()
            path = home / "agents/mr_scout.toml"
            path.write_text("unmanaged")
            with self.assertRaises(ValueError):
                install.plan(home, home / "AGENTS.md")
            self.assertEqual(path.read_text(), "unmanaged")

    def test_malformed_rules(self):
        with self.assertRaises(ValueError):
            install.rules(install.START.encode(), "block")

    def test_optional_model_tiers(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            changes = install.plan(home, home / "AGENTS.md", models={"architect": "example-astra", "scout": "example-fast"})
            self.assertEqual(tomllib.loads(changes[home / "agents/mr_architect.toml"][1].decode())["model"], "example-astra")
            self.assertEqual(tomllib.loads(changes[home / "agents/mr_scout.toml"][1].decode())["model"], "example-fast")
            self.assertNotIn("model", tomllib.loads(changes[home / "agents/mr_builder.toml"][1].decode()))

    def test_latest_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            changes = install.plan(home, home / "AGENTS.md", models=install.LATEST_MODELS, efforts=install.EFFORTS)
            for role in install.ROLES:
                data = tomllib.loads(changes[home / "agents" / f"mr_{role}.toml"][1].decode())
                self.assertEqual(data["model"], install.LATEST_MODELS[role])
                self.assertEqual(data["model_reasoning_effort"], install.EFFORTS[role])

    def test_migrate_managed_planner(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / "agents").mkdir()
            old = home / "agents/mr_planner.toml"
            old.write_bytes(install.HEADER + b"old")
            changes = install.plan(home, home / "AGENTS.md")
            self.assertIsNone(changes[old][1])
            install.apply(home, changes)
            self.assertFalse(old.exists())
            self.assertTrue((home / "agents/mr_architect.toml").exists())

    def test_preserve_unmanaged_planner(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / "agents").mkdir()
            old = home / "agents/mr_planner.toml"
            old.write_text("user-owned")
            self.assertNotIn(old, install.plan(home, home / "AGENTS.md"))
