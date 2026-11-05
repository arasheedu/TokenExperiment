import sys

def solve(grid):
    rows=[0]*9;cols=[0]*9;boxes=[0]*9
    empties=[]
    for r in range(9):
        for c in range(9):
            v=grid[r][c]
            if v:
                b=1<<v
                if rows[r]&b or cols[c]&b or boxes[(r//3)*3+c//3]&b: return False
                rows[r]|=b;cols[c]|=b;boxes[(r//3)*3+c//3]|=b
            else:
                empties.append((r,c))
    def bt():
        if not empties: return True
        best=-1;bestm=0;bestcnt=10
        for i,(r,c) in enumerate(empties):
            m=~(rows[r]|cols[c]|boxes[(r//3)*3+c//3])&0x3FE
            cnt=bin(m).count('1')
            if cnt<bestcnt:
                bestcnt=cnt;best=i;bestm=m
                if cnt<=1: break
        if bestcnt==0: return False
        r,c=empties[best]
        empties[best],empties[-1]=empties[-1],empties[best]
        empties.pop()
        bi=(r//3)*3+c//3
        m=bestm
        while m:
            b=m&-m
            v=b.bit_length()-1
            rows[r]|=b;cols[c]|=b;boxes[bi]|=b
            grid[r][c]=v
            if bt(): return True
            rows[r]^=b;cols[c]^=b;boxes[bi]^=b
            m&=m-1
        grid[r][c]=0
        empties.append((r,c))
        empties[best],empties[-1]=empties[-1],empties[best]
        return False
    return bt()

def main():
    try:
        with open(sys.argv[1]) as f:
            lines=[''.join(ln.split()) for ln in f if ln.strip()]
    except:
        print("Invalid puzzle");sys.exit(2)
    if len(lines)!=9 or any(len(l)!=9 for l in lines):
        print("Invalid puzzle");sys.exit(2)
    grid=[]
    for l in lines:
        row=[]
        for ch in l:
            if ch in '0.': row.append(0)
            elif ch in '123456789': row.append(int(ch))
            else: print("Invalid puzzle");sys.exit(2)
        grid.append(row)
    if not solve(grid):
        if any(grid[r][c]==0 for r in range(9) for c in range(9)) or not all(grid[r][c] for r in range(9) for c in range(9)):
            pass
        # Determine if invalid vs no solution: re-check initial
        print("No solution");sys.exit(1)
    print('\n'.join(''.join(str(v) for v in row) for row in grid))

if __name__=="__main__":
    main()
