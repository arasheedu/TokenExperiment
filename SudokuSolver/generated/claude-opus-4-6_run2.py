import sys


def parse_puzzle(text: str) -> list[list[int]]:
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        lines.append(line)
    if len(lines) != 9:
        raise ValueError("Invalid puzzle")
    grid = []
    for line in lines:
        if len(line) != 9:
            raise ValueError("Invalid puzzle")
        row = []
        for ch in line:
            if ch == '.':
                row.append(0)
            elif ch.isdigit() and '0' <= ch <= '9':
                row.append(int(ch))
            else:
                raise ValueError("Invalid puzzle")
        grid.append(row)
    return grid


def validate_grid(grid: list[list[int]]) -> bool:
    for i in range(9):
        for j in range(9):
            val = grid[i][j]
            if val < 0 or val > 9:
                return False
            if val == 0:
                continue
            # Check row
            for k in range(9):
                if k != j and grid[i][k] == val:
                    return False
            # Check column
            for k in range(9):
                if k != i and grid[k][j] == val:
                    return False
            # Check box
            bi, bj = 3 * (i // 3), 3 * (j // 3)
            for di in range(3):
                for dj in range(3):
                    ni, nj = bi + di, bj + dj
                    if (ni, nj) != (i, j) and grid[ni][nj] == val:
                        return False
    return True


def solve(grid: list[list[int]]) -> bool:
    # Build candidate sets for each cell
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for i in range(9):
        for j in range(9):
            val = grid[i][j]
            if val != 0:
                rows[i].add(val)
                cols[j].add(val)
                boxes[3 * (i // 3) + j // 3].add(val)

    empty_cells = []
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                empty_cells.append((i, j))

    def get_candidates(r: int, c: int) -> set[int]:
        return {1,2,3,4,5,6,7,8,9} - rows[r] - cols[c] - boxes[3*(r//3) + c//3]

    def backtrack(idx: int) -> bool:
        if idx == len(empty_cells):
            return True

        # MRV: pick the cell among remaining with fewest candidates
        min_count = 10
        min_pos = idx
        for k in range(idx, len(empty_cells)):
            r, c = empty_cells[k]
            count = len(get_candidates(r, c))
            if count == 0:
                return False
            if count < min_count:
                min_count = count
                min_pos = k
                if count == 1:
                    break

        # Swap to current position
        empty_cells[idx], empty_cells[min_pos] = empty_cells[min_pos], empty_cells[idx]

        r, c = empty_cells[idx]
        b = 3 * (r // 3) + c // 3
        candidates = get_candidates(r, c)

        for val in candidates:
            grid[r][c] = val
            rows[r].add(val)
            cols[c].add(val)
            boxes[b].add(val)

            if backtrack(idx + 1):
                return True

            grid[r][c] = 0
            rows[r].discard(val)
            cols[c].discard(val)
            boxes[b].discard(val)

        # Swap back
        empty_cells[idx], empty_cells[min_pos] = empty_cells[min_pos], empty_cells[idx]
        return False

    return backtrack(0)


def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        sys.exit(2)

    try:
        with open(sys.argv[1], 'r') as f:
            text = f.read()
    except (IOError, OSError) as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(2)

    try:
        grid = parse_puzzle(text)
    except ValueError:
        print("Invalid puzzle")
        sys.exit(2)

    if not validate_grid(grid):
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
