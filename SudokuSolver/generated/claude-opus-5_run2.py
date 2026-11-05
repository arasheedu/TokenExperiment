#!/usr/bin/env python3
"""A Sudoku solver using backtracking search with the MRV heuristic.

Usage:
    python sudoku.py puzzle.txt

The puzzle file must contain 9 lines of 9 characters each.  Digits 1-9 are
given clues; '0' or '.' marks an empty cell.  Blank lines and surrounding
whitespace are ignored.
"""

import sys

DIGITS = range(1, 10)
ALL_MASK = 0b111111111  # bits 0..8 represent digits 1..9


def _box_index(row: int, col: int) -> int:
    return (row // 3) * 3 + (col // 3)


def is_valid_grid(grid) -> bool:
    """Return True if `grid` is a well-formed 9x9 grid with no conflicting clues."""
    if not isinstance(grid, list) or len(grid) != 9:
        return False
    for row in grid:
        if not isinstance(row, list) or len(row) != 9:
            return False
        for value in row:
            if not isinstance(value, int) or isinstance(value, bool):
                return False
            if value < 0 or value > 9:
                return False

    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for r in range(9):
        for c in range(9):
            value = grid[r][c]
            if value == 0:
                continue
            bit = 1 << (value - 1)
            b = _box_index(r, c)
            if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                return False
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
    return True


def solve(grid: list[list[int]]) -> bool:
    """Solve `grid` in place with backtracking + MRV.  Return True on success.

    `grid` is a 9x9 list of lists of ints, where 0 marks an empty cell.
    If the grid is malformed or already contains conflicting clues, False is
    returned and the grid is left untouched.
    """
    if not is_valid_grid(grid):
        return False

    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    empties = []

    for r in range(9):
        for c in range(9):
            value = grid[r][c]
            if value == 0:
                empties.append((r, c))
            else:
                bit = 1 << (value - 1)
                rows[r] |= bit
                cols[c] |= bit
                boxes[_box_index(r, c)] |= bit

    if not empties:
        return True

    def candidates(r: int, c: int) -> int:
        return ALL_MASK & ~(rows[r] | cols[c] | boxes[_box_index(r, c)])

    def backtrack(remaining) -> bool:
        if not remaining:
            return True

        # Minimum Remaining Values: choose the cell with fewest candidates.
        best_pos = -1
        best_mask = 0
        best_count = 10
        for i, (r, c) in enumerate(remaining):
            mask = candidates(r, c)
            count = bin(mask).count("1")
            if count < best_count:
                best_count = count
                best_mask = mask
                best_pos = i
                if count <= 1:
                    break

        if best_count == 0:
            return False

        r, c = remaining[best_pos]
        b = _box_index(r, c)
        rest = remaining[:best_pos] + remaining[best_pos + 1:]

        mask = best_mask
        while mask:
            bit = mask & -mask
            mask ^= bit
            value = bit.bit_length()

            grid[r][c] = value
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit

            if backtrack(rest):
                return True

            rows[r] &= ~bit
            cols[c] &= ~bit
            boxes[b] &= ~bit
            grid[r][c] = 0

        return False

    return backtrack(empties)


def parse_grid(text: str):
    """Parse puzzle text into a 9x9 grid, or return None if malformed."""
    lines = []
    for raw in text.splitlines():
        line = "".join(raw.split())  # strip all whitespace inside the line
        if line:
            lines.append(line)

    if len(lines) != 9:
        return None

    grid = []
    for line in lines:
        if len(line) != 9:
            return None
        row = []
        for ch in line:
            if ch in ".0":
                row.append(0)
            elif ch in "123456789":
                row.append(int(ch))
            else:
                return None
        grid.append(row)
    return grid


def format_grid(grid) -> str:
    return "\n".join("".join(str(v) for v in row) for row in grid)


def main(argv) -> int:
    if len(argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        return 2

    try:
        with open(argv[1], "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print(f"Cannot read {argv[1]}: {exc}", file=sys.stderr)
        return 2

    grid = parse_grid(text)
    if grid is None or not is_valid_grid(grid):
        print("Invalid puzzle")
        return 2

    if not solve(grid):
        print("No solution")
        return 1

    print(format_grid(grid))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
