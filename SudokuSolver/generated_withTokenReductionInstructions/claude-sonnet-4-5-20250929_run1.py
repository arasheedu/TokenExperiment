#!/usr/bin/env python3
import sys

def is_valid(grid, row, col, num):
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if grid[i][j] == num:
                return False
    return True

def get_candidates(grid, row, col):
    return [num for num in range(1, 10) if is_valid(grid, row, col, num)]

def solve(grid):
    min_candidates = None
    min_count = 10
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                candidates = get_candidates(grid, i, j)
                if len(candidates) == 0:
                    return False
                if len(candidates) < min_count:
                    min_count = len(candidates)
                    min_candidates = (i, j, candidates)
    if min_candidates is None:
        return True
    row, col, candidates = min_candidates
    for num in candidates:
        grid[row][col] = num
        if solve(grid):
            return True
        grid[row][col] = 0
    return False

def parse_puzzle(lines):
    grid = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(line) != 9:
            return None
        row = []
        for ch in line:
            if ch in '0.':
                row.append(0)
            elif ch in '123456789':
                row.append(int(ch))
            else:
                return None
        grid.append(row)
    if len(grid) != 9:
        return None
    return grid

def validate_puzzle(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                num = grid[i][j]
                grid[i][j] = 0
                if not is_valid(grid, i, j, num):
                    grid[i][j] = num
                    return False
                grid[i][j] = num
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Invalid puzzle")
        sys.exit(2)
    try:
        with open(sys.argv[1]) as f:
            lines = f.readlines()
    except:
        print("Invalid puzzle")
        sys.exit(2)
    grid = parse_puzzle(lines)
    if grid is None or not validate_puzzle(grid):
        print("Invalid puzzle")
        sys.exit(2)
    if solve(grid):
        for row in grid:
            print(''.join(map(str, row)))
    else:
        print("No solution")
        sys.exit(1)
