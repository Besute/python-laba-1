import decimal

from decimal import getcontext
from pathlib import Path

from .auxiliary_functions import is_int
from .auxiliary_functions import is_oper
from .auxiliary_functions import load_data
from .constants import HAHAHA_CONST
from .errors import DivisionByZeroError
from .errors import InvalidExpressionError
from .errors import InvalidValueError
from .tokenization import tokenize_expression
from .validation import validation

JSON_FILE = Path(__file__).parent / "calculator_config.json"
CALC_CONFIG = load_data(JSON_FILE)
PRECISION = CALC_CONFIG["precision"]


def make_operation(first, second, op):
    if op == "*":
        return first * second
    elif op == "/":
        if second == 0:
            raise DivisionByZeroError("You devised by zero")
        return first / second
    elif op == "-":
        return first - second
    elif op == "+":
        return first + second
    elif op == "%":
        if second == 0:
            raise DivisionByZeroError("You devised by zero")
        return abs(first) % abs(second)
    elif op == "№":
        if second == 0:
            raise DivisionByZeroError("You devised by zero")
        if is_int(first) and is_int(second):
            minus = 1
            if first < 0:
                minus = minus * -1
            if second < 0:
                minus = minus * -1
            return abs(first) // abs(second) * minus
        else:
            raise InvalidValueError("You can't divide evenly float number ")
    return HAHAHA_CONST


def make_unar(first, op):
    if op == "!":
        return -1 * first
    if op == "?":
        return first
    return HAHAHA_CONST


def execute(expr):
    """
    Counts final expression
    """
    stack = []
    for i in range(len(expr)):
        if expr[i] in "?!":
            op = expr[i]
            first = stack.pop()
            res = str(make_unar(decimal.Decimal(first), op))
            stack.append(res)
        elif is_oper(expr[i]):
            if len(stack) < 2:
                raise InvalidExpressionError("Probably you have error in your expression")
            second = stack.pop()
            first = stack.pop()
            res = make_operation(decimal.Decimal(first), decimal.Decimal(second), expr[i])
            stack.append(str(res))
        else:
            stack.append(expr[i])
    if len(stack) > 1:
        raise InvalidExpressionError("Probably you have error in your expression")
    return stack[0]


def calculate(expression):
    getcontext().prec = PRECISION
    validation(expression)
    expr = tokenize_expression(expression)
    res = execute(expr)
    return decimal.Decimal(res)
