import sys


def candidates(g, r, c):
    br, bc = r - r % 3, c - c % 3
    used = set(g[r]) | {g[i][c] for i in range(9)} | {g[i][j] for i in range(br, br + 3) for j in range(bc, bc + 3)}
    return [d for d in range(1, 10) if d not in used]


def valid(g):
    units = [g[r] for r in range(9)]
    units += [[g[r][c] for r in range(9)] for c in range(9)]
    units += [[g[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)] for br in (0, 3, 6) for bc in (0, 3, 6)]
    for u in units:
        d = [v for v in u if v]
        if len(d) != len(set(d)):
            return False
    return True


def solve(grid):
    best = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cs = candidates(grid, r, c)
                if not cs:
                    return False
                if best is None or len(cs) < len(best[2]):
                    best = (r, c, cs)
    if best is None:
        return True
    r, c, cs = best
    for d in cs:
        grid[r][c] = d
        if solve(grid):
            return True
    grid[r][c] = 0
    return False


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        rows = ["".join(line.split()) for line in f]
    rows = [row for row in rows if row]
    if len(rows) != 9 or any(len(row) != 9 or set(row) - set("0123456789.") for row in rows):
        print("Invalid puzzle")
        sys.exit(2)
    grid = [[0 if ch in "0." else int(ch) for ch in row] for row in rows]
    if not valid(grid):
        print("Invalid puzzle")
        sys.exit(2)
    if not solve(grid):
        print("No solution")
        sys.exit(1)
    for row in grid:
        print("".join(map(str, row)))
