import sys

def solve(g):
    b = None
    for r in range(9):
        for c in range(9):
            if g[r][c] == 0:
                R, C = r // 3 * 3, c // 3 * 3
                used = {g[r][i] for i in range(9)} | {g[i][c] for i in range(9)} | {g[R + i][C + j] for i in range(3) for j in range(3)}
                cand = [v for v in range(1, 10) if v not in used]
                if not cand:
                    return False
                if b is None or len(cand) < len(b[2]):
                    b = (r, c, cand)
    if b is None:
        return True
    r, c, cand = b
    for v in cand:
        g[r][c] = v
        if solve(g):
            return True
    g[r][c] = 0
    return False

if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as f:
            rows = [''.join(l.split()) for l in f]
        rows = [l for l in rows if l]
        if len(rows) != 9 or any(len(l) != 9 or set(l) - set("0123456789.") for l in rows):
            raise ValueError
        g = [[0 if ch == '.' else int(ch) for ch in l] for l in rows]
        units = [[(r, c) for c in range(9)] for r in range(9)] + [[(r, c) for r in range(9)] for c in range(9)] + [[(R + i, C + j) for i in range(3) for j in range(3)] for R in (0, 3, 6) for C in (0, 3, 6)]
        for u in units:
            v = [g[r][c] for r, c in u if g[r][c]]
            if len(set(v)) != len(v):
                raise ValueError
    except (IndexError, OSError, ValueError):
        print("Invalid puzzle")
        sys.exit(2)
    if not solve(g):
        print("No solution")
        sys.exit(1)
    for row in g:
        print(''.join(map(str, row)))
