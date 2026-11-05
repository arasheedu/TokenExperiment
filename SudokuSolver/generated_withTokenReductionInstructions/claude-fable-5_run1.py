import sys

def candidates(g, r, c):
    used = set(g[r]) | {g[i][c] for i in range(9)}
    br, bc = r - r % 3, c - c % 3
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            used.add(g[i][j])
    return [v for v in range(1, 10) if v not in used]

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
    for v in cands:
        grid[r][c] = v
        if solve(grid):
            return True
    grid[r][c] = 0
    return False

def main():
    try:
        with open(sys.argv[1]) as f:
            lines = [''.join(ln.split()) for ln in f]
        lines = [ln for ln in lines if ln]
        if len(lines) != 9 or any(len(ln) != 9 for ln in lines):
            raise ValueError
        grid = [[0 if ch in '0.' else int(ch) for ch in ln] for ln in lines]
        for r in range(9):
            for c in range(9):
                v = grid[r][c]
                if v:
                    grid[r][c] = 0
                    if v not in candidates(grid, r, c):
                        raise ValueError
                    grid[r][c] = v
    except (ValueError, IndexError, OSError):
        print("Invalid puzzle")
        sys.exit(2)
    if solve(grid):
        print('\n'.join(''.join(map(str, row)) for row in grid))
    else:
        print("No solution")
        sys.exit(1)

if __name__ == '__main__':
    main()
