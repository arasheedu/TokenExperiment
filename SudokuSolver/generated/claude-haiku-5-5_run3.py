#!/usr/bin/env python3
"""Sudoku solver using backtracking with the MRV (fewest candidates) heuristic.

Usage: python sudoku.py puzzle.txt

Input: 9 lines of 9 characters. Digits 1-9 are clues; 0 or '.' is an empty cell.
Whitespace and blank lines are ignored.

Exit status:
    0 - solved
    1 - no solution
    2 - malformed input (bad dimensions, invalid characters, or conflicting clues)
"""

import sys

SIZE = 9
BOX = 3


def _has_conflict(grid):
    """Return True if any filled digit repeats in a row, column, or box."""
    for r in range(SIZE):
        seen = set()
        for c in range(SIZE):
            v = grid[r][c]
            if v:
                if v in seen:
                    return True
                seen.add(v)
    for c in range(SIZE):
        seen = set()
        for r in range(SIZE):
            v = grid[r][c]
            if v:
                if v in seen:
                    return True
                seen.add(v)
    for br in range(0, SIZE, BOX):
        for bc in range(0, SIZE, BOX):
            seen = set()
            for r in range(br, br + BOX):
                for c in range(bc, bc + BOX):
                    v = grid[r][c]
                    if v:
                        if v in seen:
                            return True
                        seen.add(v)
    return False


def _is_well_formed(grid):
    """Check that grid is a 9x9 list of ints in 0..9."""
    if not isinstance(grid, list) or len(grid) != SIZE:
        return False
    for row in grid:
        if not isinstance(row, list) or len(row) != SIZE:
            return False
        for v in row:
            if not isinstance(v, int) or isinstance(v, bool) or not (0 <= v <= 9):
                return False
    return True


def _candidates(grid, r, c):
    """Return the sorted list of legal digits for empty cell (r, c)."""
    used = set(grid[r])
    used.update(grid[i][c] for i in range(SIZE))
    br, bc = (r // BOX) * BOX, (c // BOX) * BOX
    for i in range(br, br + BOX):
        for j in range(bc, bc + BOX):
            used.add(grid[i][j])
    return [d for d in range(1, SIZE + 1) if d not in used]


def _search(grid):
    """Recursive backtracking. Restores all cells it sets on failure."""
    best_cell = None
    best_cands = None
    for r in range(SIZE):
        for c in range(SIZE):
            if grid[r][c] == 0:
                cands = _candidates(grid, r, c)
                if not cands:
                    return False
                if best_cands is None or len(cands) < len(best_cands):
                    best_cell = (r, c)
                    best_cands = cands
                    if len(cands) == 1:
                        break
        else:
            continue
        if best_cands is not None and len(best_cands) == 1:
            break

    if best_cell is None:
        return True  # no empty cells: solved

    r, c = best_cell
    for d in best_cands:
        grid[r][c] = d
        if _search(grid):
            return True
        grid[r][c] = 0
    return False


def solve(grid: list[list[int]]) -> bool:
    """Solve the grid in place. Returns True on success.

    On failure (no solution or invalid grid), the grid is left unchanged.
    """
    if not _is_well_formed(grid):
        return False
    if _has_conflict(grid):
        return False
    return _search(grid)


def _parse(text):
    """Parse puzzle text into a 9x9 grid of ints. Raises ValueError if malformed."""
    rows = []
    for line in text.splitlines():
        stripped = "".join(line.split())
        if stripped:
            rows.append(stripped)

    if len(rows) != SIZE:
        raise ValueError("wrong number of rows")

    grid = []
    for row in rows:
        if len(row) != SIZE:
            raise ValueError("wrong row length")
        values = []
        for ch in row:
            if ch == ".":
                values.append(0)
            elif ch in "0123456789":
                values.append(int(ch))
            else:
                raise ValueError("invalid character")
        grid.append(values)
    return grid


def main(argv):
    if len(argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        return 2

    try:
        with open(argv[1], "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as exc:
        print(f"Cannot read file: {exc}", file=sys.stderr)
        return 2

    try:
        grid = _parse(text)
    except ValueError:
        print("Invalid puzzle")
        return 2

    if _has_conflict(grid):
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
