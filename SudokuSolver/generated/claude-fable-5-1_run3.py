#!/usr/bin/env python3
"""
sudoku.py - A Sudoku solver using backtracking search with the
Minimum Remaining Values (MRV) heuristic.

Usage:
    python sudoku.py puzzle.txt

Input format:
    9 lines of 9 characters each. Digits 1-9 are given clues;
    '0' or '.' marks an empty cell. Blank lines and whitespace are ignored.

Exit status:
    0 - solved, solution printed
    1 - no solution exists ("No solution" printed)
    2 - malformed input ("Invalid puzzle" printed)
"""

import sys

SIZE = 9
BOX = 3
DIGITS = range(1, SIZE + 1)
VALID_CHARS = set("0123456789.")


def candidates(grid, r, c):
    """Return a list of legal digits for the empty cell (r, c)."""
    used = set(grid[r])
    used.update(grid[i][c] for i in range(SIZE))
    br, bc = (r // BOX) * BOX, (c // BOX) * BOX
    for i in range(br, br + BOX):
        for j in range(bc, bc + BOX):
            used.add(grid[i][j])
    return [d for d in DIGITS if d not in used]


def find_mrv_cell(grid):
    """
    Find the empty cell with the fewest legal candidates.

    Returns ((row, col), candidates) or (None, None) if there are no
    empty cells left.
    """
    best_cell = None
    best_cands = None
    for r in range(SIZE):
        for c in range(SIZE):
            if grid[r][c] == 0:
                cands = candidates(grid, r, c)
                if best_cell is None or len(cands) < len(best_cands):
                    best_cell, best_cands = (r, c), cands
                    if len(cands) <= 1:
                        # Can't do better than 0 or 1 candidate.
                        return best_cell, best_cands
    return best_cell, best_cands


def is_valid(grid):
    """Check that the grid has the right shape and no conflicting clues."""
    if len(grid) != SIZE or any(len(row) != SIZE for row in grid):
        return False
    for row in grid:
        for v in row:
            if not isinstance(v, int) or v < 0 or v > SIZE:
                return False

    # Rows
    for r in range(SIZE):
        seen = set()
        for c in range(SIZE):
            v = grid[r][c]
            if v:
                if v in seen:
                    return False
                seen.add(v)

    # Columns
    for c in range(SIZE):
        seen = set()
        for r in range(SIZE):
            v = grid[r][c]
            if v:
                if v in seen:
                    return False
                seen.add(v)

    # Boxes
    for br in range(0, SIZE, BOX):
        for bc in range(0, SIZE, BOX):
            seen = set()
            for r in range(br, br + BOX):
                for c in range(bc, bc + BOX):
                    v = grid[r][c]
                    if v:
                        if v in seen:
                            return False
                        seen.add(v)

    return True


def solve(grid: list[list[int]]) -> bool:
    """
    Solve the Sudoku grid in place using backtracking with the MRV heuristic.

    `grid` is a 9x9 list of lists of ints, where 0 marks an empty cell.
    Returns True if a solution was found (grid now holds it), False otherwise.
    If the grid is left unsolved, it is restored to its original state.
    """
    if not is_valid(grid):
        return False
    return _backtrack(grid)


def _backtrack(grid):
    cell, cands = find_mrv_cell(grid)
    if cell is None:
        return True  # No empty cells remain: solved.
    r, c = cell
    for d in cands:
        grid[r][c] = d
        if _backtrack(grid):
            return True
    grid[r][c] = 0
    return False


def parse_puzzle(text):
    """
    Parse puzzle text into a 9x9 grid of ints.

    Returns the grid, or None if the input is malformed.
    """
    lines = []
    for raw in text.splitlines():
        line = "".join(raw.split())  # remove all whitespace
        if line:
            lines.append(line)

    if len(lines) != SIZE:
        return None

    grid = []
    for line in lines:
        if len(line) != SIZE:
            return None
        row = []
        for ch in line:
            if ch not in VALID_CHARS:
                return None
            row.append(0 if ch in "0." else int(ch))
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
