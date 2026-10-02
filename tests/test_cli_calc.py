import subprocess
import sys


def test_calc_success():
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc", "+2+2"], capture_output=True, text=True, check=False
    )

    assert result.returncode == 0
    assert result.stdout == "Result of your expression: 4\n"


def test_calc_invalid_expression():
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc", "+2+ 2-"], capture_output=True, text=True, check=False
    )

    assert result.returncode == 1
    assert "Probably you have error in your expression\n" in result.stderr


def test_calc_division_by_zero():
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc", "2+2/(2-2)"], capture_output=True, text=True, check=False
    )

    assert result.returncode == 1
    assert "You devised by zero" in result.stderr


def test_calc_single_number():
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc", "15"], capture_output=True, text=True, check=False
    )

    assert result.returncode == 0
    assert result.stdout == "Result of your expression: 15\n"


def test_calc_unsupported_symbols():
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "calc", "15 * 13c"], capture_output=True, text=True, check=False
    )

    assert result.returncode == 1
    assert "Your expression has unsupported symbols\n" in result.stderr


def test_calc_empty_expression():
    result = subprocess.run([sys.executable, "-m", "toolkit", "calc", "*"], capture_output=True, text=True, check=False)

    assert result.returncode == 1
    assert "Your expression is empty or doesn't make any sense\n" in result.stderr
