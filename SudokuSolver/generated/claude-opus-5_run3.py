#!/usr/bin/env python3
"""A Sudoku solver using backtracking search with the MRV heuristic.

Usage:
    python sudoku.py puzzle.txt

Input file format:
    9 lines of 9 characters each.  The digits '1'-'9' are given clues,
    '0' or '.' marks an empty cell.  Blank lines and surrounding
    whitespace are ignored.

Exit status:
    0 - solved (the solution is printed)
    1 - the puzzle has no solution ("No solution" is printed)
    2 - the input is malformed ("Invalid puzzle" is printed)
"""

import sys

ALL = 0b1111111110  # bits 1..9 set


def _popcount(x: int) -> int:
    return bin(x).count("1")


def solve(grid: "list[list[int]]") -> bool:
    """Solve `grid` in place.  Return True on success, False otherwise.

    `grid` must be a 9x9 list of lists holding integers 0-9, where 0 marks
    an empty cell.  If the given clues already conflict, False is returned
    and the grid is left untouched.
    """
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    empties = []

    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                bit = 1 << v
                b = (r // 3) * 3 + (c // 3)
                if (rows[r] | cols[c] | boxes[b]) & bit:
                    return False  # conflicting clues
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit
            else:
                empties.append((r, c))

    def backtrack() -> bool:
        # Minimum remaining values: pick the empty cell with fewest candidates.
        best_cell = None
        best_mask = 0
        best_count = 10

        for (r, c) in empties:
            if grid[r][c]:
                continue
            b = (r // 3) * 3 + (c // 3)
            mask = ALL & ~(rows[r] | cols[c] | boxes[b])
            count = _popcount(mask)
            if count < best_count:
                best_count = count
                best_cell = (r, c)
                best_mask = mask
                if count <= 1:
                    break

        if best_cell is None:
            return True  # no empty cells left: solved

        if best_count == 0:
            return False  # dead end

        r, c = best_cell
        b = (r // 3) * 3 + (c // 3)
        mask = best_mask
        while mask:
            bit = mask & -mask
            mask ^= bit
            v = bit.bit_length() - 1

            grid[r][c] = v
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit

            if backtrack():
                return True

            grid[r][c] = 0
            rows[r] &= ~bit
            cols[c] &= ~bit
            boxes[b] &= ~bit

        return False

    return backtrack()


def parse_grid(text: str) -> "list[list[int]]":
    """Parse the puzzle text into a 9x9 grid of ints.

    Raises ValueError if the text is malformed.
    """
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    if len(lines) != 9:
        raise ValueError("expected 9 non-empty lines, got %d" % len(lines))

    grid = []
    for line in lines:
        line = "".join(line.split())  # drop any internal whitespace
        if len(line) != 9:
            raise ValueError("expected 9 characters per line")
        row = []
        for ch in line:
            if ch in "0.":
                row.append(0)
            elif ch in "123456789":
                row.append(int(ch))
            else:
                raise ValueError("invalid character %r" % ch)
        grid.append(row)

    if not is_consistent(grid):
        raise ValueError("clues already conflict")

    return grid


def is_consistent(grid: "list[list[int]]") -> bool:
    """Return True if the given clues do not conflict."""
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if not v:
                continue
            bit = 1 << v
            b = (r // 3) * 3 + (c // 3)
            if (rows[r] | cols[c] | boxes[b]) & bit:
                return False
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
    return True


def format_grid(grid: "list[list[int]]") -> str:
    return "\n".join("".join(str(v) for v in row) for row in grid)


def main(argv: "list[str]") -> int:
    if len(argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        return 2

    try:
        with open(argv[1], "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print("Invalid puzzle", file=sys.stderr if False else sys.stdout)
        print("could not read %s: %s" % (argv[1], exc), file=sys.stderr)
        return 2

    try:
        grid = parse_grid(text)
    except ValueError as exc:
        print("Invalid puzzle")
        print("error: %s" % exc, file=sys.stderr)
        return 2

    if not solve(grid):
        print("No solution")
        return 1

    print(format_grid(grid))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
