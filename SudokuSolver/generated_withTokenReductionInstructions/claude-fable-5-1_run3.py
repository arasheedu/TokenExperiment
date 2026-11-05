import sys

def cands(g, r, c):
    br, bc = r - r % 3, c - c % 3
    used = set(g[r]) | {g[i][c] for i in range(9)} | {g[i][j] for i in range(br, br + 3) for j in range(bc, bc + 3)}
    return [v for v in range(1, 10) if v not in used]

def solve(g):
    best = None
    for r in range(9):
        for c in range(9):
            if g[r][c] == 0:
                cs = cands(g, r, c)
                if not cs:
                    return False
                if best is None or len(cs) < len(best[2]):
                    best = (r, c, cs)
    if best is None:
        return True
    r, c, cs = best
    for v in cs:
        g[r][c] = v
        if solve(g):
            return True
    g[r][c] = 0
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
    try:
        lines = [l for l in ("".join(x.split()) for x in open(sys.argv[1])) if l]
        if len(lines) != 9 or any(len(l) != 9 or set(l) - set("0123456789.") for l in lines):
            raise ValueError
        g = [[0 if ch == "." else int(ch) for ch in l] for l in lines]
        if not valid(g):
            raise ValueError
    except (OSError, ValueError, IndexError):
        print("Invalid puzzle")
        sys.exit(2)
    if solve(g):
        print("\n".join("".join(map(str, r)) for r in g))
    else:
        print("No solution")
        sys.exit(1)

if __name__ == "__main__":
    main()
