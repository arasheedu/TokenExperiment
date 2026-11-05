#!/usr/bin/env python3
import sys


def parse_grid(text):
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line != ""]
    if len(lines) != 9:
        return None
    grid = []
    for line in lines:
        if len(line) != 9:
            return None
        row = []
        for ch in line:
            if ch in ".0":
                row.append(0)
            elif ch in "123456789":
                row.append(int(ch))
            else:
                return None
        grid.append(row)
    return grid


def is_valid_grid(grid):
    for i in range(9):
        for j in range(9):
            v = grid[i][j]
            if v != 0:
                grid[i][j] = 0
                if not is_safe(grid, i, j, v):
                    grid[i][j] = v
                    return False
                grid[i][j] = v
    return True


def is_safe(grid, row, col, val):
    for k in range(9):
        if grid[row][k] == val:
            return False
        if grid[k][col] == val:
            return False
    br = (row // 3) * 3
    bc = (col // 3) * 3
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if grid[i][j] == val:
                return False
    return True


def candidates(grid, row, col):
    cands = []
    for v in range(1, 10):
        if is_safe(grid, row, col, v):
            cands.append(v)
    return cands


def find_mrv_cell(grid):
    best = None
    best_cands = None
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                cands = candidates(grid, i, j)
                if best is None or len(cands) < len(best_cands):
                    best = (i, j)
                    best_cands = cands
                    if len(cands) == 0:
                        return best, best_cands
    return best, best_cands


def solve(grid: list[list[int]]) -> bool:
    cell, cands = find_mrv_cell(grid)
    if cell is None:
        return True
    if not cands:
        return False
    row, col = cell
    for v in cands:
        grid[row][col] = v
        if solve(grid):
            return True
        grid[row][col] = 0
    return False


def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        sys.exit(2)
    try:
        with open(sys.argv[1], "r") as f:
            text = f.read()
    except OSError:
        print("Invalid puzzle")
        sys.exit(2)

    grid = parse_grid(text)
    if grid is None or not is_valid_grid(grid):
        print("Invalid puzzle")
        sys.exit(2)

    if not solve(grid):
        print("No solution")
        sys.exit(1)

    for row in grid:
        print("".join(str(v) for v in row))


if __name__ == "__main__":
    main()
