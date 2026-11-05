import sys


def _parse(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
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


def _valid(grid):
    for i in range(9):
        seen_r, seen_c = set(), set()
        for j in range(9):
            v = grid[i][j]
            if v:
                if v in seen_r:
                    return False
                seen_r.add(v)
            v = grid[j][i]
            if v:
                if v in seen_c:
                    return False
                seen_c.add(v)
    for br in range(3):
        for bc in range(3):
            seen = set()
            for i in range(3):
                for j in range(3):
                    v = grid[br*3+i][bc*3+j]
                    if v:
                        if v in seen:
                            return False
                        seen.add(v)
    return True


def _candidates(grid, r, c):
    used = set()
    for i in range(9):
        used.add(grid[r][i])
        used.add(grid[i][c])
    br, bc = (r // 3) * 3, (c // 3) * 3
    for i in range(3):
        for j in range(3):
            used.add(grid[br+i][bc+j])
    return [v for v in range(1, 10) if v not in used]


def solve(grid):
    best = None
    best_cands = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cands = _candidates(grid, r, c)
                if not cands:
                    return False
                if best is None or len(cands) < len(best_cands):
                    best = (r, c)
                    best_cands = cands
                    if len(cands) == 1:
                        break
        if best and len(best_cands) == 1:
            break
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
        print("Usage: python sudoku.py puzzle.txt")
        sys.exit(2)
    try:
        with open(sys.argv[1]) as f:
            text = f.read()
    except OSError:
        print("Invalid puzzle")
        sys.exit(2)
    grid = _parse(text)
    if grid is None or not _valid(grid):
        print("Invalid puzzle")
        sys.exit(2)
    if not solve(grid):
        print("No solution")
        sys.exit(1)
    print('\n'.join(''.join(str(v) for v in row) for row in grid))


if __name__ == "__main__":
    main()
