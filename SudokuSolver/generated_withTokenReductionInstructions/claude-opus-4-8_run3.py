import sys

def candidates(grid, r, c):
    used = set()
    for i in range(9):
        used.add(grid[r][i])
        used.add(grid[i][c])
    br, bc = 3 * (r // 3), 3 * (c // 3)
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            used.add(grid[i][j])
    return [d for d in range(1, 10) if d not in used]

def solve(grid):
    best = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cands = candidates(grid, r, c)
                if best is None or len(cands) < len(best[2]):
                    best = (r, c, cands)
                    if not cands:
                        return False
    if best is None:
        return True
    r, c, cands = best
    for d in cands:
        grid[r][c] = d
        if solve(grid):
            return True
        grid[r][c] = 0
    return False

def valid(grid):
    for i in range(9):
        row = [grid[i][j] for j in range(9) if grid[i][j]]
        col = [grid[j][i] for j in range(9) if grid[j][i]]
        if len(set(row)) != len(row) or len(set(col)) != len(col):
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            box = [grid[br + i][bc + j] for i in range(3) for j in range(3) if grid[br + i][bc + j]]
            if len(set(box)) != len(box):
                return False
    return True

def main():
    if len(sys.argv) != 2:
        print("Invalid puzzle")
        sys.exit(2)
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f if l.strip()]
    if len(lines) != 9 or any(len(l) != 9 for l in lines):
        print("Invalid puzzle")
        sys.exit(2)
    grid = []
    for l in lines:
        row = []
        for ch in l:
            if ch in ".0":
                row.append(0)
            elif ch in "123456789":
                row.append(int(ch))
            else:
                print("Invalid puzzle")
                sys.exit(2)
        grid.append(row)
    if not valid(grid):
        print("Invalid puzzle")
        sys.exit(2)
    if not solve(grid):
        print("No solution")
        sys.exit(1)
    print("\n".join("".join(map(str, row)) for row in grid))

if __name__ == "__main__":
    main()
