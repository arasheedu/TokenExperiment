import sys


def parse_puzzle(lines: list[str]) -> list[list[int]] | None:
    """Parse puzzle from lines, return 9x9 grid or None if invalid."""
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


def is_valid_puzzle(grid: list[list[int]]) -> bool:
    """Check if the initial puzzle has no conflicts among given clues."""
    # Check rows
    for row in grid:
        seen = []
        for val in row:
            if val != 0:
                if val in seen:
                    return False
                seen.append(val)
    
    # Check columns
    for col in range(9):
        seen = []
        for row in range(9):
            val = grid[row][col]
            if val != 0:
                if val in seen:
                    return False
                seen.append(val)
    
    # Check 3x3 boxes
    for box_row in range(3):
        for box_col in range(3):
            seen = []
            for i in range(3):
                for j in range(3):
                    val = grid[box_row * 3 + i][box_col * 3 + j]
                    if val != 0:
                        if val in seen:
                            return False
                        seen.append(val)
    
    return True


def get_candidates(grid: list[list[int]], row: int, col: int) -> set[int]:
    """Get legal candidates for a cell."""
    if grid[row][col] != 0:
        return set()
    
    used = set()
    
    # Check row
    for c in range(9):
        if grid[row][c] != 0:
            used.add(grid[row][c])
    
    # Check column
    for r in range(9):
        if grid[r][col] != 0:
            used.add(grid[r][col])
    
    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            val = grid[box_row + i][box_col + j]
            if val != 0:
                used.add(val)
    
    return set(range(1, 10)) - used


def solve(grid: list[list[int]]) -> bool:
    """Solve the Sudoku puzzle in place using backtracking with MRV heuristic.
    
    Returns True if solved successfully, False if no solution exists.
    """
    # Find empty cell with minimum remaining values (MRV heuristic)
    min_candidates = None
    min_cell = None
    
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                candidates = get_candidates(grid, row, col)
                if len(candidates) == 0:
                    return False  # No valid candidates, dead end
                if min_candidates is None or len(candidates) < len(min_candidates):
                    min_candidates = candidates
                    min_cell = (row, col)
    
    # No empty cells, puzzle is solved
    if min_cell is None:
        return True
    
    row, col = min_cell
    
    # Try each candidate
    for val in min_candidates:
        grid[row][col] = val
        if solve(grid):
            return True
        grid[row][col] = 0
    
    return False


def print_grid(grid: list[list[int]]) -> None:
    """Print the grid as 9 lines of 9 digits."""
    for row in grid:
        print(''.join(str(cell) for cell in row))


def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        sys.exit(2)
    
    try:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    except IOError:
        print("Invalid puzzle")
        sys.exit(2)
    
    grid = parse_puzzle(lines)
    
    if grid is None:
        print("Invalid puzzle")
        sys.exit(2)
    
    if not is_valid_puzzle(grid):
        print("Invalid puzzle")
        sys.exit(2)
    
    if solve(grid):
        print_grid(grid)
    else:
        print("No solution")
        sys.exit(1)


if __name__ == "__main__":
    main()
