import sys

def solve(grid):
    best, best_pos = None, None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                used = set()
                for k in range(9):
                    used.add(grid[r][k])
                    used.add(grid[k][c])
                br, bc = (r//3)*3, (c//3)*3
                for dr in range(3):
                    for dc in range(3):
                        used.add(grid[br+dr][bc+dc])
                cands = [d for d in range(1,10) if d not in used]
                if not cands:
                    return False
                if best is None or len(cands) < len(best):
                    best, best_pos = cands, (r, c)
    if best_pos is None:
        return True
    r, c = best_pos
    for d in best:
        grid[r][c] = d
        if solve(grid):
            return True
        grid[r][c] = 0
    return False

def parse(path):
    with open(path) as f:
        raw = f.read()
    rows = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if len(line) != 9 or not all(ch in '0123456789.' for ch in line):
            print("Invalid puzzle"); sys.exit(2)
        rows.append([0 if ch in '0.' else int(ch) for ch in line])
    if len(rows) != 9:
        print("Invalid puzzle"); sys.exit(2)
    return rows

def validate(grid):
    for i in range(9):
        row = [v for v in grid[i] if v]
        col = [grid[r][i] for r in range(9) if grid[r][i]]
        if len(row) != len(set(row)) or len(col) != len(set(col)):
            return False
    for br in range(0,9,3):
        for bc in range(0,9,3):
            box = [grid[br+dr][bc+dc] for dr in range(3) for dc in range(3) if grid[br+dr][bc+dc]]
            if len(box) != len(set(box)):
                return False
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt"); sys.exit(2)
    grid = parse(sys.argv[1])
    if not validate(grid):
        print("Invalid puzzle"); sys.exit(2)
    if not solve(grid):
        print("No solution"); sys.exit(1)
    for row in grid:
        print(''.join(map(str, row)))
