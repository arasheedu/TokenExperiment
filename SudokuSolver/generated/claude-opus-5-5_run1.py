#!/usr/bin/env python3
"""Sudoku solver using backtracking search with the MRV heuristic.

Usage: python sudoku.py puzzle.txt
"""
from __future__ import annotations

import sys

ALL_DIGITS = 0x3FE  # bits 1..9 set


def _box(r: int, c: int) -> int:
    return (r // 3) * 3 + c // 3


def _popcount(x: int) -> int:
    return bin(x).count("1")


def _init_masks(grid: list[list[int]]):
    """Build row/col/box bitmasks. Returns None if clues conflict or grid is bad."""
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        return None
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if not isinstance(v, int) or v < 0 or v > 9:
                return None
            if v == 0:
                continue
            bit = 1 << v
            b = _box(r, c)
            if (rows[r] & bit) or (cols[c] & bit) or (boxes[b] & bit):
                return None
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
    return rows, cols, boxes


def is_consistent(grid: list[list[int]]) -> bool:
    """Return True if the grid is 9x9 with values 0-9 and no conflicting clues."""
    return _init_masks(grid) is not None


def _search(grid, rows, cols, boxes, empties) -> bool:
    if not empties:
        return True

    # MRV: choose the empty cell with the fewest legal candidates.
    best_idx = -1
    best_mask = 0
    best_count = 10
    for i, (r, c) in enumerate(empties):
        mask = ALL_DIGITS & ~(rows[r] | cols[c] | boxes[_box(r, c)])
        cnt = _popcount(mask)
        if cnt < best_count:
            best_count = cnt
            best_idx = i
            best_mask = mask
            if cnt <= 1:
                break

    if best_count == 0:
        return False

    r, c = empties[best_idx]
    b = _box(r, c)
    # Remove chosen cell from the empties list (swap with last for O(1)).
    empties[best_idx] = empties[-1]
    empties.pop()

    mask = best_mask
    while mask:
        bit = mask & -mask
        mask ^= bit
        digit = bit.bit_length() - 1
        grid[r][c] = digit
        rows[r] |= bit
        cols[c] |= bit
        boxes[b] |= bit
        if _search(grid, rows, cols, boxes, empties):
            return True
        rows[r] &= ~bit
        cols[c] &= ~bit
        boxes[b] &= ~bit
        grid[r][c] = 0

    # Restore empties list to its previous state.
    empties.append((r, c))
    last = len(empties) - 1
    empties[best_idx], empties[last] = empties[last], empties[best_idx]
    return False


def solve(grid: list[list[int]]) -> bool:
    """Solve the grid in place. Returns True on success, False if unsolvable/invalid."""
    masks = _init_masks(grid)
    if masks is None:
        return False
    rows, cols, boxes = masks
    empties = [(r, c) for r in range(9) for c in range(9) if grid[r][c] == 0]
    return _search(grid, rows, cols, boxes, empties)


def parse_puzzle(text: str):
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
            if ch in "0.":
                row.append(0)
            elif ch in "123456789":
                row.append(int(ch))
            else:
                return None
        grid.append(row)
    return grid


def main(argv: list[str]) -> int:
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
    if grid is None or not is_consistent(grid):
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
