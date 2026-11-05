import sys

def solve(grid):
    best = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                br, bc = r // 3 * 3, c // 3 * 3
                s = set(range(1, 10)) - set(grid[r]) - {grid[i][c] for i in range(9)} - {grid[br + i][bc + j] for i in range(3) for j in range(3)}
                if not s:
                    return False
                if best is None or len(s) < len(best[2]):
                    best = (r, c, s)
    if best is None:
        return True
    r, c, s = best
    for v in s:
        grid[r][c] = v
        if solve(grid):
            return True
    grid[r][c] = 0
    return False

def main():
    try:
        with open(sys.argv[1]) as f:
            rows = ["".join(l.split()) for l in f]
    except (OSError, ValueError, IndexError):
        rows = []
    rows = [l for l in rows if l]
    if len(rows) != 9 or any(len(l) != 9 or set(l) - set("0123456789.") for l in rows):
        print("Invalid puzzle")
        sys.exit(2)
    g = [[0 if ch == "." else int(ch) for ch in l] for l in rows]
    boxes = [[g[r + i][c + j] for i in range(3) for j in range(3)] for r in (0, 3, 6) for c in (0, 3, 6)]
    for u in [*g, *zip(*g), *boxes]:
        d = [x for x in u if x]
        if len(d) != len(set(d)):
            print("Invalid puzzle")
            sys.exit(2)
    if not solve(g):
        print("No solution")
        sys.exit(1)
    print("\n".join("".join(map(str, r)) for r in g))

if __name__ == "__main__":
    main()
