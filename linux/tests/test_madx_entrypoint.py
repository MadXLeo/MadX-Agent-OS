"""Public CLI dispatch contract; handlers are mocked, never install/update the test host.

This imports the real command implementation. Unavailable Unix account and signal definitions
are stubbed on Windows; native system behavior remains covered by Linux's test_cli.py suite.
"""
import importlib.machinery
import importlib.util
import json
import signal
from pathlib import Path
import sys
from types import ModuleType
from unittest.mock import Mock

import pytest


@pytest.fixture
def cli(monkeypatch, tmp_path):
    if sys.platform == "win32":
        monkeypatch.setitem(sys.modules, "pwd", ModuleType("pwd"))
        monkeypatch.setattr(signal, "SIGHUP", 1, raising=False)
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(tmp_path))
    path = Path(__file__).resolve().parents[1] / "bin/herald-os"
    loader = importlib.machinery.SourceFileLoader("madx_entrypoint_test", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


@pytest.mark.parametrize("args", [[], ["help"], ["--help"], ["-h"]])
def test_primary_help_teaches_real_supported_commands(cli, capsys, args):
    assert cli.main(args) == 0
    output = capsys.readouterr().out
    for command in ("help", "setup", "update", "rollback", "install", "hermes-command"):
        assert f"madx {command}" in output
    assert "herald-os" not in output


@pytest.mark.parametrize("args,handler,expected", [
    (["setup"], "setup", ([],)),
    (["setup", "ssh", "--status"], "setup", (["ssh", "--status"],)),
    (["update"], "update", (False,)),
    (["update", "--check"], "update", (True,)),
    (["rollback"], "rollback", ()),
    (["install", "steam"], "catalog", (["install", "steam"],)),
    (["install", "app", "Text", "Editor"], "install_app", ("Text Editor",)),
])
def test_primary_commands_reuse_the_existing_handlers_and_exit_status(cli, monkeypatch, args, handler, expected):
    action = Mock(return_value=17)
    monkeypatch.setattr(cli, handler, action)
    assert cli.main(args) == 17
    action.assert_called_once_with(*expected)


def test_hermes_discovery_preserves_argv_and_managed_requirement(cli, monkeypatch, capsys):
    monkeypatch.setattr(cli, "hermes_install", lambda: ("external", ["/path with space/hermes", "--profile", "work"]))
    assert cli.main(["hermes-command"]) == 0
    assert capsys.readouterr().out.splitlines() == ["/path with space/hermes", "--profile", "work"]
    assert cli.main(["hermes-command", "--managed"]) == 1
    assert capsys.readouterr().out == ""
    monkeypatch.setattr(cli, "hermes_install", lambda: None)
    assert cli.main(["hermes-command"]) == 1


def test_command_catalog_keeps_existing_commands_and_has_no_placeholder_doctor(cli, capsys):
    assert cli.main(["commands", "--json"]) == 0
    commands = {item["name"]: item["help"] for item in json.loads(capsys.readouterr().out)}
    assert {"setup", "update", "rollback", "install", "hermes-command", "password", "docs", "sheets", "canvas", "os"} <= commands.keys()
    assert "doctor" not in commands
    with pytest.raises(SystemExit) as exc:
        cli.main(["doctor"])
    assert exc.value.code == 2
    assert "madx commands" in capsys.readouterr().err


@pytest.mark.parametrize("prefix", ["madx: ", "herald-os: "])
def test_ssh_json_errors_preserve_the_existing_unprefixed_contract(cli, monkeypatch, capsys, prefix):
    def fail(_args):
        print(prefix + "setup ssh: refused test input", file=sys.stderr)
        raise SystemExit(2)
    monkeypatch.setattr(cli, "setup_ssh_run", fail)
    with pytest.raises(SystemExit) as stopped:
        cli.setup_ssh(["--json"])
    assert stopped.value.code == 2
    captured = capsys.readouterr()
    assert json.loads(captured.out)["error"] == "setup ssh: refused test input"
    assert captured.err == ""
