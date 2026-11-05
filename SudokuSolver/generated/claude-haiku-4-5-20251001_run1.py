import sys

def solve(grid: list[list[int]]) -> bool:
    """
    Solve a Sudoku puzzle using backtracking with MRV heuristic.
    Modifies grid in place and returns True if solvable, False otherwise.
    """
    # Find the empty cell with minimum remaining values (MRV heuristic)
    min_candidates = 10
    best_cell = None
    best_candidates = None
    
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                candidates = get_candidates(grid, i, j)
                if len(candidates) == 0:
                    return False  # No valid candidates for this cell - dead end
                if len(candidates) < min_candidates:
                    min_candidates = len(candidates)
                    best_cell = (i, j)
                    best_candidates = candidates
    
    # If no empty cells found, puzzle is solved
    if best_cell is None:
        return True
    
    i, j = best_cell
    for num in best_candidates:
        grid[i][j] = num
        if solve(grid):
            return True
        grid[i][j] = 0
    
    return False


def get_candidates(grid: list[list[int]], row: int, col: int) -> list[int]:
    """Get list of valid candidates for a cell."""
    if grid[row][col] != 0:
        return []
    
    candidates = set(range(1, 10))
    
    # Remove numbers in same row
    for j in range(9):
        if grid[row][j] != 0:
            candidates.discard(grid[row][j])
    
    # Remove numbers in same column
    for i in range(9):
        if grid[i][col] != 0:
            candidates.discard(grid[i][col])
    
    # Remove numbers in same 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if grid[i][j] != 0:
                candidates.discard(grid[i][j])
    
    return sorted(list(candidates))


def parse_input(filename: str) -> list[list[int]]:
    """Parse Sudoku puzzle from file."""
    grid = []
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Invalid puzzle")
        sys.exit(2)
    
    for line in lines:
        # Skip blank lines and strip whitespace
        line = line.strip()
        if not line:
            continue
        
        # Check line length
        if len(line) != 9:
            print("Invalid puzzle")
            sys.exit(2)
        
        row = []
        for char in line:
            if char == '0' or char == '.':
                row.append(0)
            elif char in '123456789':
                row.append(int(char))
            else:
                print("Invalid puzzle")
                sys.exit(2)
        
        grid.append(row)
    
    # Check dimensions
    if len(grid) != 9:
        print("Invalid puzzle")
        sys.exit(2)
    
    # Validate no conflicts in initial puzzle
    for i in range(9):
        if len(grid[i]) != 9:
            print("Invalid puzzle")
            sys.exit(2)
    
    # Check for conflicts
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                num = grid[i][j]
                temp = grid[i][j]
                grid[i][j] = 0
                
                # Check if this number is valid at this position
                if not is_valid(grid, i, j, num):
                    print("Invalid puzzle")
                    sys.exit(2)
                
                grid[i][j] = temp
    
    return grid


def is_valid(grid: list[list[int]], row: int, col: int, num: int) -> bool:
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
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if grid[i][j] == num:
                return False
    
    return True


def print_grid(grid: list[list[int]]) -> None:
    """Print Sudoku grid."""
    for row in grid:
        print(''.join(str(num) for num in row))


def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Parse input
    grid = parse_input(filename)
    
    # Solve
    if solve(grid):
        print_grid(grid)
        sys.exit(0)
    else:
        print("No solution")
        sys.exit(1)


if __name__ == "__main__":
    main()
