#!/usr/bin/env python3
"""Sudoku solver: backtracking search with the MRV (minimum remaining values) heuristic.

Usage:
    python sudoku.py puzzle.txt

Exit status:
    0 - solved, solution printed
    1 - puzzle has no solution ("No solution" printed)
    2 - malformed input ("Invalid puzzle" printed)
"""

import sys

DIGITS = frozenset(range(1, 10))


def _box_index(r: int, c: int) -> int:
    return (r // 3) * 3 + c // 3


def _is_well_formed(grid) -> bool:
    """Check shape (9x9), cell values (ints 0..9) and absence of conflicting clues."""
    if not isinstance(grid, list) or len(grid) != 9:
        return False
    for row in grid:
        if not isinstance(row, list) or len(row) != 9:
            return False
        for v in row:
            if not isinstance(v, int) or isinstance(v, bool) or not 0 <= v <= 9:
                return False

    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v == 0:
                continue
            b = _box_index(r, c)
            if v in rows[r] or v in cols[c] or v in boxes[b]:
                return False
            rows[r].add(v)
            cols[c].add(v)
            boxes[b].add(v)
    return True


def solve(grid: list[list[int]]) -> bool:
    """Solve the Sudoku grid in place.

    `grid` is a 9x9 list of lists of ints, where 0 marks an empty cell.
    Returns True if a solution was found (grid now holds it), False otherwise.
    If the grid is malformed or contains conflicting clues, returns False
    and leaves the grid unchanged.
    """
    if not _is_well_formed(grid):
        return False

    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                rows[r].add(v)
                cols[c].add(v)
                boxes[_box_index(r, c)].add(v)

    def backtrack() -> bool:
        # MRV: find the empty cell with the fewest legal candidates.
        best_cell = None
        best_cands = None
        for r in range(9):
            row = grid[r]
            for c in range(9):
                if row[c] != 0:
                    continue
                cands = DIGITS - rows[r] - cols[c] - boxes[_box_index(r, c)]
                n = len(cands)
                if n == 0:
                    return False  # dead end
                if best_cands is None or n < len(best_cands):
                    best_cell = (r, c)
                    best_cands = cands
                    if n == 1:
                        break
            if best_cands is not None and len(best_cands) == 1:
                break

        if best_cell is None:
            return True  # no empty cells left: solved

        r, c = best_cell
        b = _box_index(r, c)
        for v in sorted(best_cands):
            grid[r][c] = v
            rows[r].add(v)
            cols[c].add(v)
            boxes[b].add(v)
            if backtrack():
                return True
            grid[r][c] = 0
            rows[r].discard(v)
            cols[c].discard(v)
            boxes[b].discard(v)
        return False

    return backtrack()


def parse_puzzle(text: str):
    """Parse puzzle text into a 9x9 grid of ints. Returns None if malformed."""
    lines = []
    for line in text.splitlines():
        compact = "".join(line.split())  # drop all whitespace
        if compact:
            lines.append(compact)
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


def format_grid(grid) -> str:
    return "\n".join("".join(str(v) for v in row) for row in grid)


def main(argv) -> int:
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
    if grid is None or not _is_well_formed(grid):
        print("Invalid puzzle")
        return 2

    if solve(grid):
        print(format_grid(grid))
        return 0

    print("No solution")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
