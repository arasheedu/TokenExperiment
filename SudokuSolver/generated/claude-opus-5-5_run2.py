#!/usr/bin/env python3
"""Sudoku solver using backtracking search with the MRV heuristic.

Usage: python sudoku.py puzzle.txt
"""

import sys

ALL_DIGITS = 0x3FE  # bits 1..9 set


def _box_index(r, c):
    return (r // 3) * 3 + c // 3


def has_conflicts(grid):
    """Return True if any given clues conflict with each other."""
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v == 0:
                continue
            bit = 1 << v
            b = _box_index(r, c)
            if (rows[r] | cols[c] | boxes[b]) & bit:
                return True
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
    return False


def solve(grid):
    """Solve the 9x9 grid in place. Empty cells are 0.

    Returns True if a solution was found (grid is filled in), otherwise
    False (grid is left unchanged).
    """
    if not isinstance(grid, list) or len(grid) != 9:
        return False
    for row in grid:
        if not isinstance(row, list) or len(row) != 9:
            return False

    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    empties = []

    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if not isinstance(v, int) or v < 0 or v > 9:
                return False
            if v == 0:
                empties.append((r, c))
                continue
            bit = 1 << v
            b = _box_index(r, c)
            if (rows[r] | cols[c] | boxes[b]) & bit:
                return False
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit

    def search():
        if not empties:
            return True

        # MRV: choose the empty cell with the fewest legal candidates.
        best_i = -1
        best_mask = 0
        best_count = 10
        for i, (r, c) in enumerate(empties):
            mask = ALL_DIGITS & ~(rows[r] | cols[c] | boxes[_box_index(r, c)])
            n = bin(mask).count("1")
            if n < best_count:
                best_i, best_mask, best_count = i, mask, n
                if n == 0:
                    return False
                if n == 1:
                    break

        r, c = empties[best_i]
        empties[best_i] = empties[-1]
        empties.pop()
        b = _box_index(r, c)

        for d in range(1, 10):
            bit = 1 << d
            if not (best_mask & bit):
                continue
            grid[r][c] = d
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            if search():
                return True
            rows[r] &= ~bit
            cols[c] &= ~bit
            boxes[b] &= ~bit

        grid[r][c] = 0
        empties.append((r, c))
        last = len(empties) - 1
        empties[best_i], empties[last] = empties[last], empties[best_i]
        return False

    return search()


def parse_puzzle(text):
    """Parse puzzle text into a grid. Returns None if malformed."""
    lines = []
    for raw in text.splitlines():
        line = "".join(raw.split())
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
            if ch == "." or ch == "0":
                row.append(0)
            elif ch in "123456789":
                row.append(int(ch))
            else:
                return None
        grid.append(row)
    return grid


def main(argv):
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
    if grid is None or has_conflicts(grid):
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
