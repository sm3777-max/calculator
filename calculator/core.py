# calculator/core.py
from typing import Tuple

class CalculatorError(Exception):
    """Custom exception for calculator errors."""
    pass

def parse_number(value: str) -> float:
    """Parse string to float with validation."""
    if value is None:
        raise CalculatorError("No value provided")
    s = value.strip()
    if s == "":
        raise CalculatorError("Empty input")
    try:
        return float(s)
    except ValueError:
        raise CalculatorError(f"Invalid number: {value!r}")

def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise CalculatorError("Division by zero is not allowed")
    return a / b

def perform_operation(op: str, left: str, right: str) -> Tuple[str, float]:
    """
    op: operation string (e.g., 'add', '+', 'mul', '*', etc.)
    left/right: raw string inputs
    Returns: (operation_key, result)
    """
    l = parse_number(left)
    r = parse_number(right)
    op_map = {
        "add": add, "+": add, "plus": add,
        "sub": subtract, "-": subtract, "minus": subtract,
        "mul": multiply, "*": multiply, "x": multiply, "times": multiply,
        "div": divide, "/": divide, "divide": divide
    }
    key = op.strip().lower()
    if key not in op_map:
        raise CalculatorError(f"Unknown operation: {op}")
    func = op_map[key]
    return key, func(l, r)
