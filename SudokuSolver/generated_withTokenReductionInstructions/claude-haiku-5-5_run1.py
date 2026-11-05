import sys


def candidates(grid, r, c):
    used = set(grid[r]) | {grid[i][c] for i in range(9)}
    br, bc = r // 3 * 3, c // 3 * 3
    used |= {grid[i][j] for i in range(br, br + 3) for j in range(bc, bc + 3)}
    return [d for d in range(1, 10) if d not in used]


def solve(grid):
    best = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cand = candidates(grid, r, c)
                if best is None or len(cand) < len(best[2]):
                    best = (r, c, cand)
    if best is None:
        return True
    r, c, cand = best
    for d in cand:
        grid[r][c] = d
        if solve(grid):
            return True
    grid[r][c] = 0
    return False


def main():
    with open(sys.argv[1]) as f:
        rows = ["".join(line.split()) for line in f]
    rows = [row for row in rows if row]
    if len(rows) != 9 or any(len(row) != 9 for row in rows) or any(ch not in "0123456789." for row in rows for ch in row):
        print("Invalid puzzle")
        sys.exit(2)
    grid = [[0 if ch == "." else int(ch) for ch in row] for row in rows]
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                grid[r][c] = 0
                ok = v in candidates(grid, r, c)
                grid[r][c] = v
                if not ok:
                    print("Invalid puzzle")
                    sys.exit(2)
    if not solve(grid):
        print("No solution")
        sys.exit(1)
    print("\n".join("".join(map(str, row)) for row in grid))


if __name__ == "__main__":
    main()
