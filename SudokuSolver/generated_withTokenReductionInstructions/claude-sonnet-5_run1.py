import sys

def solve(grid):
    rows = [0]*9
    cols = [0]*9
    boxes = [0]*9
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                bit = 1 << (v-1)
                b = (r//3)*3 + c//3
                if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                    return False
                rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit

    def backtrack():
        best = None
        best_cands = 0
        best_count = 10
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    b = (r//3)*3 + c//3
                    cands = ~(rows[r] | cols[c] | boxes[b]) & 0x1FF
                    cnt = bin(cands).count('1')
                    if cnt < best_count:
                        best_count = cnt
                        best = (r, c)
                        best_cands = cands
                        if cnt == 0:
                            return False
        if best is None:
            return True
        r, c = best
        b = (r//3)*3 + c//3
        cands = best_cands
        while cands:
            bit = cands & -cands
            cands ^= bit
            v = bit.bit_length()
            grid[r][c] = v
            rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
            if backtrack():
                return True
            rows[r] ^= bit; cols[c] ^= bit; boxes[b] ^= bit
            grid[r][c] = 0
        return False

    return backtrack()

def main():
    if len(sys.argv) != 2:
        print("Invalid puzzle")
        sys.exit(2)
    try:
        with open(sys.argv[1]) as f:
            raw_lines = f.readlines()
    except OSError:
        print("Invalid puzzle")
        sys.exit(2)

    lines = [l.strip() for l in raw_lines]
    lines = [l for l in lines if l]
    if len(lines) != 9:
        print("Invalid puzzle")
        sys.exit(2)

    valid_chars = set("0.123456789")
    grid = []
    for line in lines:
        if len(line) != 9 or any(ch not in valid_chars for ch in line):
            print("Invalid puzzle")
            sys.exit(2)
        row = [0 if ch in "0." else int(ch) for ch in line]
        grid.append(row)

    rows = [0]*9
    cols = [0]*9
    boxes = [0]*9
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                bit = 1 << (v-1)
                b = (r//3)*3 + c//3
                if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                    print("Invalid puzzle")
                    sys.exit(2)
                rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit

    if not solve(grid):
        print("No solution")
        sys.exit(1)

    for row in grid:
        print(''.join(str(v) for v in row))

if __name__ == "__main__":
    main()
