from __future__ import annotations

from aoc2025.days.day01 import Day01


EXAMPLE = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


def test_part1_counts_zero_hits() -> None:
    puzzle = Day01(raw_input=EXAMPLE)
    assert puzzle.part1() == 3


def test_part2_counts_all_zero_clicks() -> None:
    puzzle = Day01(raw_input=EXAMPLE)
    assert puzzle.part2() == 6


def test_part2_counts_multiple_wraps() -> None:
    puzzle = Day01(raw_input="R1000\n")  # 10 full spins from 50
    assert puzzle.part2() == 10


def test_part2_counts_single_wrap_left() -> None:
    puzzle = Day01(raw_input="L55\n")  # crosses zero once
    assert puzzle.part2() == 1
