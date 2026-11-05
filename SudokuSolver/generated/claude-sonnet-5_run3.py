#!/usr/bin/env python3
"""
sudoku.py - A simple Sudoku solver using backtracking with the
Minimum Remaining Values (MRV) heuristic.

Usage:
    python sudoku.py puzzle.txt

Input format:
    9 lines of 9 characters each. Digits 1-9 are clues; '0' or '.'
    marks an empty cell. Blank lines and surrounding/internal
    whitespace are ignored.
"""

import sys


def get_candidates(grid: list, r: int, c: int) -> set:
    """Return the set of legal digits for the empty cell (r, c)."""
    used = set()
    used.update(grid[r])
    used.update(grid[i][c] for i in range(9))

    br, bc = 3 * (r // 3), 3 * (c // 3)
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            used.add(grid[i][j])

    used.discard(0)
    return set(range(1, 10)) - used


def solve(grid: list) -> bool:
    """
    Solve the Sudoku grid in place using backtracking with MRV.
    grid is a list of 9 lists of 9 ints (0 = empty).
    Returns True if solved successfully, False otherwise.
    """
    best_cell = None
    best_candidates = None

    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cands = get_candidates(grid, r, c)
                if not cands:
                    return False  # dead end, no legal digit
                if best_candidates is None or len(cands) < len(best_candidates):
                    best_cell = (r, c)
                    best_candidates = cands
                    if len(cands) == 1:
                        # Can't do better than 1 candidate; stop searching early.
                        break
        else:
            continue
        break

    if best_cell is None:
        return True  # no empty cells left -> solved

    r, c = best_cell
    for val in sorted(best_candidates):
        grid[r][c] = val
        if solve(grid):
            return True
        grid[r][c] = 0

    return False


def valid_initial(grid: list) -> bool:
    """Check that the initial grid has no conflicting clues."""
    # Rows
    for r in range(9):
        vals = [v for v in grid[r] if v != 0]
        if len(vals) != len(set(vals)):
            return False

    # Columns
    for c in range(9):
        vals = [grid[r][c] for r in range(9) if grid[r][c] != 0]
        if len(vals) != len(set(vals)):
            return False

    # Boxes
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            vals = [
                grid[r][c]
                for r in range(br, br + 3)
                for c in range(bc, bc + 3)
                if grid[r][c] != 0
            ]
            if len(vals) != len(set(vals)):
                return False

    return True


def parse_input(lines: list) -> list:
    """
    Parse raw lines into a 9x9 grid of ints.
    Returns None if the input is malformed.
    """
    rows = []
    for line in lines:
        stripped = "".join(line.split())  # remove all whitespace
        if stripped == "":
            continue  # ignore blank lines
        rows.append(stripped)

    if len(rows) != 9:
        return None

    grid = []
    for row in rows:
        if len(row) != 9:
            return None
        grid_row = []
        for ch in row:
            if ch == ".":
                grid_row.append(0)
            elif ch.isdigit():
                grid_row.append(int(ch))
            else:
                return None
        grid.append(grid_row)

    return grid


def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        sys.exit(2)

    path = sys.argv[1]

    try:
        with open(path, "r") as f:
            lines = f.readlines()
    except OSError:
        print("Invalid puzzle")
        sys.exit(2)

    grid = parse_input(lines)
    if grid is None:
        print("Invalid puzzle")
        sys.exit(2)

    if not valid_initial(grid):
        print("Invalid puzzle")
        sys.exit(2)

    if solve(grid):
        for row in grid:
            print("".join(str(v) for v in row))
    else:
        print("No solution")
        sys.exit(1)


if __name__ == "__main__":
    main()
