#!/usr/bin/env python3
"""Sudoku solver using backtracking search with the MRV heuristic.

Usage: python sudoku.py puzzle.txt

Exit codes:
    0 - solved
    1 - no solution
    2 - invalid puzzle / bad input
"""

import sys

DIGITS = range(1, 10)


def candidates(grid, r, c):
    """Return the list of legal digits for the empty cell (r, c)."""
    used = set()
    for i in range(9):
        used.add(grid[r][i])
        used.add(grid[i][c])
    br, bc = 3 * (r // 3), 3 * (c // 3)
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            used.add(grid[i][j])
    return [d for d in DIGITS if d not in used]


def find_mrv_cell(grid):
    """Return ((r, c), candidates) for the empty cell with fewest candidates.

    Returns (None, None) when there are no empty cells left.
    """
    best_cell = None
    best_cands = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cands = candidates(grid, r, c)
                if best_cell is None or len(cands) < len(best_cands):
                    best_cell, best_cands = (r, c), cands
                    if len(cands) <= 1:
                        return best_cell, best_cands
    return best_cell, best_cands


def is_valid(grid):
    """Check that the grid is 9x9, contains only 0-9, and has no conflicts."""
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        return False
    for row in grid:
        for v in row:
            if not isinstance(v, int) or v < 0 or v > 9:
                return False
    # rows
    for r in range(9):
        seen = set()
        for c in range(9):
            v = grid[r][c]
            if v:
                if v in seen:
                    return False
                seen.add(v)
    # columns
    for c in range(9):
        seen = set()
        for r in range(9):
            v = grid[r][c]
            if v:
                if v in seen:
                    return False
                seen.add(v)
    # boxes
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            seen = set()
            for r in range(br, br + 3):
                for c in range(bc, bc + 3):
                    v = grid[r][c]
                    if v:
                        if v in seen:
                            return False
                        seen.add(v)
    return True


def _backtrack(grid):
    cell, cands = find_mrv_cell(grid)
    if cell is None:
        return True
    r, c = cell
    for d in cands:
        grid[r][c] = d
        if _backtrack(grid):
            return True
    grid[r][c] = 0
    return False


def solve(grid: list[list[int]]) -> bool:
    """Solve the Sudoku grid in place. Return True on success, False otherwise.

    The grid is a 9x9 list of lists of ints, with 0 marking empty cells.
    """
    if not is_valid(grid):
        return False
    return _backtrack(grid)


def parse_puzzle(text):
    """Parse puzzle text into a 9x9 grid. Return None if malformed."""
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


def format_grid(grid):
    return "\n".join("".join(str(v) for v in row) for row in grid)


def main(argv):
    if len(argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        return 2
    try:
        with open(argv[1], "r", encoding="utf-8") as f:
            text = f.read()
    except OSError:
        print("Invalid puzzle")
        return 2

    grid = parse_puzzle(text)
    if grid is None or not is_valid(grid):
        print("Invalid puzzle")
        return 2

    if solve(grid):
        print(format_grid(grid))
        return 0

    print("No solution")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
