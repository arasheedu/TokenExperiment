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
        row = [c for c in grid[i] if c != 0]
        if len(set(row)) != len(row):
            return False
        col = [grid[r][i] for r in range(9) if grid[r][i] != 0]
        if len(set(col)) != len(col):
            return False
    for br in range(3):
        for bc in range(3):
            box = []
            for r in range(br*3, br*3+3):
                for c in range(bc*3, bc*3+3):
                    if grid[r][c] != 0:
                        box.append(grid[r][c])
            if len(set(box)) != len(box):
                return False
    return True


def _candidates(grid, r, c):
    used = set(grid[r])
    used |= {grid[i][c] for i in range(9)}
    br, bc = (r // 3) * 3, (c // 3) * 3
    for i in range(br, br+3):
        for j in range(bc, bc+3):
            used.add(grid[i][j])
    return [d for d in range(1, 10) if d not in used]


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
    for d in best_cands:
        grid[r][c] = d
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
    print('\n'.join(''.join(str(d) for d in row) for row in grid))


if __name__ == '__main__':
    main()
