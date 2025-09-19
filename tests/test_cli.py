def test_running_module_as_main_calls_repl(monkeypatch, capsys):
    # Simulate immediate EOF so the repl exits right away
    def raise_eof(prompt):
        raise EOFError
    monkeypatch.setattr('builtins.input', raise_eof)

    import sys, runpy

    # Remove any existing references to the package/module so run_module runs cleanly
    popped = {}
    for name in ("calculator.cli", "calculator"):
        if name in sys.modules:
            popped[name] = sys.modules.pop(name)

    try:
        runpy.run_module("calculator.cli", run_name="__main__")
    finally:
        # restore original modules so other tests are unaffected
        sys.modules.update(popped)

    captured = capsys.readouterr()
    assert "Welcome to the calculator." in captured.out or "Goodbye." in captured.out
# Additional CLI tests to cover print_help and repl branches
import runpy
import sys

def test_print_help_outputs_text(capsys):
    # cover print_help() (lines 7-13)
    from calculator import cli
    cli.print_help()
    captured = capsys.readouterr()
    assert "Simple command-line calculator." in captured.out
    assert "Usage: <operation> <number1> <number2>" in captured.out

def test_repl_handles_eof(monkeypatch, capsys):
    # Simulate EOFError on first input; REPL prints Goodbye and exits
    def raise_eof(prompt):
        raise EOFError
    monkeypatch.setattr('builtins.input', raise_eof)
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Goodbye." in captured.out

def test_repl_handles_keyboard_interrupt(monkeypatch, capsys):
    # Simulate KeyboardInterrupt on first input; REPL prints Goodbye and exits
    def raise_kb(prompt):
        raise KeyboardInterrupt
    monkeypatch.setattr('builtins.input', raise_kb)
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Goodbye." in captured.out

def test_repl_blank_line_then_exit(monkeypatch, capsys):
    # blank line should be ignored, then exit prints Exiting.
    inputs = iter(["", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Exiting." in captured.out

def test_repl_help_then_exit(monkeypatch, capsys):
    # help should call print_help and then exit
    inputs = iter(["help", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Simple command-line calculator." in captured.out
    assert "Exiting." in captured.out

def test_repl_bad_token_count(monkeypatch, capsys):
    # 'hello' -> triggers "expected 3 tokens" message, then exit
    inputs = iter(["hello", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "expected 3 tokens" in captured.out

def test_repl_successful_operation(monkeypatch, capsys):
    # simple successful operation via CLI
    inputs = iter(["add 2 3", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out

def test_repl_divide_by_zero_shows_error(monkeypatch, capsys):
    # CLI should show division-by-zero error message
    inputs = iter(["div 10 0", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Division by zero" in captured.out or "Division by zero is not allowed" in captured.out

def test_running_module_as_main_calls_repl(monkeypatch, capsys):
    # Run calculator.cli as __main__ while avoiding RuntimeWarning by popping modules first.
    def raise_eof(prompt):
        raise EOFError
    monkeypatch.setattr('builtins.input', raise_eof)

    popped = {}
    for name in ("calculator.cli", "calculator"):
        if name in sys.modules:
            popped[name] = sys.modules.pop(name)

    try:
        runpy.run_module("calculator.cli", run_name="__main__")
    finally:
        sys.modules.update(popped)

    captured = capsys.readouterr()
    assert "Welcome to the calculator." in captured.out or "Goodbye." in captured.out
# Extra CLI tests to exercise aliases, whitespace, invalid numbers, quit alias, and help aliases
def test_repl_quit_alias(monkeypatch, capsys):
    inputs = iter(["quit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Exiting." in captured.out

def test_repl_help_aliases_h_and_question(monkeypatch, capsys):
    # test 'h' and '?'
    inputs = iter(["h", "?", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Simple command-line calculator." in captured.out

def test_repl_operation_aliases_and_case_insensitive(monkeypatch, capsys):
    # test variety of op aliases and uppercase, whitespace
    cases = [
        ("plus 1 2", "Result: 3.0"),
        ("times 2 3", "Result: 6.0"),
        ("x 4 2", "Result: 8.0"),
        ("mul 3 5", "Result: 15.0"),
        ("minus 5 2", "Result: 3.0"),
        ("ADD   2    3", "Result: 5.0"),         # uppercase and extra whitespace
        ("  add  2  3  ", "Result: 5.0"),        # leading/trailing whitespace
    ]
    # run all cases in sequence then exit
    inputs = iter([c for c, _ in cases] + ["exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    for _, expected in cases:
        assert expected in captured.out

def test_repl_invalid_number_shows_error(monkeypatch, capsys):
    inputs = iter(["add abc 2", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Invalid number" in captured.out or "Invalid number:" in captured.out

def test_repl_negative_and_float_numbers(monkeypatch, capsys):
    inputs = iter(["add -1.5 2.5", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Result: 1.0" in captured.out

def test_repl_multiple_errors_and_recovery(monkeypatch, capsys):
    # bad token count, then invalid number, then valid op, then exit
    inputs = iter(["hello", "add 1", "add a b", "add 1 2", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "expected 3 tokens" in captured.out
    assert "Invalid number" in captured.out
    assert "Result: 3.0" in captured.out
# Extensive CLI tests to cover all branches in calculator/cli.py

import runpy
import sys

def test_print_help_outputs_text(capsys):
    from calculator import cli
    cli.print_help()
    captured = capsys.readouterr()
    assert "Simple command-line calculator." in captured.out
    assert "Usage: <operation> <number1> <number2>" in captured.out

def test_repl_eof_exits(monkeypatch, capsys):
    def raise_eof(prompt):
        raise EOFError
    monkeypatch.setattr('builtins.input', raise_eof)
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Goodbye." in captured.out

def test_repl_keyboard_interrupt_exits(monkeypatch, capsys):
    def raise_kb(prompt):
        raise KeyboardInterrupt
    monkeypatch.setattr('builtins.input', raise_kb)
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Goodbye." in captured.out

def test_repl_blank_line_then_exit(monkeypatch, capsys):
    inputs = iter(["", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Exiting." in captured.out

def test_repl_help_aliases(monkeypatch, capsys):
    inputs = iter(["help", "h", "?", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Simple command-line calculator." in captured.out

def test_repl_quit_alias(monkeypatch, capsys):
    inputs = iter(["quit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Exiting." in captured.out

def test_repl_bad_token_count(monkeypatch, capsys):
    inputs = iter(["hello", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "expected 3 tokens" in captured.out

def test_repl_invalid_number(monkeypatch, capsys):
    inputs = iter(["add abc 2", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Invalid number" in captured.out

def test_repl_divide_by_zero(monkeypatch, capsys):
    inputs = iter(["div 10 0", "exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    assert "Division by zero" in captured.out or "Division by zero is not allowed" in captured.out

def test_repl_success_cases_and_aliases(monkeypatch, capsys):
    cases = [
        ("add 2 3", "Result: 5.0"),
        ("+ 4 1", "Result: 5.0"),
        ("sub 5 2", "Result: 3.0"),
        ("- 6 1", "Result: 5.0"),
        ("mul 3 3", "Result: 9.0"),
        ("* 2 3", "Result: 6.0"),
        ("times 2 5", "Result: 10.0"),
        ("x 2 3", "Result: 6.0"),
        ("div 9 3", "Result: 3.0"),
        ("/ 8 2", "Result: 4.0"),
        ("ADD   2    3", "Result: 5.0"),  # whitespace & case
        ("  add  2  3  ", "Result: 5.0"), # extra whitespace edges
    ]
    inputs = iter([c for c, _ in cases] + ["exit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    from calculator import cli
    cli.repl()
    captured = capsys.readouterr()
    for _, expected in cases:
        assert expected in captured.out

def test_repl_run_module_as_main(monkeypatch, capsys):
    # run the module as __main__ after removing any imported modules
    def raise_eof(prompt):
        raise EOFError
    monkeypatch.setattr('builtins.input', raise_eof)

    popped = {}
    for name in ("calculator.cli", "calculator"):
        if name in sys.modules:
            popped[name] = sys.modules.pop(name)
    try:
        runpy.run_module("calculator.cli", run_name="__main__")
    finally:
        sys.modules.update(popped)

    captured = capsys.readouterr()
    assert "Welcome to the calculator." in captured.out or "Goodbye." in captured.out
