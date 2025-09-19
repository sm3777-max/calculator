# tests/test_cli.py
from calculator import cli

def test_repl_help_and_exit(monkeypatch, capsys):
    inputs = iter(["help", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    cli.repl()
    captured = capsys.readouterr()
    assert "Simple command-line calculator" in captured.out
    assert "Exiting." in captured.out

def test_repl_operation(monkeypatch, capsys):
    inputs = iter(["add 2 3", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    cli.repl()
    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out
