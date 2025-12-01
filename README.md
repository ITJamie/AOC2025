# Advent of Code 2025

Python-friendly class for solving Advent of Code 2025. Each day lives in `aoc2025/days/dayXX.py`, inherits a shared base class, and reads its input from `inputs/XX.txt`.

## Layout
- `aoc2025/puzzle.py`: shared `Puzzle` base class that handles input discovery, CLI, and common helpers.
- `aoc2025/days/day01.py`: sample day implementation.
- `inputs/`: put your real puzzle inputs here (e.g., `inputs/03.txt`).
- `examples/inputs/`: AoC-provided small examples, one per part (e.g., `01_part1_example.txt`).
- `examples/outputs/`: expected answers for each example input for reference (e.g., `01_part1_example.txt`).
- `tests/`: pytest suite per day.

## Usage
Run a day module directly:
```bash
python -m aoc2025.days.day01             # runs both parts using inputs/01.txt
python -m aoc2025.days.day01 --part 1    # run a single part
python -m aoc2025.days.day01 -i my.txt   # point at a different input file
# or use the central runner
python -m aoc2025.run 01
```

Adding a new day:
1. Copy `aoc2025/days/day01.py` to `aoc2025/days/dayXX.py` and update the class name (e.g., `Day05`).
2. Drop your input in `inputs/XX.txt`.
3. Save the official examples and answers in `examples/inputs/XX_part1_example.txt`, `examples/outputs/XX_part1_example.txt`, and similarly for part 2.
4. Override `part1`/`part2` in the new class.
5. Add a matching test module in `tests/test_dayXX.py`.

## Testing
Install dev deps and run pytest:
```bash
python -m pip install -r requirements.txt
pytest
```
