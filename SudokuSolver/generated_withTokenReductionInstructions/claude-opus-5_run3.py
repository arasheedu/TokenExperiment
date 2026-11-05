import sys


def candidates(grid, r, c):
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
                cand = candidates(grid, r, c)
                if not cand:
                    return False
                if best is None or len(cand) < len(best[2]):
                    best = (r, c, cand)
                    if len(cand) == 1:
                        break
        else:
            continue
        break
    if best is None:
        return True
    r, c, cand = best
    for v in cand:
        grid[r][c] = v
        if solve(grid):
            return True
    grid[r][c] = 0
    return False


def parse(text):
    rows = [line.strip() for line in text.splitlines() if line.strip()]
    if len(rows) != 9 or any(len(row) != 9 for row in rows):
        return None
    grid = []
    for row in rows:
        line = []
        for ch in row:
            if ch in '0.':
                line.append(0)
            elif ch.isdigit():
                line.append(int(ch))
            else:
                return None
        grid.append(line)
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                grid[r][c] = 0
                if v not in candidates(grid, r, c):
                    return None
                grid[r][c] = v
    return grid


def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        sys.exit(2)
    try:
        text = open(sys.argv[1]).read()
    except OSError as e:
        print(e, file=sys.stderr)
        sys.exit(2)
    grid = parse(text)
    if grid is None:
        print("Invalid puzzle")
        sys.exit(2)
    if not solve(grid):
        print("No solution")
        sys.exit(1)
    print('\n'.join(''.join(map(str, row)) for row in grid))


if __name__ == '__main__':
    main()
