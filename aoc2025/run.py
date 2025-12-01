from __future__ import annotations

import importlib
import argparse
from typing import Type

from aoc2025.puzzle import Puzzle


def load_day(day_tag: str) -> Type[Puzzle]:
    """
    Dynamically import a day module and return its Puzzle subclass.

    Expects modules named ``aoc2025.days.dayXX`` containing a class named
    ``DayXX``. The numeric portion should be zero-padded to two digits.
    """

    module_name = f"aoc2025.days.day{day_tag}"
    class_name = f"Day{day_tag}"
    module = importlib.import_module(module_name)
    puzzle_cls = getattr(module, class_name, None)
    if puzzle_cls is None:
        raise ImportError(f"{class_name} not found in {module_name}")
    if not issubclass(puzzle_cls, Puzzle):
        raise TypeError(f"{class_name} is not a Puzzle subclass")
    return puzzle_cls


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run an Advent of Code 2025 day (e.g., python -m aoc2025.run 01)"
    )
    parser.add_argument("day", help="Day number, zero-padded (e.g., 01, 12, 25)")
    parser.add_argument(
        "--part",
        "-p",
        choices=["1", "2", "both"],
        default="both",
        help="Select which part to run",
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        help="Optional path to an input file (defaults to inputs/<day>.txt)",
    )
    args = parser.parse_args()

    puzzle_cls = load_day(args.day)
    puzzle = puzzle_cls(input_path=args.input)
    result = puzzle.run(part=args.part)
    puzzle.print_results(result)


if __name__ == "__main__":
    main()
