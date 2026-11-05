"""Sudoku solver using backtracking with the MRV heuristic.

Usage: python sudoku.py puzzle.txt
"""

import sys


def parse_puzzle(text):
    """Parse puzzle text into a 9x9 grid of ints (0 = empty).

    Raises ValueError on malformed input.
    """
    lines = []
    for raw in text.splitlines():
        line = "".join(raw.split())  # strip all whitespace
        if not line:
            continue
        lines.append(line)

    if len(lines) != 9:
        raise ValueError("wrong number of rows")

    grid = []
    for line in lines:
        if len(line) != 9:
            raise ValueError("wrong row length")
        row = []
        for ch in line:
            if ch == "." or ch == "0":
                row.append(0)
            elif ch in "123456789":
                row.append(int(ch))
            else:
                raise ValueError("invalid character: %r" % ch)
        grid.append(row)
    return grid


def is_consistent(grid):
    """Check that no row, column, or box contains a duplicate clue."""
    for unit in all_units():
        seen = set()
        for r, c in unit:
            v = grid[r][c]
            if v != 0:
                if v in seen:
                    return False
                seen.add(v)
    return True


def all_units():
    """Yield all 27 units (rows, columns, boxes) as lists of (r, c)."""
    for i in range(9):
        yield [(i, c) for c in range(9)]
        yield [(r, i) for r in range(9)]
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            yield [(br + dr, bc + dc) for dr in range(3) for dc in range(3)]


def candidates(grid, r, c):
    """Return the set of legal digits for the empty cell (r, c)."""
    used = set()
    for i in range(9):
        used.add(grid[r][i])
        used.add(grid[i][c])
    br, bc = 3 * (r // 3), 3 * (c // 3)
    for dr in range(3):
        for dc in range(3):
            used.add(grid[br + dr][bc + dc])
    return {d for d in range(1, 10)} - used


def find_mrv_cell(grid):
    """Find the empty cell with the fewest candidates.

    Returns (r, c, candidates) or None if the grid is full.
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


def solve(grid):
    """Solve the grid in place via backtracking + MRV. Returns True on success."""
    cell = find_mrv_cell(grid)
    if cell is None:
        return True  # no empty cells: solved
    r, c, cands = cell
    for digit in cands:
        grid[r][c] = digit
        if solve(grid):
            return True
        grid[r][c] = 0
    return False


def format_grid(grid):
    return "\n".join("".join(str(v) for v in row) for row in grid)


def main(argv):
    if len(argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        return 2

    try:
        with open(argv[1], "r", encoding="utf-8") as f:
            text = f.read()
        grid = parse_puzzle(text)
    except (OSError, ValueError):
        print("Invalid puzzle")
        return 2

    if not is_consistent(grid):
        print("Invalid puzzle")
        return 2

    if solve(grid):
        print(format_grid(grid))
        return 0
    else:
        print("No solution")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
