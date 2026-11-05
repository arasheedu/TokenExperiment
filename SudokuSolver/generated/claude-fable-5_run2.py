#!/usr/bin/env python3
"""Sudoku solver using backtracking with the MRV heuristic.

Usage: python sudoku.py puzzle.txt
"""

import sys


def candidates(grid, row, col):
    """Return the set of legal digits for the empty cell (row, col)."""
    used = set()
    for i in range(9):
        used.add(grid[row][i])
        used.add(grid[i][col])
    br, bc = 3 * (row // 3), 3 * (col // 3)
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            used.add(grid[r][c])
    return {d for d in range(1, 10) if d not in used}


def find_mrv_cell(grid):
    """Find the empty cell with the fewest candidates.

    Returns (row, col, candidates) or None if the grid is full.
    """
    best = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cands = candidates(grid, r, c)
                if best is None or len(cands) < len(best[2]):
                    best = (r, c, cands)
                    if len(cands) <= 1:
                        return best
    return best


def solve(grid: list[list[int]]) -> bool:
    """Solve the Sudoku grid in place. Return True on success."""
    cell = find_mrv_cell(grid)
    if cell is None:
        return True  # grid is complete
    row, col, cands = cell
    for digit in cands:
        grid[row][col] = digit
        if solve(grid):
            return True
    grid[row][col] = 0
    return False


def is_consistent(grid):
    """Check that no given clues conflict with each other."""
    def no_dups(values):
        digits = [v for v in values if v != 0]
        return len(digits) == len(set(digits))

    for i in range(9):
        if not no_dups(grid[i]):
            return False
        if not no_dups([grid[r][i] for r in range(9)]):
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            block = [grid[r][c]
                     for r in range(br, br + 3)
                     for c in range(bc, bc + 3)]
            if not no_dups(block):
                return False
    return True


def parse_puzzle(text):
    """Parse puzzle text into a 9x9 grid of ints. Raise ValueError if malformed."""
    lines = []
    for raw in text.splitlines():
        line = "".join(raw.split())  # remove all whitespace
        if line:
            lines.append(line)
    if len(lines) != 9:
        raise ValueError("expected 9 lines")
    grid = []
    for line in lines:
        if len(line) != 9:
            raise ValueError("expected 9 characters per line")
        row = []
        for ch in line:
            if ch == "." or ch == "0":
                row.append(0)
            elif ch in "123456789":
                row.append(int(ch))
            else:
                raise ValueError(f"invalid character: {ch!r}")
        grid.append(row)
    if not is_consistent(grid):
        raise ValueError("clues conflict")
    return grid


def main(argv):
    if len(argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding="utf-8") as f:
            text = f.read()
        grid = parse_puzzle(text)
    except (OSError, ValueError):
        print("Invalid puzzle")
        return 2
    if solve(grid):
        print("\n".join("".join(str(d) for d in row) for row in grid))
        return 0
    print("No solution")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
