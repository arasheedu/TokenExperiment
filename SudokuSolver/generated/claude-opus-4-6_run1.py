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
            br, bc = 3 * (i // 3), 3 * (j // 3)
            for r in range(br, br + 3):
                for c in range(bc, bc + 3):
                    if (r, c) != (i, j) and grid[r][c] == v:
                        return False
    return True


def solve(grid: list[list[int]]) -> bool:
    # Build candidate sets for each cell
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for i in range(9):
        for j in range(9):
            v = grid[i][j]
            if v != 0:
                rows[i].add(v)
                cols[j].add(v)
                boxes[3 * (i // 3) + j // 3].add(v)

    empty = []
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                empty.append((i, j))

    def backtrack(idx: int) -> bool:
        if idx == len(empty):
            return True

        # MRV: pick the empty cell (from idx onward) with fewest candidates
        best = idx
        best_count = 10
        for k in range(idx, len(empty)):
            i, j = empty[k]
            b = 3 * (i // 3) + j // 3
            count = 9 - len(rows[i] | cols[j] | boxes[b])
            if count < best_count:
                best_count = count
                best = k
                if count == 0:
                    return False
                if count == 1:
                    break

        # Swap best to current position
        empty[idx], empty[best] = empty[best], empty[idx]

        i, j = empty[idx]
        b = 3 * (i // 3) + j // 3
        used = rows[i] | cols[j] | boxes[b]

        for v in range(1, 10):
            if v in used:
                continue
            grid[i][j] = v
            rows[i].add(v)
            cols[j].add(v)
            boxes[b].add(v)

            if backtrack(idx + 1):
                return True

            grid[i][j] = 0
            rows[i].discard(v)
            cols[j].discard(v)
            boxes[b].discard(v)

        # Undo swap
        empty[idx], empty[best] = empty[best], empty[idx]
        return False

    return backtrack(0)


def main():
    if len(sys.argv) != 2:
        print("Usage: python sudoku.py puzzle.txt", file=sys.stderr)
        sys.exit(2)

    try:
        with open(sys.argv[1], 'r') as f:
            text = f.read()
    except IOError as e:
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
            print(''.join(str(c) for c in row))
    else:
        print("No solution")
        sys.exit(1)


if __name__ == '__main__':
    main()
