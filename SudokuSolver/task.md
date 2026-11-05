Write a complete Sudoku solver in Python 3.

## Requirements

- Single file, `sudoku.py`, using only the Python standard library.
- Usage: `python sudoku.py puzzle.txt`
- Input file format: 9 lines of 9 characters each. Digits `1`-`9` are given clues; `0` or `.` marks an empty cell. Ignore blank lines and whitespace.
- Solve with backtracking search. Before recursing, pick the empty cell with the fewest legal candidates (MRV heuristic).
- Output: print the solved grid as 9 lines of 9 digits with no separators.
- If the puzzle has no solution, print `No solution` and exit with status 1.
- If the input is malformed (wrong dimensions, invalid characters, or clues that already conflict), print `Invalid puzzle` and exit with status 2.
- Include a `solve(grid: list[list[int]]) -> bool` function that solves the grid in place and returns True on success, so the solver can be imported and tested.


## Test puzzle

The program must solve this puzzle:

```
530070000
600195000
098000060
800060003
400803001
700020006
060000280
000419005
000080079
```

Expected output:

```
534678912
672195348
198342567
859761423
426853791
713924856
961537284
287419635
345286179
```

## Response format

Return only the contents of `sudoku.py` in a single Python code block. No explanation before or after the code.
