from __future__ import annotations

import argparse
import inspect
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "inputs"


@dataclass(slots=True)
class RunResult:
    """Container for outputs from a puzzle run."""

    part1: Any | None = None
    part2: Any | None = None
    part1_time: float | None = None
    part2_time: float | None = None


class Puzzle:
    """
    Base class for each Advent of Code day.

    The class figures out which input file to load by looking for the first
    numeric portion of the module's filename (``day01.py`` -> ``01``) and
    reading ``inputs/<tag>.txt``. You can override that by passing a custom
    path or raw text.
    """

    def __init__(self, input_path: Path | None = None, raw_input: str | None = None) -> None:
        self.module_file = Path(inspect.getfile(self.__class__)).resolve()
        self.day_tag = self._derive_day_tag(self.module_file)
        self.input_path = Path(input_path) if input_path is not None else self.default_input_path()

        if raw_input is not None:
            self.input_text = raw_input.rstrip("\n")
        else:
            self.input_text = self._read_input()

    # --- Class helpers -------------------------------------------------
    @classmethod
    def cli(cls) -> None:
        """
        Command-line entrypoint for a day module.

        Provides ``--input`` to override the detected file and ``--part`` to run
        only one half of the puzzle.
        """

        parser = argparse.ArgumentParser(description=cls.__doc__)
        parser.add_argument(
            "--input",
            "-i",
            type=Path,
            help="Optional path to an input file (defaults to inputs/<day>.txt)",
        )
        parser.add_argument(
            "--part",
            "-p",
            choices=["1", "2", "both"],
            default="both",
            help="Select which part to run",
        )
        args = parser.parse_args()

        puzzle = cls(input_path=args.input)
        results = puzzle.run(part=args.part)
        puzzle.print_results(results)

    # --- Input handling ------------------------------------------------
    @staticmethod
    def _derive_day_tag(module_path: Path) -> str:
        """
        Pull the first numeric component from a module path.

        ``Day00.py`` -> ``01``
        ``02.py`` -> ``02``
        """

        match = re.search(r"(\d+)", module_path.stem)
        if not match:
            raise ValueError(f"Could not determine day number from {module_path.name}")
        return match.group(1)

    def default_input_path(self) -> Path:
        """Return the default input file path for this puzzle."""

        return INPUT_DIR / f"{self.day_tag}.txt"

    def _read_input(self) -> str:
        """Read and return puzzle input as a single string."""

        if not self.input_path.exists():
            raise FileNotFoundError(
                f"No input file found for day {self.day_tag} at {self.input_path}"
            )
        return self.input_path.read_text(encoding="utf-8").rstrip("\n")

    # --- Convenience properties ---------------------------------------
    @property
    def lines(self) -> list[str]:
        """Input split into lines."""

        return self.input_text.splitlines()

    @property
    def nonempty_lines(self) -> list[str]:
        """Input split into non-empty lines."""

        return [line for line in self.lines if line.strip()]

    @property
    def ints(self) -> list[int]:
        """All integers found in the input, in order."""

        return [int(x) for x in re.findall(r"-?\d+", self.input_text)]

    # --- Solving -------------------------------------------------------
    def part1(self) -> Any:
        raise NotImplementedError

    def part2(self) -> Any:
        raise NotImplementedError

    def run(self, *, part: str = "both") -> RunResult:
        """Execute part1/part2 based on the selected option."""

        result = RunResult()
        if part in {"1", "both"}:
            start = time.perf_counter()
            result.part1 = self.part1()
            result.part1_time = time.perf_counter() - start
        if part in {"2", "both"}:
            start = time.perf_counter()
            result.part2 = self.part2()
            result.part2_time = time.perf_counter() - start
        return result

    # --- Output --------------------------------------------------------
    def print_results(self, result: RunResult) -> None:
        """Pretty-print part outputs."""

        if result.part1 is not None:
            suffix = (
                f" ({self._format_duration(result.part1_time)})"
                if result.part1_time is not None
                else ""
            )
            print(f"Part 1: {result.part1}{suffix}")
        if result.part2 is not None:
            suffix = (
                f" ({self._format_duration(result.part2_time)})"
                if result.part2_time is not None
                else ""
            )
            print(f"Part 2: {result.part2}{suffix}")

    @staticmethod
    def _format_duration(seconds: float) -> str:
        """Format a duration into a compact human-readable string."""

        if seconds >= 1:
            return f"{seconds:.3f}s"
        millis = seconds * 1_000
        if millis >= 1:
            return f"{millis:.2f}ms"
        micros = seconds * 1_000_000
        if micros >= 1:
            return f"{micros:.0f}µs"
        nanos = seconds * 1_000_000_000
        return f"{nanos:.0f}ns"


# def batched(iterable: Iterable[Any], size: int) -> Iterable[list[Any]]:
#     """Yield fixed-size batches from an iterable."""

#     batch: list[Any] = []
#     for item in iterable:
#         batch.append(item)
#         if len(batch) == size:
#             yield batch
#             batch = []
#     if batch:
#         yield batch
