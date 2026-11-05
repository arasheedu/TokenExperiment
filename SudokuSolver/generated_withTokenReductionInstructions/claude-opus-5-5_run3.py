import sys

def cands(g, r, c):
    s = {g[r][i] for i in range(9)} | {g[i][c] for i in range(9)}
    br, bc = r // 3 * 3, c // 3 * 3
    s |= {g[i][j] for i in range(br, br + 3) for j in range(bc, bc + 3)}
    return [d for d in range(1, 10) if d not in s]

def solve(grid: list[list[int]]) -> bool:
    best = None
    for r in range(9):
        for c in range(9):
            if not grid[r][c]:
                cs = cands(grid, r, c)
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

def valid(g):
    for r in range(9):
        for c in range(9):
            v = g[r][c]
            if v:
                g[r][c] = 0
                ok = v in cands(g, r, c)
                g[r][c] = v
                if not ok:
                    return False
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt")
        sys.exit(2)
    try:
        with open(sys.argv[1]) as f:
            text = f.read()
    except (OSError, UnicodeDecodeError):
        print("Invalid puzzle")
        sys.exit(2)
    rows = [l for l in (''.join(x.split()) for x in text.splitlines()) if l]
    if len(rows) != 9 or any(len(l) != 9 or any(ch not in '.0123456789' for ch in l) for l in rows):
        print("Invalid puzzle")
        sys.exit(2)
    g = [[0 if ch == '.' else int(ch) for ch in l] for l in rows]
    if not valid(g):
        print("Invalid puzzle")
        sys.exit(2)
    if not solve(g):
        print("No solution")
        sys.exit(1)
    print('\n'.join(''.join(map(str, row)) for row in g))

if __name__ == "__main__":
    main()
