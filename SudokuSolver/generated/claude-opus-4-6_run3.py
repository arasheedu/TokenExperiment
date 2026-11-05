import sys


def parse_puzzle(lines: list[str]) -> list[list[int]]:
    rows = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        row = []
        for ch in line:
            if ch == '.':
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
    for row in rows:
        if len(row) != 9:
            print("Invalid puzzle")
            sys.exit(2)
    return rows


def validate_puzzle(grid: list[list[int]]) -> bool:
    for i in range(9):
        for j in range(9):
            v = grid[i][j]
            if v < 0 or v > 9:
                return False
            if v == 0:
                continue
            # Check row
            for k in range(9):
                if k != j and grid[i][k] == v:
                    return False
            # Check column
            for k in range(9):
                if k != i and grid[k][j] == v:
                    return False
            # Check box
            bi, bj = 3 * (i // 3), 3 * (j // 3)
            for di in range(3):
                for dj in range(3):
                    ni, nj = bi + di, bj + dj
                    if (ni, nj) != (i, j) and grid[ni][nj] == v:
                        return False
    return True


def get_candidates(grid: list[list[int]], row: int, col: int) -> set[int]:
    used = set()
    for k in range(9):
        used.add(grid[row][k])
        used.add(grid[k][col])
    bi, bj = 3 * (row // 3), 3 * (col // 3)
    for di in range(3):
        for dj in range(3):
            used.add(grid[bi + di][bj + dj])
    return set(range(1, 10)) - used


def solve(grid: list[list[int]]) -> bool:
    best = None
    best_candidates = None
    min_count = 10

    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                cands = get_candidates(grid, i, j)
                if len(cands) == 0:
                    return False
                if len(cands) < min_count:
                    min_count = len(cands)
                    best = (i, j)
                    best_candidates = cands
                    if min_count == 1:
                        break
        if min_count == 1:
            break

    if best is None:
        return True

    row, col = best
    for val in best_candidates:
        grid[row][col] = val
        if solve(grid):
            return True
        grid[row][col] = 0

    return False


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} puzzle.txt")
        sys.exit(2)

    try:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Invalid puzzle")
        sys.exit(2)

    grid = parse_puzzle(lines)

    if not validate_puzzle(grid):
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
