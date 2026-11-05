import sys


def candidates(grid, r, c):
    used = set()
    for i in range(9):
        used.add(grid[r][i])
        used.add(grid[i][c])
    br, bc = r - r % 3, c - c % 3
    for i in range(3):
        for j in range(3):
            used.add(grid[br + i][bc + j])
    return [d for d in range(1, 10) if d not in used]


def solve(grid):
    best = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cand = candidates(grid, r, c)
                if best is None or len(cand) < len(best[2]):
                    best = (r, c, cand)
                    if not cand:
                        return False
    if best is None:
        return True
    r, c, cand = best
    for d in cand:
        grid[r][c] = d
        if solve(grid):
            return True
        grid[r][c] = 0
    return False


def valid(grid):
    for r in range(9):
        for c in range(9):
            d = grid[r][c]
            if d == 0:
                continue
            grid[r][c] = 0
            if d not in candidates(grid, r, c):
                grid[r][c] = d
                return False
            grid[r][c] = d
    return True


def main():
    if len(sys.argv) != 2:
        print("Invalid puzzle")
        sys.exit(2)
    try:
        with open(sys.argv[1]) as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except OSError:
        print("Invalid puzzle")
        sys.exit(2)
    if len(lines) != 9:
        print("Invalid puzzle")
        sys.exit(2)
    grid = []
    for ln in lines:
        if len(ln) != 9:
            print("Invalid puzzle")
            sys.exit(2)
        row = []
        for ch in ln:
            if ch in "0.":
                row.append(0)
            elif ch in "123456789":
                row.append(int(ch))
            else:
                print("Invalid puzzle")
                sys.exit(2)
        grid.append(row)
    if not valid(grid):
        print("Invalid puzzle")
        sys.exit(2)
    if not solve(grid):
        print("No solution")
        sys.exit(1)
    print("\n".join("".join(map(str, row)) for row in grid))


if __name__ == "__main__":
    main()
