"""Tests for the text engines that don't need a live agent: command shape and output parsing."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.engines import ENGINES, EngineError, EngineRequest, get_engine, model_for  # noqa: E402
from core.engines import codex, gemini  # noqa: E402


class RegistryTests(unittest.TestCase):
    def test_three_engines_with_skill_folders(self):
        self.assertEqual(set(ENGINES), {"claude", "codex", "gemini"})
        for name in ENGINES:
            eng = get_engine(name)
            self.assertEqual(eng.name, name)
            self.assertTrue(eng.skills_dir.endswith("/skills"), name)

    def test_unknown_engine(self):
        with self.assertRaises(EngineError):
            get_engine("gpt")

    def test_claude_aliases_mean_default_elsewhere(self):
        self.assertEqual(model_for("claude", "sonnet"), "sonnet")
        self.assertIsNone(model_for("codex", "sonnet"))
        self.assertIsNone(model_for("gemini", "opus"))
        self.assertEqual(model_for("codex", "gpt-5.5"), "gpt-5.5")
        self.assertIsNone(model_for("codex", None))


class CodexTests(unittest.TestCase):
    def test_command_shape(self):
        eng = codex.CodexEngine()
        with mock.patch("shutil.which", return_value="C:/bin/codex.cmd"):
            cmd = eng.command(EngineRequest(prompt="p", workdir=Path("/tmp/x"), tools=("Read",), model="sonnet"))
        self.assertEqual(cmd[1:3], ["exec", "--json"])
        self.assertIn("workspace-write", cmd)
        self.assertIn("--skip-git-repo-check", cmd)
        self.assertNotIn("-m", cmd)  # a Claude alias is not passed to Codex
        self.assertEqual(cmd[-1], "-")
        with mock.patch("shutil.which", return_value="C:/bin/codex.cmd"):
            cmd = eng.command(EngineRequest(prompt="p", workdir=Path("/tmp/x"), tools=(), model="gpt-5.5"))
        self.assertEqual(cmd[cmd.index("-m") + 1], "gpt-5.5")

    def test_parse_events_takes_last_agent_message_and_usage(self):
        lines = [
            {"type": "thread.started", "thread_id": "t"},
            {"type": "item.completed", "item": {"id": "i0", "type": "error", "message": "Codex is ignoring 2 settings"}},
            {"type": "turn.started"},
            {"type": "item.completed", "item": {"id": "i1", "type": "agent_message", "text": "working…"}},
            {"type": "item.completed", "item": {"id": "i2", "type": "agent_message", "text": "```json\n{\"title\": \"T\"}\n```"}},
            {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 3}},
        ]
        text, usage, notices = codex.parse_events("\n".join(json.dumps(l) for l in lines) + "\nnot json\n")
        self.assertIn('"title": "T"', text)
        self.assertEqual(usage["output_tokens"], 3)
        self.assertEqual(len(notices), 1)

    def test_parse_events_turn_failed(self):
        with self.assertRaises(EngineError):
            codex.parse_events(json.dumps({"type": "turn.failed", "error": {"message": "boom"}}))

    def test_run_surfaces_missing_message(self):
        eng = codex.CodexEngine()
        proc = mock.Mock(stdout=json.dumps({"type": "turn.started"}), stderr="", returncode=0)
        with mock.patch("shutil.which", return_value="codex"), mock.patch("subprocess.run", return_value=proc):
            with self.assertRaises(EngineError):
                eng.run(EngineRequest(prompt="p", workdir=Path("."), tools=()))


class GeminiTests(unittest.TestCase):
    def test_command_shape(self):
        eng = gemini.GeminiEngine()
        with mock.patch("shutil.which", return_value="gemini"):
            cmd = eng.command(EngineRequest(prompt="p", workdir=Path("."), tools=(), model="haiku"))
        self.assertEqual(cmd[1:5], ["-p", "", "-o", "json"])
        self.assertIn("yolo", cmd)
        self.assertNotIn("-m", cmd)
        with mock.patch("shutil.which", return_value="gemini"):
            cmd = eng.command(EngineRequest(prompt="p", workdir=Path("."), tools=(), model="gemini-3.1-pro"))
        self.assertEqual(cmd[cmd.index("-m") + 1], "gemini-3.1-pro")

    def test_parse_output_tolerates_banner(self):
        payload = {"session_id": "s", "response": "PONG", "stats": {"models": {
            "gemini-3.1-flash": {"tokens": {"prompt": 5, "candidates": 2}},
            "gemini-3.1-pro": {"tokens": {"prompt": 50, "candidates": 40}}}}}
        out = gemini.parse_output("YOLO mode is enabled.\n" + json.dumps(payload, indent=2))
        self.assertEqual(out["response"], "PONG")
        self.assertEqual(gemini.busiest_model(out["stats"], "x"), "gemini-3.1-pro")
        self.assertEqual(gemini.busiest_model(None, "x"), "x")

    def test_run_reports_error_envelope(self):
        eng = gemini.GeminiEngine()
        proc = mock.Mock(stdout=json.dumps({"error": {"type": "AuthError", "message": "no auth"}}), stderr="", returncode=1)
        with mock.patch("shutil.which", return_value="gemini"), mock.patch("subprocess.run", return_value=proc):
            with self.assertRaises(EngineError) as cm:
                eng.run(EngineRequest(prompt="p", workdir=Path("."), tools=()))
        self.assertIn("no auth", str(cm.exception))

    def test_run_returns_response(self):
        eng = gemini.GeminiEngine()
        proc = mock.Mock(stdout=json.dumps({"response": "```json\n{}\n```", "stats": {}}), stderr="", returncode=0)
        with mock.patch("shutil.which", return_value="gemini"), mock.patch("subprocess.run", return_value=proc):
            res = eng.run(EngineRequest(prompt="p", workdir=Path("."), tools=(), model="sonnet"))
        self.assertEqual(res.model, "default")
        self.assertIn("{}", res.text)


if __name__ == "__main__":
    unittest.main()
