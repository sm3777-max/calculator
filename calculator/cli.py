# calculator/cli.py
from calculator.core import perform_operation, CalculatorError

PROMPT = "calc> "

def print_help():
    print("Simple command-line calculator.")
    print("Commands: add|+  sub|-  mul|*  div|/  help  exit")
    print("Usage: <operation> <number1> <number2>")
    print("Examples:")
    print("  add 2 3")
    print("  * 4 5")
    print("  div 10 2")

def repl():
    print("Welcome to the calculator. Type 'help' or 'exit'.")
    while True:
        try:
            raw = input(PROMPT)
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not raw or raw.strip() == "":
            continue

        parts = raw.strip().split()
        cmd = parts[0].lower()

        if cmd in ("exit", "quit"):
            print("Exiting.")
            break
        if cmd in ("help", "h", "?"):
            print_help()
            continue

        if len(parts) != 3:
            print("Error: expected 3 tokens: <operation> <num1> <num2>")
            continue

        operation, a_str, b_str = parts
        try:
            _, result = perform_operation(operation, a_str, b_str)
            print(f"Result: {result}")
        except CalculatorError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    repl()
