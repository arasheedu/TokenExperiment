import sys

def solve(g):
    best = None
    for r in range(9):
        for c in range(9):
            if not g[r][c]:
                br, bc = r // 3 * 3, c // 3 * 3
                used = {g[r][i] for i in range(9)} | {g[i][c] for i in range(9)} | {g[br + i // 3][bc + i % 3] for i in range(9)}
                cand = [v for v in range(1, 10) if v not in used]
                if not cand:
                    return False
                if best is None or len(cand) < len(best[2]):
                    best = (r, c, cand)
    if best is None:
        return True
    r, c, cand = best
    for v in cand:
        g[r][c] = v
        if solve(g):
            return True
    g[r][c] = 0
    return False

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python sudoku.py puzzle.txt")
    try:
        with open(sys.argv[1]) as f:
            text = f.read()
    except OSError as e:
        sys.exit(str(e))
    lines = [s for s in (''.join(l.split()) for l in text.splitlines()) if s]
    if len(lines) != 9 or any(len(l) != 9 or any(ch not in "0123456789." for ch in l) for l in lines):
        print("Invalid puzzle")
        sys.exit(2)
    g = [[0 if ch == '.' else int(ch) for ch in l] for l in lines]
    units = g + [list(col) for col in zip(*g)] + [[g[r + i // 3][c + i % 3] for i in range(9)] for r in (0, 3, 6) for c in (0, 3, 6)]
    for u in units:
        vals = [x for x in u if x]
        if len(vals) != len(set(vals)):
            print("Invalid puzzle")
            sys.exit(2)
    if not solve(g):
        print("No solution")
        sys.exit(1)
    print('\n'.join(''.join(map(str, row)) for row in g))

if __name__ == "__main__":
    main()
