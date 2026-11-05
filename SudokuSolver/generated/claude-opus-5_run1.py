#!/usr/bin/env python3
"""A Sudoku solver using backtracking search with the MRV heuristic.

Usage:
    python sudoku.py puzzle.txt

Input file format: 9 lines of 9 characters each.  Digits 1-9 are givens,
'0' or '.' marks an empty cell.  Blank lines and surrounding whitespace
are ignored.
"""

import sys

__all__ = ["solve", "parse_grid", "format_grid", "main"]


def parse_grid(text: str) -> list[list[int]]:
    """Parse puzzle text into a 9x9 grid of ints.

    Raises ValueError if the text is malformed.
    """
    lines = []
    for raw in text.splitlines():
        line = "".join(raw.split())  # drop all whitespace inside the line
        if not line:
            continue
        lines.append(line)

    if len(lines) != 9:
        raise ValueError("expected 9 non-empty lines, got %d" % len(lines))

    grid = []
    for line in lines:
        if len(line) != 9:
            raise ValueError("expected 9 characters per line, got %d" % len(line))
        row = []
        for ch in line:
            if ch in "0.":
                row.append(0)
            elif ch in "123456789":
                row.append(int(ch))
            else:
                raise ValueError("invalid character %r" % ch)
        grid.append(row)
    return grid


def format_grid(grid: list[list[int]]) -> str:
    """Render a 9x9 grid as 9 lines of 9 digits."""
    return "\n".join("".join(str(v) for v in row) for row in grid)


def _check_shape(grid) -> None:
    if not isinstance(grid, list) or len(grid) != 9:
        raise ValueError("grid must have 9 rows")
    for row in grid:
        if not isinstance(row, list) or len(row) != 9:
            raise ValueError("each row must have 9 cells")
        for v in row:
            if not isinstance(v, int) or isinstance(v, bool) or not 0 <= v <= 9:
                raise ValueError("cell values must be ints in 0..9")


def solve(grid: list[list[int]]) -> bool:
    """Solve the Sudoku in `grid` in place.

    Returns True if a solution was found (grid is filled in), False if the
    puzzle is unsolvable (including when the given clues already conflict).
    Raises ValueError if the grid is not a 9x9 list of ints in 0..9.
    """
    _check_shape(grid)

    ALL = 0x1FF
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    empties = []

    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                bit = 1 << (v - 1)
                b = (r // 3) * 3 + (c // 3)
                if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                    return False  # conflicting clues
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit
            else:
                empties.append((r, c))

    def search(cells):
        if not cells:
            return True

        # Minimum remaining values: pick the cell with fewest candidates.
        best_i = -1
        best_mask = 0
        best_count = 10
        for i, (r, c) in enumerate(cells):
            b = (r // 3) * 3 + (c // 3)
            mask = ~(rows[r] | cols[c] | boxes[b]) & ALL
            count = bin(mask).count("1")
            if count == 0:
                return False  # dead end
            if count < best_count:
                best_count = count
                best_mask = mask
                best_i = i
                if count == 1:
                    break

        r, c = cells[best_i]
        b = (r // 3) * 3 + (c // 3)
        rest = cells[:best_i] + cells[best_i + 1:]

        m = best_mask
        while m:
            bit = m & -m
            m -= bit
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            grid[r][c] = bit.bit_length()
            if search(rest):
                return True
            rows[r] ^= bit
            cols[c] ^= bit
            boxes[b] ^= bit
            grid[r][c] = 0

        return False

    return search(empties)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        return 2

    try:
        with open(argv[1], "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as exc:
        print("Cannot read %s: %s" % (argv[1], exc), file=sys.stderr)
        return 2

    try:
        grid = parse_grid(text)
    except ValueError:
        print("Invalid puzzle")
        return 2

    # Detect clue conflicts up front so they report as malformed input.
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if not v:
                continue
            bit = 1 << (v - 1)
            b = (r // 3) * 3 + (c // 3)
            if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                print("Invalid puzzle")
                return 2
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit

    if not solve(grid):
        print("No solution")
        return 1

    print(format_grid(grid))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
