import sys

def solve(grid):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                b = (r // 3) * 3 + c // 3
                if v in rows[r] or v in cols[c] or v in boxes[b]:
                    return False
                rows[r].add(v)
                cols[c].add(v)
                boxes[b].add(v)

    def bt():
        best, best_cands, best_pos = 10, None, None
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    b = (r // 3) * 3 + c // 3
                    cands = {1,2,3,4,5,6,7,8,9} - rows[r] - cols[c] - boxes[b]
                    if not cands:
                        return False
                    if len(cands) < best:
                        best, best_cands, best_pos = len(cands), cands, (r, c)
        if best_pos is None:
            return True
        r, c = best_pos
        b = (r // 3) * 3 + c // 3
        for v in best_cands:
            grid[r][c] = v
            rows[r].add(v)
            cols[c].add(v)
            boxes[b].add(v)
            if bt():
                return True
            grid[r][c] = 0
            rows[r].discard(v)
            cols[c].discard(v)
            boxes[b].discard(v)
        return False

    return bt()

def main():
    try:
        with open(sys.argv[1]) as f:
            lines = [l.strip() for l in f if l.strip()]
    except (IndexError, FileNotFoundError):
        print("Invalid puzzle")
        sys.exit(2)
    if len(lines) != 9:
        print("Invalid puzzle")
        sys.exit(2)
    grid = []
    for line in lines:
        if len(line) != 9:
            print("Invalid puzzle")
            sys.exit(2)
        row = []
        for ch in line:
            if ch in '0.':
                row.append(0)
            elif ch in '123456789':
                row.append(int(ch))
            else:
                print("Invalid puzzle")
                sys.exit(2)
        grid.append(row)
    # Check for conflicts in initial grid
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                for c2 in range(9):
                    if c2 != c and grid[r][c2] == v:
                        print("Invalid puzzle")
                        sys.exit(2)
                for r2 in range(9):
                    if r2 != r and grid[r2][c] == v:
                        print("Invalid puzzle")
                        sys.exit(2)
                br, bc = (r // 3) * 3, (c // 3) * 3
                for dr in range(3):
                    for dc in range(3):
                        r2, c2 = br + dr, bc + dc
                        if (r2, c2) != (r, c) and grid[r2][c2] == v:
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
