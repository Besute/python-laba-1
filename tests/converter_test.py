from decimal import Decimal
from decimal import getcontext
from pathlib import Path

import pytest

from toolkit.auxiliary_functions import load_data
from toolkit.converter import convert
from toolkit.errors import InvalidValueError

JSON_FILE = Path(__file__).parent.parent / "src" / "toolkit" / "calculator_config.json"

CALC_CONFIG = load_data(JSON_FILE)
PRECISION = CALC_CONFIG["precision"]
getcontext().prec = PRECISION


def test_1():
    assert convert(1000, "g", "kg") == Decimal(1)


def test_2():
    with pytest.raises(InvalidValueError):
        convert(1000, "m", "kg")


def test_3():
    assert convert(1500, "g", "kg") == Decimal("1.5")


def test_4():
    assert convert(Decimal("3.5555"), "kg", "g") == Decimal("3555.5")


def test_5():
    with pytest.raises(InvalidValueError):
        convert(-280, "c", "f")


def test_6():
    assert convert(0, "c", "k") == Decimal(273) + Decimal("0.15")


def test_7():
    assert convert(100, "cm", "m") == Decimal(1)


def test_8():
    with pytest.raises(InvalidValueError):
        convert(-100, "cm", "m")


def test_9():
    with pytest.raises(InvalidValueError):
        convert(-50, "kg", "g")


def test_10():
    assert convert(500, "f", "c") == Decimal(260)


def test_11():
    assert convert(260, "c", "f") == Decimal(500)


def test_12():
    with pytest.raises(InvalidValueError):
        convert(0, "c", "i")


def test_13():
    with pytest.raises(InvalidValueError):
        convert(0, "g", "c")


def test_14():
    with pytest.raises(InvalidValueError):
        convert(0, "u", "kg")


def test_15():
    with pytest.raises(InvalidValueError):
        convert(-4, "m", "cm")


def test_16():
    assert convert(1000, "m", "km") == Decimal(1)
