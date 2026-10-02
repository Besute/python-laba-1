import subprocess
import sys

from decimal import Decimal


def test_convert_success():
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "convert", "1", "--from", "m", "--to", "cm"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == "The 1m is 100cm\n"
    assert result.stderr == ""


def test_convert_success_kelvin_to_celsius():
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "convert", "273.15", "--from", "k", "--to", "c"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == f"The 273.15k is {Decimal(27315) / Decimal(100) - Decimal(27315) / Decimal(100)}c\n"
    assert result.stderr == ""


def test_convert_below_absolute_zero():
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "convert", "-600", "--from", "c", "--to", "k"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "You have temperature below absolute zero\n" in result.stderr


def test_convert_invalid_units():
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "convert", "1", "--from", "adads", "--to", "VVV"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "You can't convert adads to VVV\n" in result.stderr


def test_convert_kg_to_g():
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "convert", "5.5555", "--from", "kg", "--to", "g"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == f"The 5.5555kg is {Decimal(55555) / Decimal(10000) * Decimal(1000)}g\n"
    assert result.stderr == ""
