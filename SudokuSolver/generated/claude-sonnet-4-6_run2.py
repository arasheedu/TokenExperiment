import sys

def parse(path):
    with open(path) as f:
        raw = f.read()
    rows = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
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
        rows.append(row)
    if len(rows) != 9:
        print("Invalid puzzle")
        sys.exit(2)
    return rows

def is_valid_clues(grid):
    for r in range(9):
        seen = set()
        for c in range(9):
            v = grid[r][c]
            if v == 0:
                continue
            if v in seen:
                return False
            seen.add(v)
    for c in range(9):
        seen = set()
        for r in range(9):
            v = grid[r][c]
            if v == 0:
                continue
            if v in seen:
                return False
            seen.add(v)
    for br in range(3):
        for bc in range(3):
            seen = set()
            for r in range(br*3, br*3+3):
                for c in range(bc*3, bc*3+3):
                    v = grid[r][c]
                    if v == 0:
                        continue
                    if v in seen:
                        return False
                    seen.add(v)
    return True

def candidates(grid, r, c):
    used = set()
    for col in range(9):
        if grid[r][col]:
            used.add(grid[r][col])
    for row in range(9):
        if grid[row][c]:
            used.add(grid[row][c])
    br, bc = (r // 3) * 3, (c // 3) * 3
    for row in range(br, br+3):
        for col in range(bc, bc+3):
            if grid[row][col]:
                used.add(grid[row][col])
    return [v for v in range(1, 10) if v not in used]

def solve(grid: list[list[int]]) -> bool:
    # Find empty cell with fewest candidates (MRV)
    best = None
    best_cands = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cands = candidates(grid, r, c)
                if not cands:
                    return False
                if best is None or len(cands) < len(best_cands):
                    best = (r, c)
                    best_cands = cands
                    if len(best_cands) == 1:
                        break
        if best is not None and len(best_cands) == 1:
            break
    if best is None:
        return True  # No empty cells, solved
    r, c = best
    for v in best_cands:
        grid[r][c] = v
        if solve(grid):
            return True
        grid[r][c] = 0
    return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt")
        sys.exit(2)
    grid = parse(sys.argv[1])
    if not is_valid_clues(grid):
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
