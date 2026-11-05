import sys


def parse_puzzle(content: str) -> list[list[int]]:
    """Parse puzzle from string content. Returns 9x9 grid or raises ValueError."""
    lines = []
    for line in content.splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    
    if len(lines) != 9:
        raise ValueError("Invalid puzzle: expected 9 lines")
    
    grid = []
    for line in lines:
        if len(line) != 9:
            raise ValueError("Invalid puzzle: expected 9 characters per line")
        row = []
        for ch in line:
            if ch in '0.':
                row.append(0)
            elif ch in '123456789':
                row.append(int(ch))
            else:
                raise ValueError(f"Invalid puzzle: invalid character '{ch}'")
        grid.append(row)
    
    return grid


def is_valid_grid(grid: list[list[int]]) -> bool:
    """Check if the initial grid has no conflicts among given clues."""
    # Check rows
    for row in grid:
        seen = set()
        for val in row:
            if val != 0:
                if val in seen:
                    return False
                seen.add(val)
    
    # Check columns
    for col in range(9):
        seen = set()
        for row in range(9):
            val = grid[row][col]
            if val != 0:
                if val in seen:
                    return False
                seen.add(val)
    
    # Check 3x3 boxes
    for box_row in range(3):
        for box_col in range(3):
            seen = set()
            for i in range(3):
                for j in range(3):
                    val = grid[box_row * 3 + i][box_col * 3 + j]
                    if val != 0:
                        if val in seen:
                            return False
                        seen.add(val)
    
    return True


def get_candidates(grid: list[list[int]], row: int, col: int) -> set[int]:
    """Get the set of valid candidates for a cell."""
    if grid[row][col] != 0:
        return set()
    
    candidates = set(range(1, 10))
    
    # Remove values in the same row
    for val in grid[row]:
        candidates.discard(val)
    
    # Remove values in the same column
    for r in range(9):
        candidates.discard(grid[r][col])
    
    # Remove values in the same 3x3 box
    box_row, box_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            candidates.discard(grid[box_row + i][box_col + j])
    
    return candidates


def solve(grid: list[list[int]]) -> bool:
    """
    Solve the Sudoku puzzle in place using backtracking with MRV heuristic.
    Returns True if a solution is found, False otherwise.
    """
    # Find the empty cell with the fewest candidates (MRV heuristic)
    min_candidates = None
    min_cell = None
    
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                candidates = get_candidates(grid, row, col)
                if len(candidates) == 0:
                    # No valid candidates for this cell, backtrack
                    return False
                if min_candidates is None or len(candidates) < len(min_candidates):
                    min_candidates = candidates
                    min_cell = (row, col)
                    # Optimization: if only one candidate, no need to search further
                    if len(candidates) == 1:
                        break
        if min_cell is not None and len(min_candidates) == 1:
            break
    
    # If no empty cell found, puzzle is solved
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
        print(''.join(str(val) for val in row))


def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        sys.exit(2)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except IOError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(2)
    
    try:
        grid = parse_puzzle(content)
    except ValueError:
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


if __name__ == "__main__":
    main()
