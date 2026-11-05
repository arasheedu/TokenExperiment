#!/usr/bin/env python3
"""Sudoku solver using backtracking search with the MRV heuristic.

Usage: python sudoku.py puzzle.txt
"""

import sys

ALL_DIGITS = 0x3FE  # bits 1..9 set


def solve(grid: list[list[int]]) -> bool:
    """Solve the Sudoku grid in place. Return True on success, else False.

    If no solution exists (or the given clues conflict), the grid is left
    unchanged and False is returned.
    """
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        return False

    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9

    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if not isinstance(v, int) or v < 0 or v > 9:
                return False
            if v:
                bit = 1 << v
                b = (r // 3) * 3 + c // 3
                if (rows[r] | cols[c] | boxes[b]) & bit:
                    return False
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit

    def search() -> bool:
        best = None
        best_cands = 0
        best_count = 10

        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    b = (r // 3) * 3 + c // 3
                    cands = ~(rows[r] | cols[c] | boxes[b]) & ALL_DIGITS
                    count = bin(cands).count("1")
                    if count == 0:
                        return False
                    if count < best_count:
                        best_count = count
                        best = (r, c, b)
                        best_cands = cands
                        if count == 1:
                            break
            if best_count == 1:
                break

        if best is None:
            return True  # no empty cells: solved

        r, c, b = best
        cands = best_cands
        while cands:
            bit = cands & -cands
            cands ^= bit
            v = bit.bit_length() - 1
            grid[r][c] = v
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            if search():
                return True
            rows[r] &= ~bit
            cols[c] &= ~bit
            boxes[b] &= ~bit
            grid[r][c] = 0
        return False

    return search()


def parse_puzzle(text: str):
    """Parse puzzle text into a 9x9 grid of ints. Return None if malformed."""
    lines = []
    for line in text.splitlines():
        stripped = "".join(line.split())
        if stripped:
            lines.append(stripped)

    if len(lines) != 9:
        return None

    grid = []
    for line in lines:
        if len(line) != 9:
            return None
        row = []
        for ch in line:
            if ch in "123456789":
                row.append(int(ch))
            elif ch in "0.":
                row.append(0)
            else:
                return None
        grid.append(row)

    if has_conflicts(grid):
        return None
    return grid


def has_conflicts(grid) -> bool:
    """Return True if any given clues duplicate in a row, column, or box."""
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                bit = 1 << v
                b = (r // 3) * 3 + c // 3
                if (rows[r] | cols[c] | boxes[b]) & bit:
                    return True
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit
    return False


def main(argv) -> int:
    if len(argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        return 2

    try:
        with open(argv[1], "r", encoding="utf-8") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError):
        print("Invalid puzzle")
        return 2

    grid = parse_puzzle(text)
    if grid is None:
        print("Invalid puzzle")
        return 2

    if not solve(grid):
        print("No solution")
        return 1

    for row in grid:
        print("".join(str(v) for v in row))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
