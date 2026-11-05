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
        return []
    return [num for num in range(1, 10) if is_valid(grid, row, col, num)]

def solve(grid):
    min_candidates = None
    min_cell = None
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                candidates = get_candidates(grid, i, j)
                if len(candidates) == 0:
                    return False
                if min_candidates is None or len(candidates) < len(min_candidates):
                    min_candidates = candidates
                    min_cell = (i, j)
    if min_cell is None:
        return True
    row, col = min_cell
    for num in min_candidates:
        grid[row][col] = num
        if solve(grid):
            return True
        grid[row][col] = 0
    return False

def parse_input(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        grid_lines = [line.strip() for line in lines if line.strip()]
        if len(grid_lines) != 9:
            return None
        grid = []
        for line in grid_lines:
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
        return grid
    except:
        return None

def validate_initial(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                num = grid[i][j]
                grid[i][j] = 0
                if not is_valid(grid, i, j, num):
                    return False
                grid[i][j] = num
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py <puzzle.txt>")
        sys.exit(2)
    grid = parse_input(sys.argv[1])
    if grid is None:
        print("Invalid puzzle")
        sys.exit(2)
    if not validate_initial(grid):
        print("Invalid puzzle")
        sys.exit(2)
    if solve(grid):
        for row in grid:
            print(''.join(map(str, row)))
    else:
        print("No solution")
        sys.exit(1)

if __name__ == "__main__":
    main()
