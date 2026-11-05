#!/usr/bin/env python3
"""Sudoku solver using backtracking search with the MRV heuristic.

Usage: python sudoku.py puzzle.txt
"""

import sys

VALID_CHARS = set("0123456789.")
ALL = 0x3FE  # bits 1..9 set


def solve(grid: list[list[int]]) -> bool:
    """Solve the grid in place. Return True on success, False if unsolvable
    (including when the given clues conflict). On failure the grid is left
    with its original contents."""
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9

    # Load existing clues and check for conflicts.
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v == 0:
                continue
            if not (1 <= v <= 9):
                return False
            bit = 1 << v
            b = (r // 3) * 3 + c // 3
            if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                return False
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit

    def search() -> bool:
        # MRV: choose the empty cell with the fewest candidates.
        best = None
        best_mask = 0
        best_count = 10
        for r in range(9):
            for c in range(9):
                if grid[r][c] != 0:
                    continue
                b = (r // 3) * 3 + c // 3
                mask = ALL & ~(rows[r] | cols[c] | boxes[b])
                count = bin(mask).count("1")
                if count < best_count:
                    best_count = count
                    best = (r, c, b)
                    best_mask = mask
                    if count == 0:
                        return False
                    if count == 1:
                        break
            if best_count == 1:
                break

        if best is None:
            return True  # no empty cells: solved

        r, c, b = best
        for v in range(1, 10):
            bit = 1 << v
            if not (best_mask & bit):
                continue
            grid[r][c] = v
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            if search():
                return True
            grid[r][c] = 0
            rows[r] &= ~bit
            cols[c] &= ~bit
            boxes[b] &= ~bit
        return False

    return search()


def parse_puzzle(text: str):
    """Parse puzzle text into a 9x9 grid of ints. Return None if malformed."""
    lines = []
    for line in text.splitlines():
        s = "".join(line.split())
        if s:
            lines.append(s)
    if len(lines) != 9:
        return None
    grid = []
    for s in lines:
        if len(s) != 9:
            return None
        if any(ch not in VALID_CHARS for ch in s):
            return None
        grid.append([0 if ch == "." else int(ch) for ch in s])
    return grid


def has_conflicts(grid) -> bool:
    """Return True if any given clues violate Sudoku rules."""
    def dup(values):
        vals = [v for v in values if v != 0]
        return len(vals) != len(set(vals))

    for i in range(9):
        if dup(grid[i]):
            return True
        if dup([grid[r][i] for r in range(9)]):
            return True
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            if dup([grid[br + dr][bc + dc] for dr in range(3) for dc in range(3)]):
                return True
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
    if grid is None or has_conflicts(grid):
        print("Invalid puzzle")
        return 2

    if solve(grid):
        for row in grid:
            print("".join(str(v) for v in row))
        return 0

    print("No solution")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
