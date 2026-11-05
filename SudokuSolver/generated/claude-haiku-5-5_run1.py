#!/usr/bin/env python3
"""Sudoku solver: backtracking search with the MRV (fewest candidates) heuristic.

Usage:
    python sudoku.py puzzle.txt

Input: 9 lines of 9 characters. Digits 1-9 are clues; 0 or '.' is an empty cell.
Whitespace and blank lines are ignored.

Exit status:
    0 - solved (grid printed)
    1 - no solution exists
    2 - malformed input or usage error
"""
import sys

ALL_DIGITS = 0b1111111110  # bits 1..9 set


def _box_index(r, c):
    return (r // 3) * 3 + (c // 3)


def _init_masks(grid):
    """Build row/column/box bitmasks from the givens.

    Returns (rows, cols, boxes), or None if the givens already conflict.
    """
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                bit = 1 << v
                b = _box_index(r, c)
                if (rows[r] & bit) or (cols[c] & bit) or (boxes[b] & bit):
                    return None
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit
    return rows, cols, boxes


def _search(grid, rows, cols, boxes):
    # MRV: find the empty cell with the fewest legal candidates.
    best = None
    best_cands = 0
    best_count = 10
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                used = rows[r] | cols[c] | boxes[_box_index(r, c)]
                cands = ALL_DIGITS & ~used
                count = bin(cands).count("1")
                if count < best_count:
                    best = (r, c)
                    best_cands = cands
                    best_count = count
                    if count == 0:
                        return False  # dead end
    if best is None:
        return True  # no empty cells: solved

    r, c = best
    b = _box_index(r, c)
    for v in range(1, 10):
        bit = 1 << v
        if best_cands & bit:
            grid[r][c] = v
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            if _search(grid, rows, cols, boxes):
                return True
            rows[r] ^= bit
            cols[c] ^= bit
            boxes[b] ^= bit
            grid[r][c] = 0
    return False


def solve(grid: list[list[int]]) -> bool:
    """Solve a 9x9 grid in place (0 = empty). Returns True on success.

    Returns False if the grid is malformed, its givens conflict, or it
    has no solution. On False the grid is left with its original clues.
    """
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        return False
    for row in grid:
        for v in row:
            if not isinstance(v, int) or isinstance(v, bool) or not 0 <= v <= 9:
                return False
    masks = _init_masks(grid)
    if masks is None:
        return False
    rows, cols, boxes = masks
    return _search(grid, rows, cols, boxes)


def _parse(path):
    """Parse the puzzle file. Returns a 9x9 int grid or None if malformed."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_lines = f.readlines()
    except OSError as exc:
        print(f"Error: cannot read '{path}': {exc}", file=sys.stderr)
        return None

    lines = []
    for raw in raw_lines:
        cleaned = "".join(raw.split())
        if cleaned:
            lines.append(cleaned)

    if len(lines) != 9:
        return None

    grid = []
    for line in lines:
        if len(line) != 9:
            return None
        row = []
        for ch in line:
            if ch == ".":
                row.append(0)
            elif ch in "0123456789":
                row.append(int(ch))
            else:
                return None
        grid.append(row)
    return grid


def main(argv):
    if len(argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        return 2

    grid = _parse(argv[1])
    if grid is None or _init_masks(grid) is None:
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
