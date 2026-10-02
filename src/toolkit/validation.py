from .constants import REAL_OPERANDS
from .errors import InvalidExpressionError
from .errors import InvalidValueError


def validation_calc(expression):
    empty_expression = True
    correct_expression = True
    for i in "0123456789":
        if i in expression:
            empty_expression = False
            break
    for i in expression:
        if i not in REAL_OPERANDS and i not in "0123456789 .,":
            correct_expression = False
            break
    if not (correct_expression):
        raise InvalidExpressionError("Your expression has unsupported symbols")
    if empty_expression:
        raise InvalidExpressionError("Your expression is empty or doesn't make any sense")


def validation_conv(num):
    for i in num:
        if i not in "0123456789.-+":
            raise InvalidValueError("You have error in your number")
