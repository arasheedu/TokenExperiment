#!/usr/bin/env python3
"""
sudoku.py - A simple Sudoku solver using backtracking with the
Minimum Remaining Values (MRV) heuristic.

Usage:
    python sudoku.py puzzle.txt

Input format:
    9 lines of 9 characters each. Digits 1-9 are clues, '0' or '.'
    marks an empty cell. Blank lines and surrounding/inline whitespace
    are ignored.
"""

import sys
import re


def parse_grid(text: str) -> list:
    """Parse puzzle text into a 9x9 list of ints (0 for empty).

    Raises ValueError on malformed input.
    """
    raw_lines = text.splitlines()
    lines = []
    for line in raw_lines:
        # strip all whitespace characters from the line
        cleaned = re.sub(r"\s+", "", line)
        if cleaned == "":
            continue  # ignore blank lines
        lines.append(cleaned)

    if len(lines) != 9:
        raise ValueError("Expected 9 non-blank lines")

    grid = []
    for line in lines:
        if len(line) != 9:
            raise ValueError("Each line must have exactly 9 characters")
        row = []
        for ch in line:
            if ch == ".":
                row.append(0)
            elif ch.isdigit():
                row.append(int(ch))
            else:
                raise ValueError("Invalid character in puzzle: %r" % ch)
        grid.append(row)

    return grid


def has_conflicts(grid: list) -> bool:
    """Return True if the given clues already violate Sudoku rules."""
    # rows
    for r in range(9):
        seen = set()
        for c in range(9):
            v = grid[r][c]
            if v != 0:
                if v in seen:
                    return True
                seen.add(v)
    # columns
    for c in range(9):
        seen = set()
        for r in range(9):
            v = grid[r][c]
            if v != 0:
                if v in seen:
                    return True
                seen.add(v)
    # boxes
    for br in range(3):
        for bc in range(3):
            seen = set()
            for r in range(br * 3, br * 3 + 3):
                for c in range(bc * 3, bc * 3 + 3):
                    v = grid[r][c]
                    if v != 0:
                        if v in seen:
                            return True
                        seen.add(v)
    return False


def solve(grid: list) -> bool:
    """Solve the given 9x9 grid in place using backtracking with MRV.

    grid: list of 9 lists of 9 ints (0 denotes an empty cell).
    Returns True if a solution was found (grid is modified in place
    to contain the solution), False otherwise (grid may be left in
    a partially modified but ultimately reverted state).
    """
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empties = []

    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v != 0:
                b = (r // 3) * 3 + (c // 3)
                if v in rows[r] or v in cols[c] or v in boxes[b]:
                    return False  # initial conflict -> unsolvable
                rows[r].add(v)
                cols[c].add(v)
                boxes[b].add(v)
            else:
                empties.append((r, c))

    def candidates(r, c):
        b = (r // 3) * 3 + (c // 3)
        used = rows[r] | cols[c] | boxes[b]
        return [d for d in range(1, 10) if d not in used]

    def backtrack():
        if not empties:
            return True

        best_idx = None
        best_cell = None
        best_cands = None

        for idx, (r, c) in enumerate(empties):
            cands = candidates(r, c)
            if len(cands) == 0:
                return False  # dead end for this branch
            if best_cands is None or len(cands) < len(best_cands):
                best_idx, best_cell, best_cands = idx, (r, c), cands
                if len(cands) == 1:
                    break

        r, c = best_cell
        b = (r // 3) * 3 + (c // 3)

        empties.pop(best_idx)
        for d in best_cands:
            grid[r][c] = d
            rows[r].add(d)
            cols[c].add(d)
            boxes[b].add(d)

            if backtrack():
                return True

            grid[r][c] = 0
            rows[r].discard(d)
            cols[c].discard(d)
            boxes[b].discard(d)

        empties.insert(best_idx, (r, c))
        return False

    return backtrack()


def format_grid(grid: list) -> str:
    return "\n".join("".join(str(d) for d in row) for row in grid)


def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        sys.exit(2)

    path = sys.argv[1]

    try:
        with open(path, "r") as f:
            text = f.read()
        grid = parse_grid(text)
    except Exception:
        print("Invalid puzzle")
        sys.exit(2)

    if has_conflicts(grid):
        print("Invalid puzzle")
        sys.exit(2)

    if solve(grid):
        print(format_grid(grid))
    else:
        print("No solution")
        sys.exit(1)


if __name__ == "__main__":
    main()
