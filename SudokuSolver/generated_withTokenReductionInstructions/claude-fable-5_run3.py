import sys

def candidates(g, r, c):
    used = set(g[r]) | {g[i][c] for i in range(9)}
    br, bc = r - r % 3, c - c % 3
    for i in range(br, br + 3):
        used.update(g[i][bc:bc + 3])
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

def main():
    if len(sys.argv) != 2:
        print("Invalid puzzle")
        sys.exit(2)
    try:
        with open(sys.argv[1]) as f:
            lines = ["".join(ln.split()) for ln in f]
    except OSError:
        print("Invalid puzzle")
        sys.exit(2)
    lines = [ln for ln in lines if ln]
    if len(lines) != 9 or any(len(ln) != 9 for ln in lines) or any(ch not in "0123456789." for ln in lines for ch in ln):
        print("Invalid puzzle")
        sys.exit(2)
    grid = [[0 if ch == "." else int(ch) for ch in ln] for ln in lines]
    for r in range(9):
        for c in range(9):
            d = grid[r][c]
            if d:
                grid[r][c] = 0
                if d not in candidates(grid, r, c):
                    print("Invalid puzzle")
                    sys.exit(2)
                grid[r][c] = d
    if solve(grid):
        print("\n".join("".join(map(str, row)) for row in grid))
    else:
        print("No solution")
        sys.exit(1)

if __name__ == "__main__":
    main()
