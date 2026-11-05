import sys

def solve(grid):
    best, best_pos = None, None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                used = set()
                for i in range(9):
                    used.add(grid[r][i])
                    used.add(grid[i][c])
                br, bc = (r//3)*3, (c//3)*3
                for dr in range(3):
                    for dc in range(3):
                        used.add(grid[br+dr][bc+dc])
                cands = [d for d in range(1,10) if d not in used]
                if not cands:
                    return False
                if best is None or len(cands) < len(best):
                    best, best_pos = cands, (r, c)
    if best_pos is None:
        return True
    r, c = best_pos
    for d in best:
        grid[r][c] = d
        if solve(grid):
            return True
        grid[r][c] = 0
    return False

def main():
    if len(sys.argv) != 2:
        print("Invalid puzzle"); sys.exit(2)
    try:
        with open(sys.argv[1]) as f:
            raw = f.read()
    except OSError:
        print("Invalid puzzle"); sys.exit(2)
    lines = [l for l in raw.splitlines() if l.strip()]
    rows = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(line) != 9:
            print("Invalid puzzle"); sys.exit(2)
        row = []
        for ch in line:
            if ch in '123456789':
                row.append(int(ch))
            elif ch in '0.':
                row.append(0)
            else:
                print("Invalid puzzle"); sys.exit(2)
        rows.append(row)
    if len(rows) != 9:
        print("Invalid puzzle"); sys.exit(2)
    for r in range(9):
        for c in range(9):
            d = rows[r][c]
            if d == 0:
                continue
            for i in range(9):
                if i != c and rows[r][i] == d:
                    print("Invalid puzzle"); sys.exit(2)
                if i != r and rows[i][c] == d:
                    print("Invalid puzzle"); sys.exit(2)
            br, bc = (r//3)*3, (c//3)*3
            for dr in range(3):
                for dc in range(3):
                    nr, nc = br+dr, bc+dc
                    if (nr, nc) != (r, c) and rows[nr][nc] == d:
                        print("Invalid puzzle"); sys.exit(2)
    if not solve(rows):
        print("No solution"); sys.exit(1)
    for row in rows:
        print(''.join(map(str, row)))

if __name__ == '__main__':
    main()
