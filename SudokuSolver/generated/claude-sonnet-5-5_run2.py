#!/usr/bin/env python3
"""Sudoku solver using backtracking search with the MRV heuristic.

Usage: python sudoku.py puzzle.txt
"""

import sys

ALL_DIGITS = 0x3FE  # bits 1..9 set


def solve(grid: list[list[int]]) -> bool:
    """Solve the grid in place. Return True on success, False otherwise.

    On failure the grid is left unchanged.
    """
    if not isinstance(grid, list) or len(grid) != 9:
        return False

    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9

    for r in range(9):
        if not isinstance(grid[r], list) or len(grid[r]) != 9:
            return False
        for c in range(9):
            v = grid[r][c]
            if not isinstance(v, int) or isinstance(v, bool) or not 0 <= v <= 9:
                return False
            if v == 0:
                continue
            bit = 1 << v
            b = (r // 3) * 3 + c // 3
            if (rows[r] | cols[c] | boxes[b]) & bit:
                return False  # conflicting clues
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit

    def search() -> bool:
        best_r = best_c = -1
        best_cand = 0
        best_count = 10

        for r in range(9):
            for c in range(9):
                if grid[r][c] != 0:
                    continue
                b = (r // 3) * 3 + c // 3
                cand = ALL_DIGITS & ~(rows[r] | cols[c] | boxes[b])
                count = bin(cand).count("1")
                if count == 0:
                    return False
                if count < best_count:
                    best_count = count
                    best_r, best_c, best_cand = r, c, cand
                    if count == 1:
                        break
            if best_count == 1:
                break

        if best_r == -1:
            return True  # no empty cells left

        r, c = best_r, best_c
        b = (r // 3) * 3 + c // 3
        for v in range(1, 10):
            bit = 1 << v
            if not best_cand & bit:
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


def parse_puzzle(text: str) -> list[list[int]]:
    """Parse puzzle text into a 9x9 grid. Raise ValueError if malformed."""
    lines = []
    for line in text.splitlines():
        stripped = "".join(line.split())
        if stripped:
            lines.append(stripped)

    if len(lines) != 9:
        raise ValueError("wrong number of rows")

    grid = []
    for line in lines:
        if len(line) != 9:
            raise ValueError("wrong row length")
        row = []
        for ch in line:
            if ch in "123456789":
                row.append(int(ch))
            elif ch in "0.":
                row.append(0)
            else:
                raise ValueError("invalid character")
        grid.append(row)
    return grid


def has_conflicts(grid: list[list[int]]) -> bool:
    """Return True if the given clues already violate Sudoku rules."""
    seen_rows = [set() for _ in range(9)]
    seen_cols = [set() for _ in range(9)]
    seen_boxes = [set() for _ in range(9)]
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v == 0:
                continue
            b = (r // 3) * 3 + c // 3
            if v in seen_rows[r] or v in seen_cols[c] or v in seen_boxes[b]:
                return True
            seen_rows[r].add(v)
            seen_cols[c].add(v)
            seen_boxes[b].add(v)
    return False


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        return 2

    try:
        with open(argv[1], "r", encoding="utf-8") as f:
            text = f.read()
        grid = parse_puzzle(text)
    except (OSError, UnicodeDecodeError, ValueError):
        print("Invalid puzzle")
        return 2

    if has_conflicts(grid):
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
