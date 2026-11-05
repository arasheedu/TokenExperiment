import sys


def parse_grid(text):
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    if len(lines) != 9:
        return None
    grid = []
    for line in lines:
        if len(line) != 9:
            return None
        row = []
        for ch in line:
            if ch in '0.':
                row.append(0)
            elif ch in '123456789':
                row.append(int(ch))
            else:
                return None
        grid.append(row)
    return grid


def is_valid(grid):
    for i in range(9):
        seen = set()
        for j in range(9):
            v = grid[i][j]
            if v != 0:
                if v in seen:
                    return False
                seen.add(v)
    for j in range(9):
        seen = set()
        for i in range(9):
            v = grid[i][j]
            if v != 0:
                if v in seen:
                    return False
                seen.add(v)
    for bi in range(3):
        for bj in range(3):
            seen = set()
            for i in range(3):
                for j in range(3):
                    v = grid[bi * 3 + i][bj * 3 + j]
                    if v != 0:
                        if v in seen:
                            return False
                        seen.add(v)
    return True


def candidates(grid, r, c):
    used = set()
    for j in range(9):
        used.add(grid[r][j])
    for i in range(9):
        used.add(grid[i][c])
    br, bc = (r // 3) * 3, (c // 3) * 3
    for i in range(3):
        for j in range(3):
            used.add(grid[br + i][bc + j])
    return [v for v in range(1, 10) if v not in used]


def solve(grid: list[list[int]]) -> bool:
    best = None
    best_cands = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cands = candidates(grid, r, c)
                if best_cands is None or len(cands) < len(best_cands):
                    best = (r, c)
                    best_cands = cands
                    if len(cands) == 0:
                        return False
    if best is None:
        return True
    r, c = best
    for v in best_cands:
        grid[r][c] = v
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
            text = f.read()
    except OSError:
        print("Invalid puzzle")
        sys.exit(2)

    grid = parse_grid(text)
    if grid is None or not is_valid(grid):
        print("Invalid puzzle")
        sys.exit(2)

    if solve(grid):
        for row in grid:
            print(''.join(str(v) for v in row))
    else:
        print("No solution")
        sys.exit(1)


if __name__ == "__main__":
    main()
