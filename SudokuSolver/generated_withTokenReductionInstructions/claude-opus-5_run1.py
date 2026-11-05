import sys


def _cands(grid, r, c):
    used = set(grid[r])
    used |= {grid[i][c] for i in range(9)}
    br, bc = r - r % 3, c - c % 3
    used |= {grid[i][j] for i in range(br, br + 3) for j in range(bc, bc + 3)}
    return [v for v in range(1, 10) if v not in used]


def solve(grid: list[list[int]]) -> bool:
    best = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cs = _cands(grid, r, c)
                if not cs:
                    return False
                if best is None or len(cs) < len(best[2]):
                    best = (r, c, cs)
                    if len(cs) == 1:
                        break
        if best and len(best[2]) == 1:
            break
    if best is None:
        return True
    r, c, cs = best
    for v in cs:
        grid[r][c] = v
        if solve(grid):
            return True
    grid[r][c] = 0
    return False


def _parse(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if len(lines) != 9:
        return None
    grid = []
    for line in lines:
        if len(line) != 9 or any(ch not in "0.123456789" for ch in line):
            return None
        grid.append([0 if ch in "0." else int(ch) for ch in line])
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                grid[r][c] = 0
                ok = v in _cands(grid, r, c)
                grid[r][c] = v
                if not ok:
                    return None
    return grid


def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        sys.exit(2)
    try:
        with open(sys.argv[1]) as f:
            text = f.read()
    except OSError as e:
        print(e, file=sys.stderr)
        sys.exit(2)
    grid = _parse(text)
    if grid is None:
        print("Invalid puzzle")
        sys.exit(2)
    if not solve(grid):
        print("No solution")
        sys.exit(1)
    print("\n".join("".join(map(str, row)) for row in grid))


if __name__ == "__main__":
    main()
