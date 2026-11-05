import sys


def parse_puzzle(lines: list[str]) -> list[list[int]]:
    """Parse puzzle from lines, returning 9x9 grid or raising ValueError."""
    grid = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(line) != 9:
            raise ValueError("Invalid line length")
        row = []
        for ch in line:
            if ch in '0.':
                row.append(0)
            elif ch in '123456789':
                row.append(int(ch))
            else:
                raise ValueError(f"Invalid character: {ch}")
        grid.append(row)
    if len(grid) != 9:
        raise ValueError("Invalid number of rows")
    return grid


def is_valid_puzzle(grid: list[list[int]]) -> bool:
    """Check if initial puzzle state has no conflicts."""
    for i in range(9):
        for j in range(9):
            val = grid[i][j]
            if val == 0:
                continue
            # Temporarily clear the cell to check for conflicts
            grid[i][j] = 0
            if not is_valid(grid, i, j, val):
                grid[i][j] = val
                return False
            grid[i][j] = val
    return True


def is_valid(grid: list[list[int]], row: int, col: int, num: int) -> bool:
    """Check if placing num at (row, col) is valid."""
    # Check row
    if num in grid[row]:
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
    """Get all valid candidates for a cell."""
    if grid[row][col] != 0:
        return set()
    
    candidates = set(range(1, 10))
    
    # Remove numbers in same row
    candidates -= set(grid[row])
    
    # Remove numbers in same column
    for i in range(9):
        candidates.discard(grid[i][col])
    
    # Remove numbers in same 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            candidates.discard(grid[i][j])
    
    return candidates


def find_mrv_cell(grid: list[list[int]]) -> tuple[int, int, set[int]] | None:
    """Find empty cell with minimum remaining values (MRV heuristic)."""
    min_candidates = None
    min_cell = None
    
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                candidates = get_candidates(grid, i, j)
                if min_candidates is None or len(candidates) < len(min_candidates):
                    min_candidates = candidates
                    min_cell = (i, j)
                    # Early exit if we find a cell with no candidates
                    if len(candidates) == 0:
                        return (i, j, candidates)
    
    if min_cell is None:
        return None
    return (min_cell[0], min_cell[1], min_candidates)


def solve(grid: list[list[int]]) -> bool:
    """Solve the Sudoku puzzle in place using backtracking with MRV heuristic."""
    result = find_mrv_cell(grid)
    
    if result is None:
        # No empty cells, puzzle is solved
        return True
    
    row, col, candidates = result
    
    if not candidates:
        # No valid candidates for this cell
        return False
    
    for num in candidates:
        grid[row][col] = num
        if solve(grid):
            return True
        grid[row][col] = 0
    
    return False


def print_grid(grid: list[list[int]]) -> None:
    """Print the grid as 9 lines of 9 digits."""
    for row in grid:
        print(''.join(str(cell) for cell in row))


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        sys.exit(2)
    
    try:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    except IOError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(2)
    
    try:
        grid = parse_puzzle(lines)
    except ValueError:
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
