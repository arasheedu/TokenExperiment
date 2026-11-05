#!/usr/bin/env python3
"""Sudoku solver using backtracking search with the MRV heuristic.

Usage: python sudoku.py puzzle.txt
"""

import sys

ALL_DIGITS = 0x3FE  # bits 1..9 set


def _box_index(r: int, c: int) -> int:
    return (r // 3) * 3 + (c // 3)


def _init_masks(grid):
    """Build row/column/box bitmasks. Returns None if the clues conflict."""
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v == 0:
                continue
            bit = 1 << v
            b = _box_index(r, c)
            if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                return None
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
    return rows, cols, boxes


def is_valid_grid(grid) -> bool:
    """Check shape, value range, and that the given clues do not conflict."""
    if not isinstance(grid, list) or len(grid) != 9:
        return False
    for row in grid:
        if not isinstance(row, list) or len(row) != 9:
            return False
        for v in row:
            if not isinstance(v, int) or isinstance(v, bool) or not 0 <= v <= 9:
                return False
    return _init_masks(grid) is not None


def solve(grid: list[list[int]]) -> bool:
    """Solve the Sudoku grid in place. Returns True on success, False otherwise.

    Empty cells are represented by 0. On failure the grid is left unchanged.
    """
    if not is_valid_grid(grid):
        return False
    rows, cols, boxes = _init_masks(grid)

    empties = [(r, c, _box_index(r, c))
               for r in range(9) for c in range(9) if grid[r][c] == 0]

    def search(remaining: int) -> bool:
        if remaining == 0:
            return True

        # MRV: choose the empty cell with the fewest legal candidates.
        best_i = -1
        best_mask = 0
        best_count = 10
        for i in range(remaining):
            r, c, b = empties[i]
            mask = ALL_DIGITS & ~(rows[r] | cols[c] | boxes[b])
            count = bin(mask).count("1")
            if count < best_count:
                best_count = count
                best_mask = mask
                best_i = i
                if count <= 1:
                    break
        if best_count == 0:
            return False

        # Move chosen cell to the end of the active region.
        last = remaining - 1
        empties[best_i], empties[last] = empties[last], empties[best_i]
        r, c, b = empties[last]

        mask = best_mask
        while mask:
            bit = mask & -mask
            mask ^= bit
            grid[r][c] = bit.bit_length() - 1
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            if search(last):
                return True
            rows[r] &= ~bit
            cols[c] &= ~bit
            boxes[b] &= ~bit
        grid[r][c] = 0

        empties[best_i], empties[last] = empties[last], empties[best_i]
        return False

    return search(len(empties))


def parse_puzzle(text: str):
    """Parse puzzle text into a 9x9 grid. Returns None if malformed."""
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


def format_grid(grid) -> str:
    return "\n".join("".join(str(v) for v in row) for row in grid)


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        return 2

    try:
        with open(argv[0], "r", encoding="utf-8") as f:
            text = f.read()
    except UnicodeDecodeError:
        print("Invalid puzzle")
        return 2
    except OSError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return 2

    grid = parse_puzzle(text)
    if grid is None or not is_valid_grid(grid):
        print("Invalid puzzle")
        return 2

    if not solve(grid):
        print("No solution")
        return 1

    print(format_grid(grid))
    return 0


if __name__ == "__main__":
    sys.exit(main())
