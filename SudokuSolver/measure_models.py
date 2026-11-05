#!/usr/bin/env python3
"""Measure how many tokens each Claude model uses to generate the program in task.md.

For every model returned by the Models API this script:
  1. sends task.md as the prompt (RUNS times),
  2. records input/output/cache tokens, wall time, stop reason,
  3. extracts the generated code, runs it against the test puzzle in task.md,
     and records whether the output was correct,
  4. appends one row per run to results.csv.

Visualise the CSV afterwards with plot_results.py.

Usage:
    pip install anthropic
    export ANTHROPIC_API_KEY=...
    python measure_models.py [--runs 3] [--task task.md] [--only sonnet,haiku]
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import anthropic

CSV_PATH = Path("results.csv")
CODE_DIR = Path("generated")
MAX_TOKENS = 8000

CSV_FIELDS = [
    "timestamp", "model", "run", "input_tokens", "output_tokens",
    "cache_creation_input_tokens", "cache_read_input_tokens",
    "stop_reason", "wall_seconds", "code_lines", "correct", "error",
]

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

def extract_puzzle_and_answer(task_text: str) -> tuple[str, str]:
    """Pull the two 9x9 grids (puzzle, expected solution) out of task.md."""
    grids = re.findall(r"```\n((?:[0-9.]{9}\n){9})```", task_text)
    if len(grids) < 2:
        sys.exit("task.md must contain a test puzzle and an expected output block")
    return grids[0], grids[1]


def extract_code(text: str) -> str:
    """Return the first fenced code block, or the whole text if there is none."""
    m = re.search(r"```(?:python)?\n(.*?)```", text, re.S)
    return (m.group(1) if m else text).strip() + "\n"


def check_solution(code: str, puzzle: str, expected: str) -> tuple[bool, str]:
    """Run the generated solver on the puzzle; return (correct, error_message)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "sudoku.py").write_text(code)
        (tmp / "puzzle.txt").write_text(puzzle)
        try:
            proc = subprocess.run(
                [sys.executable, "-I", "sudoku.py", "puzzle.txt"],
                cwd=tmp, capture_output=True, text=True, timeout=60,
            )
        except subprocess.TimeoutExpired:
            return False, "timeout"
        if proc.returncode != 0:
            return False, (proc.stderr.strip().splitlines() or ["nonzero exit"])[-1][:200]
        got = "\n".join(l.strip() for l in proc.stdout.strip().splitlines())
        return got == expected.strip(), "" if got == expected.strip() else "wrong output"


def list_models(client: anthropic.Anthropic, only: list[str] | None) -> list[str]:
    ids = [m.id for m in client.models.list(limit=100)]
    if only:
        ids = [i for i in ids if any(o in i for o in only)]
    return sorted(ids)


# ----------------------------------------------------------------------------
# Measurement
# ----------------------------------------------------------------------------

def run_one(client, model: str, prompt: str, puzzle: str, expected: str, run: int) -> dict:
    row = {"timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "model": model, "run": run}
    t0 = time.time()
    try:
        msg = client.messages.create(
            model=model, max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.APIError as e:
        row.update(wall_seconds=round(time.time() - t0, 2), correct=False,
                   error=f"API error: {type(e).__name__}: {str(e)[:150]}")
        return row
    row["wall_seconds"] = round(time.time() - t0, 2)

    u = msg.usage
    row.update(
        input_tokens=u.input_tokens,
        output_tokens=u.output_tokens,
        cache_creation_input_tokens=getattr(u, "cache_creation_input_tokens", 0) or 0,
        cache_read_input_tokens=getattr(u, "cache_read_input_tokens", 0) or 0,
        stop_reason=msg.stop_reason,
    )

    text = "".join(b.text for b in msg.content if b.type == "text")
    code = extract_code(text)
    CODE_DIR.mkdir(exist_ok=True)
    (CODE_DIR / f"{model}_run{run}.py").write_text(code)
    row["code_lines"] = code.count("\n")
    row["correct"], row["error"] = check_solution(code, puzzle, expected)
    return row


def append_rows(rows: list[dict]) -> None:
    new_file = not CSV_PATH.exists()
    with CSV_PATH.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if new_file:
            w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in CSV_FIELDS})


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--runs", type=int, default=3, help="runs per model (default 3)")
    ap.add_argument("--task", default="task.md", help="prompt file (default task.md)")
    ap.add_argument("--only", help="comma-separated substrings to filter model ids")
    args = ap.parse_args()

    prompt = Path(args.task).read_text()
    puzzle, expected = extract_puzzle_and_answer(prompt)
    client = anthropic.Anthropic()
    models = list_models(client, args.only.split(",") if args.only else None)
    print(f"{len(models)} models: {', '.join(models)}\n")

    for model in models:
        for run in range(1, args.runs + 1):
            row = run_one(client, model, prompt, puzzle, expected, run)
            append_rows([row])
            status = "OK " if row.get("correct") else "FAIL"
            print(f"{status} {model:40s} run {run}: "
                    f"in={row.get('input_tokens', '-'):>5} "
                    f"out={row.get('output_tokens', '-'):>5} "
                    f"{row['wall_seconds']:6.1f}s  {row.get('error', '')}")

    print(f"\nresults appended to {CSV_PATH}; run: python plot_results.py {CSV_PATH}")


if __name__ == "__main__":
    main()
