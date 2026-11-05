import sys

def parse(path):
    try:
        with open(path) as f:
            content = f.read()
    except OSError:
        print("Invalid puzzle")
        sys.exit(2)

    rows = []
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if len(line) != 9:
            print("Invalid puzzle")
            sys.exit(2)
        row = []
        for ch in line:
            if ch in '0.':
                row.append(0)
            elif ch.isdigit():
                row.append(int(ch))
            else:
                print("Invalid puzzle")
                sys.exit(2)
        rows.append(row)

    if len(rows) != 9:
        print("Invalid puzzle")
        sys.exit(2)

    return rows


def is_valid_clues(grid):
    # Check rows
    for r in range(9):
        seen = set()
        for c in range(9):
            v = grid[r][c]
            if v == 0:
                continue
            if v in seen:
                return False
            seen.add(v)
    # Check cols
    for c in range(9):
        seen = set()
        for r in range(9):
            v = grid[r][c]
            if v == 0:
                continue
            if v in seen:
                return False
            seen.add(v)
    # Check boxes
    for br in range(3):
        for bc in range(3):
            seen = set()
            for r in range(br*3, br*3+3):
                for c in range(bc*3, bc*3+3):
                    v = grid[r][c]
                    if v == 0:
                        continue
                    if v in seen:
                        return False
                    seen.add(v)
    return True


def get_candidates(grid, rows_used, cols_used, boxes_used, r, c):
    box = (r // 3) * 3 + (c // 3)
    used = rows_used[r] | cols_used[c] | boxes_used[box]
    candidates = []
    for d in range(1, 10):
        if not (used >> d & 1):
            candidates.append(d)
    return candidates


def solve(grid: list[list[int]]) -> bool:
    # Build bitmask sets for rows, cols, boxes
    rows_used = [0] * 9
    cols_used = [0] * 9
    boxes_used = [0] * 9

    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v != 0:
                box = (r // 3) * 3 + (c // 3)
                rows_used[r] |= (1 << v)
                cols_used[c] |= (1 << v)
                boxes_used[box] |= (1 << v)

    return _backtrack(grid, rows_used, cols_used, boxes_used)


def _backtrack(grid, rows_used, cols_used, boxes_used):
    # Find empty cell with MRV
    best_r, best_c, best_candidates = -1, -1, None

    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                candidates = get_candidates(grid, rows_used, cols_used, boxes_used, r, c)
                if not candidates:
                    return False
                if best_candidates is None or len(candidates) < len(best_candidates):
                    best_r, best_c, best_candidates = r, c, candidates
                    if len(candidates) == 1:
                        break
        if best_candidates is not None and len(best_candidates) == 1:
            break

    if best_r == -1:
        # No empty cells
        return True

    box = (best_r // 3) * 3 + (best_c // 3)

    for d in best_candidates:
        bit = 1 << d
        grid[best_r][best_c] = d
        rows_used[best_r] |= bit
        cols_used[best_c] |= bit
        boxes_used[box] |= bit

        if _backtrack(grid, rows_used, cols_used, boxes_used):
            return True

        grid[best_r][best_c] = 0
        rows_used[best_r] &= ~bit
        cols_used[best_c] &= ~bit
        boxes_used[box] &= ~bit

    return False


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python sudoku.py puzzle.txt")
        sys.exit(2)

    grid = parse(sys.argv[1])

    if not is_valid_clues(grid):
        print("Invalid puzzle")
        sys.exit(2)

    if solve(grid):
        for row in grid:
            print(''.join(map(str, row)))
    else:
        print("No solution")
        sys.exit(1)


if __name__ == '__main__':
    main()
