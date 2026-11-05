import sys


def parse_puzzle(filename):
    """Parse puzzle from file and return a 9x9 grid."""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Invalid puzzle")
        sys.exit(2)
    
    grid = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if len(line) != 9:
            print("Invalid puzzle")
            sys.exit(2)
        
        row = []
        for char in line:
            if char == '0' or char == '.':
                row.append(0)
            elif char.isdigit() and '1' <= char <= '9':
                row.append(int(char))
            else:
                print("Invalid puzzle")
                sys.exit(2)
        grid.append(row)
    
    if len(grid) != 9:
        print("Invalid puzzle")
        sys.exit(2)
    
    return grid


def is_valid(grid, row, col, num):
    """Check if placing num at (row, col) is valid."""
    # Check row
    if num in grid[row]:
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


def get_candidates(grid, row, col):
    """Get list of valid candidates for a cell."""
    if grid[row][col] != 0:
        return []
    
    candidates = []
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            candidates.append(num)
    return candidates


def find_mrv_cell(grid):
    """Find empty cell with minimum remaining values (MRV heuristic)."""
    min_candidates = None
    best_cell = None
    
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                candidates = get_candidates(grid, row, col)
                
                # If no valid candidates, puzzle is unsolvable
                if len(candidates) == 0:
                    return None, None, []
                
                if min_candidates is None or len(candidates) < len(min_candidates):
                    min_candidates = candidates
                    best_cell = (row, col)
    
    if best_cell is None:
        return None, None, []
    
    return best_cell[0], best_cell[1], min_candidates


def solve(grid):
    """Solve the sudoku puzzle using backtracking with MRV heuristic."""
    row, col, candidates = find_mrv_cell(grid)
    
    # No empty cell found - puzzle is solved
    if row is None:
        return True
    
    # No valid candidates for this cell - backtrack
    if len(candidates) == 0:
        return False
    
    # Try each candidate
    for num in candidates:
        grid[row][col] = num
        
        if solve(grid):
            return True
        
        # Backtrack
        grid[row][col] = 0
    
    return False


def validate_initial_grid(grid):
    """Validate that initial grid has no conflicts."""
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                num = grid[row][col]
                grid[row][col] = 0
                
                if not is_valid(grid, row, col, num):
                    grid[row][col] = num
                    return False
                
                grid[row][col] = num
    
    return True


def print_grid(grid):
    """Print the solved grid."""
    for row in grid:
        print(''.join(str(cell) for cell in row))


def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt")
        sys.exit(2)
    
    grid = parse_puzzle(sys.argv[1])
    
    if not validate_initial_grid(grid):
        print("Invalid puzzle")
        sys.exit(2)
    
    if solve(grid):
        print_grid(grid)
    else:
        print("No solution")
        sys.exit(1)


if __name__ == "__main__":
    main()
