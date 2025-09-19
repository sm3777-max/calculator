# tests/test_core.py
import pytest
from calculator.core import (
    parse_number, add, subtract, multiply, divide,
    perform_operation, CalculatorError
)

@pytest.mark.parametrize("input_str,expected", [
    ("1", 1.0),
    (" 2.5 ", 2.5),
    ("-3", -3.0),
    ("0", 0.0),
])
def test_parse_number_valid(input_str, expected):
    assert parse_number(input_str) == expected

@pytest.mark.parametrize("bad", ["", "   ", "abc", None])
def test_parse_number_invalid(bad):
    with pytest.raises(CalculatorError):
        parse_number(bad)

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (2.5, 3.5, 6.0)
])
def test_add(a, b, expected):
    assert add(a, b) == expected

def test_subtract():
    assert subtract(5, 3) == 2

def test_multiply():
    assert multiply(3, 4) == 12

def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(CalculatorError):
        divide(1, 0)

@pytest.mark.parametrize("op,left,right,expected", [
    ("add", "1", "2", 3.0),
    ("+", "2", "3", 5.0),
    ("sub", "5", "2", 3.0),
    ("-", "5", "2", 3.0),
    ("mul", "3", "4", 12.0),
    ("*", "3", "4", 12.0),
    ("div", "8", "2", 4.0),
    ("/", "8", "2", 4.0),
])
def test_perform_operation_param(op, left, right, expected):
    _, result = perform_operation(op, left, right)
    assert result == expected

def test_perform_operation_unknown():
    with pytest.raises(CalculatorError):
        perform_operation("pow", "2", "3")
