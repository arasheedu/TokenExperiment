#!/usr/bin/env python3
import sys


def parse_puzzle(filename):
    """Parse puzzle from file. Returns 9x9 grid or None if malformed."""
    try:
        with open(filename, 'r') as f:
            lines = []
            for line in f:
                line = line.strip()
                if not line:
                    continue
                lines.append(line)
            
            if len(lines) != 9:
                return None
            
            grid = []
            for line in lines:
                # Remove whitespace
                line = line.replace(' ', '').replace('\t', '')
                if len(line) != 9:
                    return None
                
                row = []
                for char in line:
                    if char == '.' or char == '0':
                        row.append(0)
                    elif char in '123456789':
                        row.append(int(char))
                    else:
                        return None
                grid.append(row)
            
            return grid
    except (IOError, OSError):
        return None


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
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if grid[r][c] == num:
                return False
    
    return True


def is_valid_grid(grid):
    """Check if the initial grid has no conflicts."""
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


def get_candidates(grid, row, col):
    """Get all legal candidates for cell (row, col)."""
    if grid[row][col] != 0:
        return []
    
    candidates = []
    for num in range(1, 10):
        if is_valid_placement(grid, row, col, num):
            candidates.append(num)
    return candidates


def find_best_cell(grid):
    """Find empty cell with fewest candidates (MRV heuristic)."""
    min_candidates = 10
    best_cell = None
    
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                candidates = get_candidates(grid, row, col)
                if len(candidates) < min_candidates:
                    min_candidates = len(candidates)
                    best_cell = (row, col, candidates)
                    if min_candidates == 0:
                        return best_cell
    
    return best_cell


def solve(grid: list[list[int]]) -> bool:
    """Solve the sudoku grid in place using backtracking. Returns True if solved."""
    cell_info = find_best_cell(grid)
    
    if cell_info is None:
        return True
    
    row, col, candidates = cell_info
    
    if len(candidates) == 0:
        return False
    
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
    
    grid = parse_puzzle(sys.argv[1])
    
    if grid is None:
        print("Invalid puzzle")
        sys.exit(2)
    
    if not is_valid_grid(grid):
        print("Invalid puzzle")
        sys.exit(2)
    
    if solve(grid):
        print_grid(grid)
    else:
        print("No solution")
        sys.exit(1)


if __name__ == '__main__':
    main()
