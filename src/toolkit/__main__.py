import argparse
import sys

from pathlib import Path

from .auxiliary_functions import save_data
from .auxiliary_functions import save_history
from .calculator import calculate
from .converter import convert
from .errors import DivisionByZeroError
from .errors import InvalidExpressionError
from .errors import InvalidValueError

DATA_DIR = Path(__file__).resolve().parent
JSON_FILE = DATA_DIR / "calculator_config.json"
JSON_FILE_HISTORY = DATA_DIR / "history.json"


def build_parser():
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="This program calculates the result of a given expression or convert one measure to another",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    calc_parser = subparsers.add_parser("calc", help="calculates given expression")
    calc_parser.add_argument("value", help="expression", type=str)

    convert_parser = subparsers.add_parser("convert", help="convert one measure to another")
    convert_parser.add_argument("value", help="your initial value of 'from' unit", type=str)
    convert_parser.add_argument("--from", dest="from_unit", required=True, help="from unit", type=str)
    convert_parser.add_argument("--to", dest="to_unit", required=True, help="to unit", type=str)

    precision_parser = subparsers.add_parser("setprecision", help="set precision of the calc expression")
    precision_parser.add_argument("value", help="value of precision", type=int)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "calc":
            result = calculate(args.value)
            save_history(
                {
                    "operation": "calculation",
                    "result": str(result),
                    "expression": args.value,
                },
                JSON_FILE_HISTORY,
            )
            print("Result of your expression:", result)
        elif args.command == "convert":
            result = convert(args.value, args.from_unit, args.to_unit)
            save_history(
                {
                    "operation": "convertion",
                    "result": str(result),
                    "value": str(args.value),
                    "from": args.from_unit,
                    "to": args.to_unit,
                },
                JSON_FILE_HISTORY,
            )
            print(f"The {args.value}{args.from_unit} is {result}{args.to_unit}")
        elif args.command == "setprecision":
            print(f"You set your current precision to {args.value}")
            save_history(
                {
                    "operation": "setprecision",
                    "to": args.value,
                },
                JSON_FILE_HISTORY,
            )
            save_data(
                {
                    "precision": args.value,
                },
                JSON_FILE,
            )

    except InvalidExpressionError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    except InvalidValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    except DivisionByZeroError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
