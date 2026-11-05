import sys


def cands(g, r, c):
    br, bc = r // 3 * 3, c // 3 * 3
    used = set(g[r]) | {g[i][c] for i in range(9)} | {g[i][j] for i in range(br, br + 3) for j in range(bc, bc + 3)}
    return [v for v in range(1, 10) if v not in used]


def solve(grid):
    best = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cand = cands(grid, r, c)
                if best is None or len(cand) < len(best[2]):
                    best = (r, c, cand)
                    if not cand:
                        return False
    if best is None:
        return True
    r, c, cand = best
    for v in cand:
        grid[r][c] = v
        if solve(grid):
            return True
    grid[r][c] = 0
    return False


def groups(g):
    cols = [list(col) for col in zip(*g)]
    boxes = [[g[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)]
             for br in range(0, 9, 3) for bc in range(0, 9, 3)]
    return g + cols + boxes


def consistent(g):
    for grp in groups(g):
        vals = [x for x in grp if x]
        if len(vals) != len(set(vals)):
            return False
    return True


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f if l.strip()]
    if len(lines) != 9 or any(len(l) != 9 or set(l) - set('0123456789.') for l in lines):
        print('Invalid puzzle')
        sys.exit(2)
    grid = [[0 if ch == '.' else int(ch) for ch in l] for l in lines]
    if not consistent(grid):
        print('Invalid puzzle')
        sys.exit(2)
    if not solve(grid):
        print('No solution')
        sys.exit(1)
    print('\n'.join(''.join(map(str, row)) for row in grid))
