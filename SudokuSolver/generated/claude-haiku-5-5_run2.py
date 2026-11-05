#!/usr/bin/env python3
"""Sudoku solver using backtracking with the MRV (minimum remaining values) heuristic.

Usage: python sudoku.py puzzle.txt

Input: 9 lines of 9 characters. Digits 1-9 are clues; 0 or '.' marks an empty cell.
Blank lines and whitespace are ignored.
"""

import sys

ALL_DIGITS = 0b1111111110  # bits 1..9 set


def _popcount(x):
    return bin(x).count("1")


def _has_conflict(grid):
    """Return True if any row, column, or box contains a duplicate digit."""
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v == 0:
                continue
            bit = 1 << v
            b = (r // 3) * 3 + c // 3
            if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                return True
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
    return False


def solve(grid: list[list[int]]) -> bool:
    """Solve the 9x9 grid in place (0 = empty). Return True on success."""
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        return False
    for row in grid:
        for v in row:
            if not isinstance(v, int) or v < 0 or v > 9:
                return False
    if _has_conflict(grid):
        return False

    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    empties = []
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v == 0:
                empties.append((r, c))
            else:
                bit = 1 << v
                rows[r] |= bit
                cols[c] |= bit
                boxes[(r // 3) * 3 + c // 3] |= bit

    def search() -> bool:
        # MRV: choose the empty cell with the fewest legal candidates.
        best = None
        best_mask = 0
        best_count = 10
        for r, c in empties:
            if grid[r][c] != 0:
                continue
            b = (r // 3) * 3 + c // 3
            mask = ALL_DIGITS & ~(rows[r] | cols[c] | boxes[b])
            count = _popcount(mask)
            if count == 0:
                return False  # dead end
            if count < best_count:
                best_count = count
                best = (r, c, b)
                best_mask = mask
                if count == 1:
                    break

        if best is None:
            return True  # no empty cells left

        r, c, b = best
        for d in range(1, 10):
            if not (best_mask >> d) & 1:
                continue
            bit = 1 << d
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
        return False

    return search()


def parse_puzzle(path):
    """Parse the puzzle file. Return a 9x9 list of ints, or None if malformed."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_lines = f.readlines()
    except OSError:
        return None

    lines = []
    for line in raw_lines:
        cleaned = "".join(line.split())
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
            elif "0" <= ch <= "9":
                row.append(int(ch))
            else:
                return None
        grid.append(row)
    return grid


def main(argv):
    if len(argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        return 2

    grid = parse_puzzle(argv[1])
    if grid is None or _has_conflict(grid):
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
