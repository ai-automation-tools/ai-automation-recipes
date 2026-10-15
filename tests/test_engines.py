"""Tests for the CLI engines that don't need a live agent: profiles, command shape and output parsing.

The Codex and Gemini payloads below are recorded from real CLI output; the profiles must keep
parsing them exactly as the hand-written adapters they replaced did.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
# These tests pin the bundled profiles; the upstream fetch has its own tests below.
os.environ["RECIPES_CLI_REMOTE"] = "0"

from core.engines import EngineError, EngineRequest, engine_names, get_engine, load_profiles, model_for  # noqa: E402
from core.engines.cli import PROFILE_DIR, cache_dir  # noqa: E402

REQUIRED = {"name", "label", "binary", "install", "docs", "skillsDir", "toolPolicy", "argv", "output", "check", "verified"}


def req(**kw) -> EngineRequest:
    base = {"prompt": "p", "workdir": Path("/tmp/x"), "tools": ("Read", "Write"), "model": None}
    return EngineRequest(**{**base, **kw})


def proc(stdout: str, code: int = 0, stderr: str = "") -> mock.Mock:
    return mock.Mock(stdout=stdout, stderr=stderr, returncode=code)


class ProfileTests(unittest.TestCase):
    def test_bundled_profiles_are_complete(self):
        self.assertTrue({"claude", "codex", "gemini"} <= set(engine_names()))
        for f in sorted(PROFILE_DIR.glob("*.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            self.assertEqual(data["name"], f.stem, f.name)
            self.assertFalse(REQUIRED - set(data), f"{f.name} lacks {REQUIRED - set(data)}")
            self.assertIn(data["toolPolicy"], {"allowlist", "advisory"}, f.name)
            self.assertIn(data.get("prompt", "stdin"), {"stdin", "arg", "file"}, f.name)
            self.assertTrue(data["skillsDir"].endswith("/skills"), f.name)
            if data.get("prompt") == "arg":
                self.assertTrue(any("{prompt}" in a for a in data["argv"]), f.name)

    def test_unknown_engine(self):
        with self.assertRaises(EngineError):
            get_engine("no-such-cli")

    def test_user_dir_adds_and_overrides(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "mycli.json").write_text(json.dumps({"name": "mycli", "binary": "mycli", "argv": ["{prompt}"],
                                                         "prompt": "arg"}), encoding="utf-8")
            Path(d, "claude.json").write_text(json.dumps({"name": "claude", "binary": "my-claude"}), encoding="utf-8")
            Path(d, "broken.json").write_text("{", encoding="utf-8")
            with mock.patch.dict(os.environ, {"RECIPES_CLI_DIR": d}):
                profiles = load_profiles()
                self.assertIn("mycli", profiles)
                self.assertEqual(profiles["claude"]["binary"], "my-claude")
                self.assertIn("codex", profiles)

    def test_claude_aliases_mean_default_elsewhere(self):
        self.assertEqual(get_engine("claude").model("sonnet"), "sonnet")
        self.assertIsNone(get_engine("codex").model("sonnet"))
        self.assertIsNone(get_engine("gemini").model("opus"))
        self.assertEqual(get_engine("codex").model("gpt-5.5"), "gpt-5.5")
        self.assertIsNone(model_for("codex", None))


class ClaudeTests(unittest.TestCase):
    def test_command_shape(self):
        with mock.patch("shutil.which", return_value="claude"):
            cmd = get_engine("claude").command(req(model="sonnet"))
        self.assertEqual(cmd[1:6], ["--print", "--output-format", "json", "--permission-mode", "dontAsk"])
        self.assertEqual(cmd[cmd.index("--allowedTools") + 1], "Read,Write")
        self.assertEqual(cmd[cmd.index("--model") + 1], "sonnet")
        with mock.patch("shutil.which", return_value="claude"):
            cmd = get_engine("claude").command(req(tools=()))
        self.assertNotIn("--allowedTools", cmd)
        self.assertNotIn("--model", cmd)

    def test_result_and_busiest_model(self):
        payload = {"subtype": "success", "is_error": False, "result": "done", "num_turns": 4,
                   "modelUsage": {"claude-haiku-5-5": {"outputTokens": 3}, "claude-sonnet-5-5": {"outputTokens": 900}}}
        with mock.patch("shutil.which", return_value="claude"), mock.patch("subprocess.run", return_value=proc(json.dumps(payload))):
            res = get_engine("claude").run(req(model="sonnet"))
        self.assertEqual(res.text, "done")
        self.assertEqual(res.model, "claude-sonnet-5-5")
        self.assertEqual(res.meta["num_turns"], 4)

    def test_error_subtype(self):
        payload = {"subtype": "error_max_turns", "is_error": True, "result": "ran out"}
        with mock.patch("shutil.which", return_value="claude"), mock.patch("subprocess.run", return_value=proc(json.dumps(payload), 1)):
            with self.assertRaises(EngineError) as cm:
                get_engine("claude").run(req())
        self.assertIn("ran out", str(cm.exception))

    def test_no_json(self):
        with mock.patch("shutil.which", return_value="claude"), mock.patch("subprocess.run", return_value=proc("", 1, "auth")):
            with self.assertRaises(EngineError):
                get_engine("claude").run(req())


class CodexTests(unittest.TestCase):
    def test_command_shape(self):
        with mock.patch("shutil.which", return_value="C:/bin/codex.cmd"):
            cmd = get_engine("codex").command(req(model="sonnet"))
        self.assertEqual(cmd[1:3], ["exec", "--json"])
        self.assertIn("workspace-write", cmd)
        self.assertIn("--skip-git-repo-check", cmd)
        self.assertEqual(cmd[cmd.index("-C") + 1], str(Path("/tmp/x")))
        self.assertNotIn("-m", cmd)  # a Claude alias is not passed to Codex
        self.assertEqual(cmd[-1], "-")
        with mock.patch("shutil.which", return_value="C:/bin/codex.cmd"):
            cmd = get_engine("codex").command(req(model="gpt-5.5"))
        self.assertEqual(cmd[cmd.index("-m") + 1], "gpt-5.5")

    def test_takes_last_agent_message_and_usage(self):
        lines = [
            {"type": "thread.started", "thread_id": "t"},
            {"type": "item.completed", "item": {"id": "i0", "type": "error", "message": "Codex is ignoring 2 settings"}},
            {"type": "turn.started"},
            {"type": "item.completed", "item": {"id": "i1", "type": "agent_message", "text": "working…"}},
            {"type": "item.completed", "item": {"id": "i2", "type": "agent_message", "text": "```json\n{\"title\": \"T\"}\n```"}},
            {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 3}},
        ]
        out = "\n".join(json.dumps(l) for l in lines) + "\nnot json\n"
        res = get_engine("codex").parse(out, "", 0, "default")
        self.assertIn('"title": "T"', res.text)
        self.assertEqual(res.meta["output_tokens"], 3)

    def test_turn_failed(self):
        with self.assertRaises(EngineError) as cm:
            get_engine("codex").parse(json.dumps({"type": "turn.failed", "error": {"message": "boom"}}), "", 1, "x")
        self.assertIn("boom", str(cm.exception))

    def test_missing_message(self):
        with self.assertRaises(EngineError):
            get_engine("codex").parse(json.dumps({"type": "turn.started"}), "", 0, "x")


class GeminiTests(unittest.TestCase):
    def test_command_shape(self):
        with mock.patch("shutil.which", return_value="gemini"):
            cmd = get_engine("gemini").command(req(model="haiku"))
        self.assertEqual(cmd[1:5], ["-p", "", "-o", "json"])
        self.assertIn("yolo", cmd)
        self.assertNotIn("-m", cmd)
        with mock.patch("shutil.which", return_value="gemini"):
            cmd = get_engine("gemini").command(req(model="gemini-3.1-pro"))
        self.assertEqual(cmd[cmd.index("-m") + 1], "gemini-3.1-pro")

    def test_tolerates_banner_and_picks_busiest_model(self):
        payload = {"session_id": "s", "response": "PONG", "stats": {"models": {
            "gemini-3.1-flash": {"tokens": {"prompt": 5, "candidates": 2}},
            "gemini-3.1-pro": {"tokens": {"prompt": 50, "candidates": 40}}}}}
        res = get_engine("gemini").parse("YOLO mode is enabled.\n" + json.dumps(payload, indent=2), "", 0, "x")
        self.assertEqual(res.text, "PONG")
        self.assertEqual(res.model, "gemini-3.1-pro")
        self.assertEqual(res.meta["session_id"], "s")

    def test_error_envelope(self):
        with self.assertRaises(EngineError) as cm:
            get_engine("gemini").parse(json.dumps({"error": {"type": "AuthError", "message": "no auth"}}), "", 1, "x")
        self.assertIn("no auth", str(cm.exception))

    def test_returns_response_with_default_model(self):
        with mock.patch("shutil.which", return_value="gemini"), \
                mock.patch("subprocess.run", return_value=proc(json.dumps({"response": "```json\n{}\n```", "stats": {}}))):
            res = get_engine("gemini").run(req(model="sonnet"))
        self.assertEqual(res.model, "default")
        self.assertIn("{}", res.text)


class GenericPromptModes(unittest.TestCase):
    def test_arg_and_file_and_text_output(self):
        from core.engines.cli import CliEngine
        eng = CliEngine({"name": "t", "binary": "t", "prompt": "arg", "argv": ["run", "{prompt}"]})
        with mock.patch("shutil.which", return_value="t"):
            self.assertEqual(eng.command(req(prompt="hello"))[1:], ["run", "hello"])
        self.assertEqual(eng.parse("final words\n", "", 0, "m").text, "final words\n")
        with self.assertRaises(EngineError):
            eng.parse("", "", 0, "m")
        with self.assertRaises(EngineError):
            eng.parse("partial", "crash", 2, "m")

        with tempfile.TemporaryDirectory() as d:
            eng = CliEngine({"name": "f", "binary": "f", "prompt": "file", "promptFile": "P.md", "argv": ["--file", "{promptFile}"]})
            seen = {}

            def fake_run(cmd, **kw):
                seen["cmd"] = cmd
                seen["text"] = Path(cmd[-1]).read_text(encoding="utf-8")
                seen["input"] = kw.get("input")
                return proc("ok")

            with mock.patch("shutil.which", return_value="f"), mock.patch("subprocess.run", side_effect=fake_run):
                eng.run(req(prompt="from a file", workdir=Path(d)))
            self.assertEqual(seen["text"], "from a file")
            self.assertIsNone(seen["input"])
            self.assertFalse(Path(d, "P.md").exists())  # cleaned up after the run


class RemoteProfileTests(unittest.TestCase):
    """get_engine prefers the newest published profile, and falls back quietly."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        env = {"RECIPES_CLI_REMOTE": "1", "LOCALAPPDATA": self.tmp.name, "RECIPES_CLI_DIR": ""}
        self.env = mock.patch.dict(os.environ, env)
        self.env.start()
        self.bundled = load_profiles()["codex"]

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def published(self, **changes) -> mock.Mock:
        body = json.dumps({**self.bundled, **changes}).encode()
        resp = mock.MagicMock()
        resp.__enter__.return_value.read.return_value = body
        return mock.patch("urllib.request.urlopen", return_value=resp)

    def test_newer_flags_are_used_and_cached(self):
        argv = [*self.bundled["argv"], "--new-flag"]
        with self.published(argv=argv) as fetch:
            self.assertIn("--new-flag", get_engine("codex").profile["argv"])
            get_engine("codex")  # second call is served from the cache
        self.assertEqual(fetch.call_count, 1)
        self.assertTrue((cache_dir() / "codex.json").is_file())

    def test_a_different_binary_is_refused(self):
        with self.published(binary="not-codex"):
            self.assertEqual(get_engine("codex").binary, "codex")

    def test_an_older_profile_is_refused(self):
        with self.published(argv=["stale"], verified={"checked": "2000-01-01"}):
            self.assertEqual(get_engine("codex").profile["argv"], self.bundled["argv"])

    def test_offline_falls_back_to_bundled(self):
        with mock.patch("urllib.request.urlopen", side_effect=OSError("offline")):
            self.assertEqual(get_engine("codex").profile, self.bundled)

    def test_a_new_cli_can_arrive_upstream(self):
        new = {"name": "newcli", "binary": "newcli", "argv": ["{prompt}"], "prompt": "arg"}
        resp = mock.MagicMock()
        resp.__enter__.return_value.read.return_value = json.dumps(new).encode()
        with mock.patch("urllib.request.urlopen", return_value=resp):
            self.assertEqual(get_engine("newcli").binary, "newcli")

    def test_local_file_and_off_switch_skip_the_fetch(self):
        with tempfile.TemporaryDirectory() as d, self.published(argv=["x"]) as fetch:
            Path(d, "codex.json").write_text(json.dumps(self.bundled), encoding="utf-8")
            with mock.patch.dict(os.environ, {"RECIPES_CLI_DIR": d}):
                get_engine("codex")
            with mock.patch.dict(os.environ, {"RECIPES_CLI_REMOTE": "0"}):
                get_engine("codex")
        fetch.assert_not_called()


class NewCliTests(unittest.TestCase):
    """scripts/new_cli.py: the draft keeps the name and binary it was asked for, and records its help pages."""

    def test_draft(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import new_cli

        helps = {("--help",): "Usage: foo\n\nCommands:\n  run    run one prompt\n",
                 ("run", "--help"): "  --yes  approve all\n",
                 ("--version",): "foo 1.2.3\n"}
        reply = '```json\n{"name": "wrong", "binary": "wrong", "argv": ["run", "--yes", "{prompt}"], "prompt": "arg"}\n```'
        drafter = mock.Mock()
        drafter.run.return_value = mock.Mock(text=reply)
        with mock.patch.object(new_cli, "run", side_effect=lambda b, a: helps.get(tuple(a), "")), \
                mock.patch.object(new_cli, "get_engine", return_value=drafter):
            profile = new_cli.draft("foo", "foo", "claude")
        self.assertEqual((profile["name"], profile["binary"]), ("foo", "foo"))
        self.assertEqual(profile["check"]["help"], [["--help"], ["run", "--help"]])
        self.assertEqual(profile["verified"]["version"], "foo 1.2.3")
        self.assertIn("approve all", drafter.run.call_args.args[0].prompt)


if __name__ == "__main__":
    unittest.main()
