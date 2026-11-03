"""Check local-only execution and stale-index detection without third-party installs."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "graphify.py"
spec = importlib.util.spec_from_file_location("madx_graph_tool", SCRIPT)
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


class GraphifyToolingTests(unittest.TestCase):
    def test_backend_and_logging_cannot_leak_from_parent_configuration(self):
        with patch.dict(os.environ, {"GRAPHIFY_BACKEND": "openai", "GRAPHIFY_QUERY_LOG": "private.log",
                                     "GRAPHIFY_OUTPUT_DIR": "outside", "GRAPHIFY_GLOBAL": "1"}):
            env = tool.local_env()
        self.assertEqual(env["GRAPHIFY_BACKEND"], "none")
        self.assertEqual(env["GRAPHIFY_QUERY_LOG_DISABLE"], "1")
        self.assertNotIn("GRAPHIFY_QUERY_LOG", env)
        self.assertNotIn("GRAPHIFY_OUTPUT_DIR", env)
        self.assertNotIn("GRAPHIFY_GLOBAL", env)

    def test_working_edits_new_files_and_deletions_invalidate_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text("graphify-out/\n.venv/\n")
            source = root / "example.py"
            source.write_text("value = 1\n")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            out = root / "graphify-out"
            out.mkdir()
            graph, stamp = out / "graph.json", out / "madx-index.json"
            with patch.multiple(tool, ROOT=root, GRAPH=graph, STAMP=stamp):
                self.assertEqual(tool.state(), "missing")
                graph.write_text("{}")
                original = tool.fingerprint()
                stamp.write_text(json.dumps({"working_tree_sha256": original,
                                             "graphify_version": tool.VERSION}))
                self.assertEqual(tool.state(), "fresh")
                (out / "derived.txt").write_text("ignore generated files")
                self.assertEqual(tool.state(), "fresh")
                source.write_text("value = 2\n")
                self.assertEqual(tool.state(), "stale")
                source.write_text("value = 1\n")
                extra = root / "new.py"
                extra.write_text("new = True\n")
                self.assertEqual(tool.state(), "stale")
                extra.unlink()
                source.unlink()
                self.assertEqual(tool.state(), "stale")

    def test_query_cannot_inject_upstream_cli_flags(self):
        with patch.object(tool, "run") as run, patch.object(
            tool.sys, "argv", [str(SCRIPT), "query", "--global"]
        ):
            with self.assertRaises(SystemExit) as raised:
                tool.main()
            self.assertEqual(raised.exception.code, 2)
            run.assert_not_called()

    def test_failed_build_does_not_leave_fresh_stamp(self):
        with tempfile.TemporaryDirectory() as tmp:
            stamp = Path(tmp) / "madx-index.json"
            stamp.write_text("old success")
            with patch.object(tool, "STAMP", stamp), patch.object(tool, "fingerprint", return_value="a"), \
                 patch.object(tool, "run", side_effect=subprocess.CalledProcessError(1, "graphify")):
                with self.assertRaises(subprocess.CalledProcessError):
                    tool.build()
                self.assertFalse(stamp.exists())

    def test_build_keeps_extraction_local_and_limits_workers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            graph, stamp = root / "graph.json", root / "madx-index.json"
            graph.write_text('{"nodes": [], "links": []}')
            with patch.multiple(tool, ROOT=root, GRAPH=graph, STAMP=stamp), \
                 patch.object(tool, "fingerprint", return_value="stable"), \
                 patch.object(tool, "git", return_value=b"a" * 40), patch.object(tool, "run") as run:
                tool.build()
            self.assertEqual(run.call_args_list[0].args,
                             ("extract", str(root), "--code-only", "--no-cluster", "--max-workers", "4"))
            self.assertEqual(run.call_args_list[1].args,
                             ("cluster-only", str(root), "--no-label"))
            self.assertTrue(stamp.exists())

    def test_task_registry_has_unique_ids_real_paths_and_acceptance(self):
        data = json.loads((tool.ROOT / "docs/madx/WORK_ITEMS.json").read_text())
        ids = [item["id"] for item in data["items"]]
        self.assertEqual(len(ids), len(set(ids)))
        for item in data["items"]:
            self.assertIn(item["status"], data["status_legend"])
            self.assertTrue(item["acceptance"])
            for path in item["paths"]:
                self.assertTrue((tool.ROOT / path).exists(), path)


if __name__ == "__main__":
    unittest.main()
