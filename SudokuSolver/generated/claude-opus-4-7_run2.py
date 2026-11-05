import sys


def _candidates(grid, r, c):
    used = set()
    for i in range(9):
        used.add(grid[r][i])
        used.add(grid[i][c])
    br, bc = (r // 3) * 3, (c // 3) * 3
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            used.add(grid[i][j])
    return [d for d in range(1, 10) if d not in used]


def _find_mrv(grid):
    best = None
    best_cands = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cands = _candidates(grid, r, c)
                if best is None or len(cands) < len(best_cands):
                    best = (r, c)
                    best_cands = cands
                    if len(cands) == 0:
                        return best, best_cands
    return best, best_cands


def solve(grid):
    cell, cands = _find_mrv(grid)
    if cell is None:
        return True
    if not cands:
        return False
    r, c = cell
    for d in cands:
        grid[r][c] = d
        if solve(grid):
            return True
    grid[r][c] = 0
    return False


def _validate(grid):
    for i in range(9):
        row_seen = set()
        col_seen = set()
        for j in range(9):
            v = grid[i][j]
            if v != 0:
                if v in row_seen:
                    return False
                row_seen.add(v)
            v = grid[j][i]
            if v != 0:
                if v in col_seen:
                    return False
                col_seen.add(v)
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            seen = set()
            for i in range(br, br + 3):
                for j in range(bc, bc + 3):
                    v = grid[i][j]
                    if v != 0:
                        if v in seen:
                            return False
                        seen.add(v)
    return True


def _parse(text):
    lines = []
    for raw in text.splitlines():
        stripped = "".join(raw.split())
        if stripped:
            lines.append(stripped)
    if len(lines) != 9:
        return None
    grid = []
    for line in lines:
        if len(line) != 9:
            return None
        row = []
        for ch in line:
            if ch in "0.":
                row.append(0)
            elif ch in "123456789":
                row.append(int(ch))
            else:
                return None
        grid.append(row)
    return grid


def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        sys.exit(2)
    try:
        with open(sys.argv[1], "r") as f:
            text = f.read()
    except OSError:
        print("Invalid puzzle")
        sys.exit(2)
    grid = _parse(text)
    if grid is None or not _validate(grid):
        print("Invalid puzzle")
        sys.exit(2)
    if not solve(grid):
        print("No solution")
        sys.exit(1)
    for row in grid:
        print("".join(str(d) for d in row))


if __name__ == "__main__":
    main()
