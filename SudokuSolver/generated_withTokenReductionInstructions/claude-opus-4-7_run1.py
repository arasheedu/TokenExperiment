import sys

def solve(grid):
    rows=[0]*9;cols=[0]*9;boxes=[0]*9
    empties=[]
    for r in range(9):
        for c in range(9):
            v=grid[r][c]
            if v:
                b=1<<v
                if rows[r]&b or cols[c]&b or boxes[(r//3)*3+c//3]&b:return False
                rows[r]|=b;cols[c]|=b;boxes[(r//3)*3+c//3]|=b
            else:
                empties.append((r,c))
    def bt():
        if not empties:return True
        best=-1;bestmask=0;bestcount=10
        for i,(r,c) in enumerate(empties):
            used=rows[r]|cols[c]|boxes[(r//3)*3+c//3]
            m=(~used)&0x3FE
            cnt=bin(m).count('1')
            if cnt<bestcount:
                bestcount=cnt;best=i;bestmask=m
                if cnt<=1:break
        if bestcount==0:return False
        r,c=empties.pop(best)
        bi=(r//3)*3+c//3
        m=bestmask
        while m:
            b=m&-m
            v=b.bit_length()-1
            rows[r]|=b;cols[c]|=b;boxes[bi]|=b;grid[r][c]=v
            if bt():return True
            rows[r]^=b;cols[c]^=b;boxes[bi]^=b
            m&=m-1
        grid[r][c]=0
        empties.insert(best,(r,c))
        return False
    return bt()

def main():
    if len(sys.argv)!=2:print("Invalid puzzle");sys.exit(2)
    try:
        with open(sys.argv[1]) as f:data=f.read()
    except OSError:print("Invalid puzzle");sys.exit(2)
    lines=[l.strip() for l in data.splitlines() if l.strip()]
    if len(lines)!=9:print("Invalid puzzle");sys.exit(2)
    grid=[]
    for l in lines:
        l="".join(l.split())
        if len(l)!=9:print("Invalid puzzle");sys.exit(2)
        row=[]
        for ch in l:
            if ch in "0.":row.append(0)
            elif ch in "123456789":row.append(int(ch))
            else:print("Invalid puzzle");sys.exit(2)
        grid.append(row)
    if not solve(grid):
        seen=set()
        for r in range(9):
            for c in range(9):
                v=grid[r][c]
                if v:
                    for k in (('r',r,v),('c',c,v),('b',(r//3)*3+c//3,v)):
                        if k in seen:print("Invalid puzzle");sys.exit(2)
                        seen.add(k)
        print("No solution");sys.exit(1)
    print("\n".join("".join(str(v) for v in row) for row in grid))

if __name__=="__main__":main()
