import sys

def solve(g):
    best = None
    for r in range(9):
        for c in range(9):
            if not g[r][c]:
                b = {g[r][j] for j in range(9)} | {g[i][c] for i in range(9)} | {g[i][j] for i in range(r//3*3, r//3*3+3) for j in range(c//3*3, c//3*3+3)}
                m = [v for v in range(1, 10) if v not in b]
                if not m:
                    return False
                if best is None or len(m) < len(best[2]):
                    best = (r, c, m)
    if not best:
        return True
    r, c, m = best
    for v in m:
        g[r][c] = v
        if solve(g):
            return True
    g[r][c] = 0
    return False

def main():
    try:
        with open(sys.argv[1]) as f:
            rows = [''.join(l.split()) for l in f]
        rows = [l for l in rows if l]
        if len(rows) != 9 or any(len(l) != 9 or set(l) - set("0123456789.") for l in rows):
            raise ValueError
        g = [[0 if ch == '.' else int(ch) for ch in l] for l in rows]
        units = [[(r, c) for c in range(9)] for r in range(9)] + [[(r, c) for r in range(9)] for c in range(9)] + [[(R+r, C+c) for r in range(3) for c in range(3)] for R in (0, 3, 6) for C in (0, 3, 6)]
        for u in units:
            vals = [g[r][c] for r, c in u if g[r][c]]
            if len(vals) != len(set(vals)):
                raise ValueError
    except (IndexError, OSError, UnicodeError, ValueError):
        print("Invalid puzzle")
        sys.exit(2)
    if not solve(g):
        print("No solution")
        sys.exit(1)
    print('\n'.join(''.join(map(str, r)) for r in g))

if __name__ == "__main__":
    main()
