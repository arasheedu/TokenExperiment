import sys

def solve(grid):
    rows=[0]*9;cols=[0]*9;boxes=[0]*9
    empty=[]
    for r in range(9):
        for c in range(9):
            v=grid[r][c]
            if v:
                b=(r//3)*3+c//3;m=1<<v
                if rows[r]&m or cols[c]&m or boxes[b]&m:return False
                rows[r]|=m;cols[c]|=m;boxes[b]|=m
            else:empty.append((r,c))
    def bt():
        if not empty:return True
        best=-1;bestmask=0;bestcount=10
        for i,(r,c) in enumerate(empty):
            b=(r//3)*3+c//3
            used=rows[r]|cols[c]|boxes[b]
            cnt=0
            for v in range(1,10):
                if not used&(1<<v):cnt+=1
            if cnt<bestcount:
                bestcount=cnt;best=i;bestmask=used
                if cnt<=1:break
        if bestcount==0:return False
        r,c=empty[best];b=(r//3)*3+c//3
        empty[best],empty[-1]=empty[-1],empty[best]
        empty.pop()
        for v in range(1,10):
            m=1<<v
            if not bestmask&m:
                grid[r][c]=v
                rows[r]|=m;cols[c]|=m;boxes[b]|=m
                if bt():return True
                rows[r]^=m;cols[c]^=m;boxes[b]^=m
        grid[r][c]=0
        empty.append((r,c))
        empty[best],empty[-1]=empty[-1],empty[best]
        return False
    return bt()

def main():
    try:
        with open(sys.argv[1]) as f:
            lines=[''.join(l.split()) for l in f if l.strip()]
    except:
        print("Invalid puzzle");sys.exit(2)
    if len(lines)!=9 or any(len(l)!=9 for l in lines):
        print("Invalid puzzle");sys.exit(2)
    grid=[]
    for l in lines:
        row=[]
        for ch in l:
            if ch in '0.':row.append(0)
            elif ch in '123456789':row.append(int(ch))
            else:print("Invalid puzzle");sys.exit(2)
        grid.append(row)
    if not solve(grid):
        # distinguish invalid initial vs no solution
        rows=[0]*9;cols=[0]*9;boxes=[0]*9
        for r in range(9):
            for c in range(9):
                v=grid[r][c]
                if v:
                    b=(r//3)*3+c//3;m=1<<v
                    if rows[r]&m or cols[c]&m or boxes[b]&m:
                        print("Invalid puzzle");sys.exit(2)
                    rows[r]|=m;cols[c]|=m;boxes[b]|=m
        print("No solution");sys.exit(1)
    print('\n'.join(''.join(str(v) for v in row) for row in grid))

if __name__=='__main__':main()
