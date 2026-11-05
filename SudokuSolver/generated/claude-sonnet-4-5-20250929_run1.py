#!/usr/bin/env python3
import sys


def parse_grid(lines):
    """Parse input lines into a 9x9 grid. Returns None if malformed."""
    grid = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(line) != 9:
            return None
        row = []
        for char in line:
            if char in '123456789':
                row.append(int(char))
            elif char in '0.':
                row.append(0)
            else:
                return None
        grid.append(row)
    
    if len(grid) != 9:
        return None
    
    return grid


def is_valid_placement(grid, row, col, num):
    """Check if placing num at (row, col) is valid."""
    # Check row
    for c in range(9):
        if grid[row][c] == num:
            return False
    
    # Check column
    for r in range(9):
        if grid[r][col] == num:
            return False
    
    # Check 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if grid[r][c] == num:
                return False
    
    return True


def get_candidates(grid, row, col):
    """Get all valid candidates for a cell."""
    if grid[row][col] != 0:
        return []
    
    candidates = []
    for num in range(1, 10):
        if is_valid_placement(grid, row, col, num):
            candidates.append(num)
    
    return candidates


def find_mrv_cell(grid):
    """Find empty cell with minimum remaining values (MRV heuristic)."""
    min_candidates = 10
    best_cell = None
    best_candidates = []
    
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                candidates = get_candidates(grid, row, col)
                if len(candidates) < min_candidates:
                    min_candidates = len(candidates)
                    best_cell = (row, col)
                    best_candidates = candidates
                    if min_candidates == 0:
                        return best_cell, best_candidates
    
    return best_cell, best_candidates


def validate_initial_grid(grid):
    """Check if the initial grid has conflicting clues."""
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                num = grid[row][col]
                grid[row][col] = 0
                if not is_valid_placement(grid, row, col, num):
                    grid[row][col] = num
                    return False
                grid[row][col] = num
    return True


def solve(grid: list[list[int]]) -> bool:
    """Solve the Sudoku grid in place using backtracking with MRV heuristic."""
    cell, candidates = find_mrv_cell(grid)
    
    if cell is None:
        return True
    
    if len(candidates) == 0:
        return False
    
    row, col = cell
    
    for num in candidates:
        grid[row][col] = num
        if solve(grid):
            return True
        grid[row][col] = 0
    
    return False


def print_grid(grid):
    """Print the grid as 9 lines of 9 digits."""
    for row in grid:
        print(''.join(map(str, row)))


def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    except IOError:
        print("Invalid puzzle", file=sys.stderr)
        sys.exit(2)
    
    grid = parse_grid(lines)
    
    if grid is None:
        print("Invalid puzzle", file=sys.stderr)
        sys.exit(2)
    
    if not validate_initial_grid(grid):
        print("Invalid puzzle", file=sys.stderr)
        sys.exit(2)
    
    if solve(grid):
        print_grid(grid)
    else:
        print("No solution", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
