from __future__ import annotations

from aoc2025.puzzle import Puzzle


DIAL_SIZE = 100
START_POSITION = 50


class Day01(Puzzle):
    """
    Safe dial puzzle.

    Part 1 counts how many times the dial lands on 0 after applying all rotations.
    Part 2 counts every click that lands on 0, even mid-rotation.
    """

    def _apply_move(self, pos: int, direction: str, distance: int) -> int:
        if direction == "L":
            return (pos - distance) % DIAL_SIZE
        if direction == "R":
            return (pos + distance) % DIAL_SIZE
        raise ValueError(f"Unexpected direction {direction!r}")

    def _zero_hits_during_move(self, pos: int, direction: str, distance: int) -> int:
        """
        Count how many clicks land on 0 while moving from `pos` with the given move.
        """

        if direction == "R":
            steps_to_zero = (-pos) % DIAL_SIZE
            if steps_to_zero == 0:
                steps_to_zero = DIAL_SIZE
        elif direction == "L":
            steps_to_zero = pos % DIAL_SIZE
            if steps_to_zero == 0:
                steps_to_zero = DIAL_SIZE
        else:
            raise ValueError(f"Unexpected direction {direction!r}")

        if distance < steps_to_zero:
            return 0
        return 1 + (distance - steps_to_zero) // DIAL_SIZE

    def _simulate_end_hits(self) -> tuple[int, int]:
        """Return (zero_hits_at_rotation_end, final_position)."""

        pos = START_POSITION
        zero_hits = 0
        for line in self.nonempty_lines:
            direction = line[0]
            distance = int(line[1:])
            pos = self._apply_move(pos, direction, distance)
            if pos == 0:
                zero_hits += 1
        return zero_hits, pos

    def _simulate_click_hits(self) -> int:
        """Count all clicks that land on 0 (including ends of rotations)."""

        pos = START_POSITION
        hits = 0
        for line in self.nonempty_lines:
            direction = line[0]
            distance = int(line[1:])
            hits += self._zero_hits_during_move(pos, direction, distance)
            pos = self._apply_move(pos, direction, distance)
        return hits

    def part1(self) -> int:
        zero_hits, _ = self._simulate_end_hits()
        return zero_hits

    def part2(self) -> int:
        return self._simulate_click_hits()


if __name__ == "__main__":
    Day01.cli()
