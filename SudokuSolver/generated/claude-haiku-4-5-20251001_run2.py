import sys
from typing import Optional


def parse_input(filename: str) -> Optional[list[list[int]]]:
    """Parse a Sudoku puzzle from a file.
    
    Returns a 9x9 grid or None if invalid.
    Raises SystemExit with code 2 if puzzle is invalid.
    """
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except (FileNotFoundError, IOError):
        print("Invalid puzzle")
        sys.exit(2)
    
    # Filter out blank lines and strip whitespace
    lines = [line.strip() for line in lines if line.strip()]
    
    # Check we have exactly 9 lines
    if len(lines) != 9:
        print("Invalid puzzle")
        sys.exit(2)
    
    grid = []
    for line in lines:
        # Check line has exactly 9 characters
        if len(line) != 9:
            print("Invalid puzzle")
            sys.exit(2)
        
        row = []
        for char in line:
            if char in '0.':
                row.append(0)
            elif char in '123456789':
                row.append(int(char))
            else:
                print("Invalid puzzle")
                sys.exit(2)
        grid.append(row)
    
    # Validate the initial puzzle (check for conflicts in given clues)
    if not is_valid_initial(grid):
        print("Invalid puzzle")
        sys.exit(2)
    
    return grid


def is_valid_initial(grid: list[list[int]]) -> bool:
    """Check if the initial puzzle has no conflicts in given clues."""
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                val = grid[i][j]
                grid[i][j] = 0  # Temporarily remove to check
                if not is_valid_placement(grid, i, j, val):
                    grid[i][j] = val  # Restore
                    return False
                grid[i][j] = val  # Restore
    return True


def is_valid_placement(grid: list[list[int]], row: int, col: int, num: int) -> bool:
    """Check if placing num at (row, col) is valid."""
    # Check row
    for j in range(9):
        if grid[row][j] == num:
            return False
    
    # Check column
    for i in range(9):
        if grid[i][col] == num:
            return False
    
    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if grid[i][j] == num:
                return False
    
    return True


def get_candidates(grid: list[list[int]], row: int, col: int) -> set[int]:
    """Get the set of valid candidates for a cell."""
    if grid[row][col] != 0:
        return set()
    
    candidates = set(range(1, 10))
    
    # Remove numbers in the same row
    for j in range(9):
        candidates.discard(grid[row][j])
    
    # Remove numbers in the same column
    for i in range(9):
        candidates.discard(grid[i][col])
    
    # Remove numbers in the same 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            candidates.discard(grid[i][j])
    
    return candidates


def solve(grid: list[list[int]]) -> bool:
    """Solve the Sudoku puzzle using backtracking with MRV heuristic.
    
    Modifies grid in place and returns True if solved, False if no solution.
    """
    # Find the empty cell with minimum remaining values (MRV heuristic)
    min_candidates = None
    min_cell = None
    
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                candidates = get_candidates(grid, i, j)
                if len(candidates) == 0:
                    return False  # No valid candidates, backtrack
                if min_candidates is None or len(candidates) < len(min_candidates):
                    min_candidates = candidates
                    min_cell = (i, j)
    
    # No empty cells found, puzzle is solved
    if min_cell is None:
        return True
    
    row, col = min_cell
    
    # Try each candidate
    for num in min_candidates:
        grid[row][col] = num
        if solve(grid):
            return True
        grid[row][col] = 0  # Backtrack
    
    return False


def print_grid(grid: list[list[int]]) -> None:
    """Print the grid as 9 lines of 9 digits."""
    for row in grid:
        print(''.join(str(cell) for cell in row))


def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt")
        sys.exit(1)
    
    filename = sys.argv[1]
    grid = parse_input(filename)
    
    if solve(grid):
        print_grid(grid)
    else:
        print("No solution")
        sys.exit(1)


if __name__ == "__main__":
    main()
