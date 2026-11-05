import sys

def solve(grid: list[list[int]]) -> bool:
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                rows[r].add(v)
                cols[c].add(v)
                boxes[(r // 3) * 3 + c // 3].add(v)

    def backtrack():
        best, best_cands = None, None
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    b = (r // 3) * 3 + c // 3
                    cands = {1,2,3,4,5,6,7,8,9} - rows[r] - cols[c] - boxes[b]
                    if not cands:
                        return False
                    if best is None or len(cands) < len(best_cands):
                        best, best_cands = (r, c, b), cands
                        if len(cands) == 1:
                            break
            else:
                continue
            break
        if best is None:
            return True
        r, c, b = best
        for v in best_cands:
            grid[r][c] = v
            rows[r].add(v)
            cols[c].add(v)
            boxes[b].add(v)
            if backtrack():
                return True
            grid[r][c] = 0
            rows[r].remove(v)
            cols[c].remove(v)
            boxes[b].remove(v)
        return False

    return backtrack()

def main():
    if len(sys.argv) != 2:
        print("Invalid puzzle")
        sys.exit(2)
    try:
        with open(sys.argv[1]) as f:
            lines = [l.strip() for l in f if l.strip()]
    except:
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
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                b = (r // 3) * 3 + c // 3
                if v in rows[r] or v in cols[c] or v in boxes[b]:
                    print("Invalid puzzle")
                    sys.exit(2)
                rows[r].add(v)
                cols[c].add(v)
                boxes[b].add(v)
    if solve(grid):
        for row in grid:
            print(''.join(map(str, row)))
    else:
        print("No solution")
        sys.exit(1)

if __name__ == "__main__":
    main()
