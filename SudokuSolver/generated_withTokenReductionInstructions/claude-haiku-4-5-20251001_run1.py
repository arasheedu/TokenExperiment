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
    if grid[row][col] != 0:
        return set()
    return {n for n in range(1, 10) if is_valid(grid, row, col, n)}

def solve(grid):
    min_candidates = 10
    best_cell = None
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                candidates = get_candidates(grid, i, j)
                if len(candidates) == 0:
                    return False
                if len(candidates) < min_candidates:
                    min_candidates = len(candidates)
                    best_cell = (i, j, candidates)
    if best_cell is None:
        return True
    row, col, candidates = best_cell
    for num in candidates:
        grid[row][col] = num
        if solve(grid):
            return True
        grid[row][col] = 0
    return False

def parse_input(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Invalid puzzle")
        sys.exit(2)
    lines = [line.strip() for line in lines if line.strip()]
    if len(lines) != 9:
        print("Invalid puzzle")
        sys.exit(2)
    grid = []
    for line in lines:
        if len(line) != 9:
            print("Invalid puzzle")
            sys.exit(2)
        row = []
        for ch in line:
            if ch in '123456789':
                row.append(int(ch))
            elif ch in '0.':
                row.append(0)
            else:
                print("Invalid puzzle")
                sys.exit(2)
        grid.append(row)
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                num = grid[i][j]
                grid[i][j] = 0
                if not is_valid(grid, i, j, num):
                    print("Invalid puzzle")
                    sys.exit(2)
                grid[i][j] = num
    return grid

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt")
        sys.exit(1)
    grid = parse_input(sys.argv[1])
    if solve(grid):
        for row in grid:
            print(''.join(map(str, row)))
    else:
        print("No solution")
        sys.exit(1)
