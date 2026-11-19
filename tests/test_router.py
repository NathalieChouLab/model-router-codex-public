import tempfile
import unittest
from pathlib import Path
import tomllib
import install

class RouterTests(unittest.TestCase):
    def test_matrix(self):
        files = sorted((install.ROOT / "agents").glob("*.toml"))
        self.assertEqual(len(files), 5)
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
            self.assertEqual(len(changes), 6)
            install.apply(home, changes)
            self.assertFalse(install.plan(home, ag))
            self.assertEqual(len(list((home / "agents").glob("*.toml"))), 5)
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
            changes = install.plan(home, home / "AGENTS.md", models={"planner": "example-astra", "scout": "example-fast"})
            self.assertEqual(tomllib.loads(changes[home / "agents/mr_planner.toml"][1].decode())["model"], "example-astra")
            self.assertEqual(tomllib.loads(changes[home / "agents/mr_scout.toml"][1].decode())["model"], "example-fast")
            self.assertNotIn("model", tomllib.loads(changes[home / "agents/mr_builder.toml"][1].decode()))
