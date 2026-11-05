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
                rows[r] |= bit
                cols[c] |= bit
                boxes[(r//3)*3 + c//3] |= bit
            else:
                empties.append((r, c))

    def candidates(r, c):
        used = rows[r] | cols[c] | boxes[(r//3)*3 + c//3]
        return [d for d in range(1, 10) if not used & (1 << d)]

    def backtrack():
        if not empties:
            return True
        best = None
        bestcands = None
        for idx, (r, c) in enumerate(empties):
            cands = candidates(r, c)
            if not cands:
                return False
            if bestcands is None or len(cands) < len(bestcands):
                best, bestcands = idx, cands
                if len(cands) == 1:
                    break
        r, c = empties.pop(best)
        b = (r//3)*3 + c//3
        for d in bestcands:
            bit = 1 << d
            grid[r][c] = d
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            if backtrack():
                return True
            grid[r][c] = 0
            rows[r] &= ~bit
            cols[c] &= ~bit
            boxes[b] &= ~bit
        empties.insert(best, (r, c))
        return False

    return backtrack()

def main():
    if len(sys.argv) != 2:
        print("Invalid puzzle")
        sys.exit(2)
    try:
        with open(sys.argv[1]) as f:
            lines = [l.strip() for l in f if l.strip() != '']
    except OSError:
        print("Invalid puzzle")
        sys.exit(2)
    if len(lines) != 9:
        print("Invalid puzzle")
        sys.exit(2)
    valid_chars = set('0123456789.')
    grid = []
    for line in lines:
        line = ''.join(line.split())
        if len(line) != 9:
            print("Invalid puzzle")
            sys.exit(2)
        row = []
        for ch in line:
            if ch not in valid_chars:
                print("Invalid puzzle")
                sys.exit(2)
            row.append(0 if ch in '0.' else int(ch))
        grid.append(row)

    rows = [0]*9
    cols = [0]*9
    boxes = [0]*9
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                bit = 1 << v
                b = (r//3)*3 + c//3
                if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                    print("Invalid puzzle")
                    sys.exit(2)
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit

    if not solve(grid):
        print("No solution")
        sys.exit(1)

    for row in grid:
        print(''.join(map(str, row)))

if __name__ == '__main__':
    main()
