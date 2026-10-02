import json

from decimal import Decimal
from decimal import getcontext
from pathlib import Path

from .auxiliary_functions import load_data
from .errors import InvalidValueError
from .validation import validation_conv

JSON_FILE = Path(__file__).parent / "converts.json"
JSON_FILE_2 = Path(__file__).parent / "calculator_config.json"
LENGTH_TO_M = {}
CALC_CONFIG = load_data(JSON_FILE_2)
PRECISION = CALC_CONFIG["precision"]


def load_conversions():
    with open(JSON_FILE, "r") as file:
        return json.load(file, parse_float=Decimal)


convers = load_conversions()


def execute_length(val, from_, to_):
    convert_to_m = Decimal(convers["length_to_m"][from_]) * val
    convert_to_goal = Decimal(convers["m_to_length"][to_]) * convert_to_m
    return Decimal(convert_to_goal)


def execute_mass(val, from_, to_):
    convert_to_g = Decimal(convers["mass_to_g"][from_]) * val
    convert_to_goal = Decimal(convers["g_to_mass"][to_]) * convert_to_g
    return Decimal(convert_to_goal)


def execute_temper(val, from_, to_):
    convert_to_c = (Decimal(str(convers[from_]["c"]["inside_offset"])) + Decimal(str(val))) * Decimal(
        convers[from_]["c"]["chisl"]
    ) / Decimal(convers[from_]["c"]["znam"]) + Decimal(str(convers[from_]["c"]["offset"]))
    convert_to_goal = (Decimal(str(convers["c"][to_]["inside_offset"])) + convert_to_c) * Decimal(
        convers["c"][to_]["chisl"]
    ) / Decimal(convers["c"][to_]["znam"]) + Decimal(str(convers["c"][to_]["offset"]))
    return Decimal(convert_to_goal)


def evaluate_from(val, from_, to_):
    if from_ in ["km", "m", "cm", "mm"] and to_ in ["km", "m", "cm", "mm"]:
        if val < 0:
            raise InvalidValueError("Length can't be negative")
        return Decimal(execute_length(val, from_, to_))
    elif from_ in ["g", "kg"] and to_ in ["kg", "g"]:
        if val < 0:
            raise InvalidValueError("Mass can't be negative")
        return Decimal(execute_mass(val, from_, to_))
    elif from_ in ["c", "f", "k"] and to_ in ["c", "f", "k"]:
        total_temp = execute_temper(val, from_, to_)
        total_zero = execute_temper(0, "k", to_)
        if total_zero > total_temp:
            raise InvalidValueError("You have temperature below absolute zero")
        return Decimal(total_temp)
    raise InvalidValueError(f"You can't convert {from_} to {to_}")


def convert(val, from_, to_):
    getcontext().prec = PRECISION
    validation_conv(str(val).replace(",", "."))
    return evaluate_from(Decimal(str(val).replace(",", ".")), from_, to_)
