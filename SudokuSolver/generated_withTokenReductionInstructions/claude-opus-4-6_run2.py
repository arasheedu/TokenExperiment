import sys

def solve(grid):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty = []
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
            else:
                empty.append((r, c))

    def bt(idx):
        if idx == len(empty):
            return True
        best, best_cands, best_i = None, None, idx
        min_count = 10
        for i in range(idx, len(empty)):
            r, c = empty[i]
            b = (r // 3) * 3 + c // 3
            cands = {1,2,3,4,5,6,7,8,9} - rows[r] - cols[c] - boxes[b]
            if not cands:
                return False
            if len(cands) < min_count:
                min_count = len(cands)
                best, best_cands, best_i = (r, c), cands, i
                if min_count == 1:
                    break
        empty[idx], empty[best_i] = empty[best_i], empty[idx]
        r, c = best
        b = (r // 3) * 3 + c // 3
        for v in best_cands:
            grid[r][c] = v
            rows[r].add(v)
            cols[c].add(v)
            boxes[b].add(v)
            if bt(idx + 1):
                return True
            rows[r].discard(v)
            cols[c].discard(v)
            boxes[b].discard(v)
        grid[r][c] = 0
        empty[idx], empty[best_i] = empty[best_i], empty[idx]
        return False

    return bt(0)

def main():
    try:
        with open(sys.argv[1]) as f:
            lines = [l.strip() for l in f if l.strip()]
    except Exception:
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
            if ch == '.':
                row.append(0)
            elif ch.isdigit():
                row.append(int(ch))
            else:
                print("Invalid puzzle")
                sys.exit(2)
        grid.append(row)
    # Check for conflicts in given clues
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
