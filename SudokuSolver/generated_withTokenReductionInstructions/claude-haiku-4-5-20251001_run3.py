import sys

def solve(grid):
    def is_valid(row, col, num):
        for x in range(9):
            if grid[row][x] == num or grid[x][col] == num:
                return False
        sr, sc = (row // 3) * 3, (col // 3) * 3
        for r in range(sr, sr + 3):
            for c in range(sc, sc + 3):
                if grid[r][c] == num:
                    return False
        return True

    def get_candidates(row, col):
        if grid[row][col] != 0:
            return []
        candidates = []
        for num in range(1, 10):
            if is_valid(row, col, num):
                candidates.append(num)
        return candidates

    def find_mrv_cell():
        min_candidates = None
        best_cell = None
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    candidates = get_candidates(r, c)
                    if len(candidates) == 0:
                        return None
                    if min_candidates is None or len(candidates) < len(min_candidates):
                        min_candidates = candidates
                        best_cell = (r, c)
        return best_cell, min_candidates if best_cell else (None, None)

    cell_info = find_mrv_cell()
    if cell_info[0] is None:
        return all(grid[r][c] != 0 for r in range(9) for c in range(9))

    (row, col), candidates = cell_info
    for num in candidates:
        grid[row][col] = num
        if solve(grid):
            return True
        grid[row][col] = 0
    return False

def parse_input(filename):
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        if len(lines) != 9:
            return None
        
        grid = []
        for line in lines:
            if len(line) != 9:
                return None
            row = []
            for char in line:
                if char in '0123456789.':
                    row.append(0 if char in '0.' else int(char))
                else:
                    return None
            grid.append(row)
        
        for r in range(9):
            for c in range(9):
                if grid[r][c] != 0:
                    num = grid[r][c]
                    grid[r][c] = 0
                    if not is_valid_placement(grid, r, c, num):
                        return None
                    grid[r][c] = num
        
        return grid
    except:
        return None

def is_valid_placement(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num or grid[x][col] == num:
            return False
    sr, sc = (row // 3) * 3, (col // 3) * 3
    for r in range(sr, sr + 3):
        for c in range(sc, sc + 3):
            if grid[r][c] == num:
                return False
    return True

def main():
    if len(sys.argv) != 2:
        sys.exit(2)
    
    grid = parse_input(sys.argv[1])
    if grid is None:
        print("Invalid puzzle")
        sys.exit(2)
    
    if solve(grid):
        for row in grid:
            print(''.join(map(str, row)))
    else:
        print("No solution")
        sys.exit(1)

if __name__ == '__main__':
    main()
