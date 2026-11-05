#!/usr/bin/env python3
"""A simple Sudoku solver using backtracking with MRV heuristic."""

import sys


def parse_grid(text: str):
    """Parse puzzle text into a 9x9 grid of ints (0 for empty).

    Raises ValueError on malformed input.
    """
    lines = [line.strip().replace(" ", "") for line in text.splitlines()]
    lines = [line for line in lines if line != ""]

    if len(lines) != 9:
        raise ValueError("Expected 9 non-blank lines")

    grid = []
    for line in lines:
        if len(line) != 9:
            raise ValueError("Each line must have exactly 9 characters")
        row = []
        for ch in line:
            if ch in "123456789":
                row.append(int(ch))
            elif ch in "0.":
                row.append(0)
            else:
                raise ValueError(f"Invalid character in puzzle: {ch!r}")
        grid.append(row)
    return grid


def has_initial_conflict(grid) -> bool:
    """Return True if the given clues already violate Sudoku rules."""
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9

    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v == 0:
                continue
            bit = 1 << (v - 1)
            b = (r // 3) * 3 + (c // 3)
            if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                return True
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
    return False


def solve(grid: list) -> bool:
    """Solve the given 9x9 grid in place using backtracking with MRV.

    grid: list of 9 lists of 9 ints (0 = empty cell).
    Returns True if solved successfully, False if unsolvable
    (including cases where the grid as given is already invalid).
    """
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    empties = []

    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                bit = 1 << (v - 1)
                b = (r // 3) * 3 + (c // 3)
                if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                    return False
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit
            else:
                empties.append((r, c))

    def backtrack(remaining) -> bool:
        if not remaining:
            return True

        # Find the empty cell with fewest candidates (MRV).
        best_idx = -1
        best_cands = None

        for i, (r, c) in enumerate(remaining):
            b = (r // 3) * 3 + (c // 3)
            used = rows[r] | cols[c] | boxes[b]
            cands = [d for d in range(1, 10) if not used & (1 << (d - 1))]
            if best_cands is None or len(cands) < len(best_cands):
                best_cands = cands
                best_idx = i
                if len(cands) <= 1:
                    break

        if not best_cands:
            return False

        r, c = remaining[best_idx]
        b = (r // 3) * 3 + (c // 3)
        new_remaining = remaining[:best_idx] + remaining[best_idx + 1:]

        for d in best_cands:
            bit = 1 << (d - 1)
            grid[r][c] = d
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit

            if backtrack(new_remaining):
                return True

            grid[r][c] = 0
            rows[r] &= ~bit
            cols[c] &= ~bit
            boxes[b] &= ~bit

        return False

    return backtrack(empties)


def format_grid(grid) -> str:
    return "\n".join("".join(str(v) for v in row) for row in grid)


def main(argv):
    if len(argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        sys.exit(2)

    path = argv[1]

    try:
        with open(path, "r") as f:
            text = f.read()
    except OSError as e:
        print(f"Could not read file: {e}", file=sys.stderr)
        sys.exit(2)

    try:
        grid = parse_grid(text)
    except ValueError:
        print("Invalid puzzle")
        sys.exit(2)

    if has_initial_conflict(grid):
        print("Invalid puzzle")
        sys.exit(2)

    if solve(grid):
        print(format_grid(grid))
    else:
        print("No solution")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
