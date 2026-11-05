import sys

def solve(grid):
    rows = [0]*9
    cols = [0]*9
    boxes = [0]*9
    empties = []
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                bit = 1 << v
                b = (r//3)*3 + c//3
                if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                    return False
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit
            else:
                empties.append((r, c))

    def backtrack():
        if not empties:
            return True
        best_idx = -1
        best_cands = None
        best_count = 10
        for i, (r, c) in enumerate(empties):
            b = (r//3)*3 + c//3
            used = rows[r] | cols[c] | boxes[b]
            cands = [v for v in range(1, 10) if not used & (1 << v)]
            if len(cands) < best_count:
                best_count = len(cands)
                best_cands = cands
                best_idx = i
                if best_count == 0:
                    break
        r, c = empties[best_idx]
        b = (r//3)*3 + c//3
        empties[best_idx], empties[-1] = empties[-1], empties[best_idx]
        empties.pop()
        for v in best_cands:
            bit = 1 << v
            grid[r][c] = v
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            if backtrack():
                return True
            grid[r][c] = 0
            rows[r] &= ~bit
            cols[c] &= ~bit
            boxes[b] &= ~bit
        empties.append((r, c))
        empties[best_idx], empties[-1] = empties[-1], empties[best_idx]
        return False

    return backtrack()


def main():
    if len(sys.argv) != 2:
        print("Invalid puzzle")
        sys.exit(2)
    try:
        with open(sys.argv[1]) as f:
            lines = [line.strip() for line in f if line.strip()]
    except OSError:
        print("Invalid puzzle")
        sys.exit(2)

    if len(lines) != 9 or any(len(line) != 9 for line in lines):
        print("Invalid puzzle")
        sys.exit(2)

    grid = []
    for line in lines:
        row = []
        for ch in line:
            if ch == '.' or ch == '0':
                row.append(0)
            elif ch in '123456789':
                row.append(int(ch))
            else:
                print("Invalid puzzle")
                sys.exit(2)
        grid.append(row)

    if not solve(grid):
        print("No solution")
        sys.exit(1)

    for row in grid:
        print(''.join(map(str, row)))


if __name__ == '__main__':
    main()
