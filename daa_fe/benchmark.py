import csv
import time
from typing import List, Tuple

from maze_generator import generate_maze, get_start_goal
from bfs import bfs
from astar import astar

# ── Benchmark configuration ──────────────────────────────────────────────────
# Logical side lengths n; actual grid = (2n+1)×(2n+1), V ≈ n²
SIZES  = [10, 25, 50, 100, 250, 500, 750, 1000]   # ≥ 5 sizes, ≥ 2 orders of magnitude
TRIALS = 5                                          # averaged over 5 runs
BASE_SEED = 42                                      # seeds = BASE_SEED + trial_index
OUTPUT_CSV = "results.csv"
# ─────────────────────────────────────────────────────────────────────────────


def bench_once(size: int, seed: int) -> dict:
    """Run both algorithms on one maze and return timing / stats."""
    grid = generate_maze(size, size, seed=seed)
    start, goal = get_start_goal(grid)

    # BFS
    t0 = time.perf_counter()
    bfs_path, bfs_vis = bfs(grid, start, goal)
    bfs_ms = (time.perf_counter() - t0) * 1000

    # A*
    t0 = time.perf_counter()
    as_path, as_vis = astar(grid, start, goal)
    as_ms = (time.perf_counter() - t0) * 1000

    H = len(grid)
    W = len(grid[0])
    n_vertices = sum(grid[r][c] == 0 for r in range(H) for c in range(W))

    return {
        "size": size,
        "n_vertices": n_vertices,
        "bfs_ms": bfs_ms,
        "astar_ms": as_ms,
        "bfs_visited": bfs_vis,
        "astar_visited": as_vis,
        "bfs_path": len(bfs_path) if bfs_path else -1,
        "astar_path": len(as_path) if as_path else -1,
    }


def run_benchmark() -> List[dict]:
    """Run full benchmark sweep and return averaged rows."""
    print(f"{'Size':>6} {'Vertices':>10} {'BFS (ms)':>10} {'A* (ms)':>10}"
          f" {'BFS vis':>10} {'A* vis':>10} {'Match?':>7}")
    print("-" * 70)

    rows = []
    for size in SIZES:
        trials_data = [bench_once(size, BASE_SEED + i) for i in range(TRIALS)]

        avg = {
            "size": size,
            "n_vertices": trials_data[0]["n_vertices"],
            "bfs_ms":       sum(d["bfs_ms"]       for d in trials_data) / TRIALS,
            "astar_ms":     sum(d["astar_ms"]      for d in trials_data) / TRIALS,
            "bfs_visited":  sum(d["bfs_visited"]   for d in trials_data) / TRIALS,
            "astar_visited":sum(d["astar_visited"] for d in trials_data) / TRIALS,
            "bfs_path":     trials_data[0]["bfs_path"],
            "astar_path":   trials_data[0]["astar_path"],
        }

        match = "✓" if avg["bfs_path"] == avg["astar_path"] else "✗"
        print(f"{size:>6} {avg['n_vertices']:>10} {avg['bfs_ms']:>10.3f}"
              f" {avg['astar_ms']:>10.3f} {avg['bfs_visited']:>10.0f}"
              f" {avg['astar_visited']:>10.0f} {match:>7}")

        rows.append(avg)

    return rows


def save_csv(rows: List[dict], path: str = OUTPUT_CSV) -> None:
    fieldnames = ["size", "n_vertices", "bfs_ms", "astar_ms",
                  "bfs_visited", "astar_visited", "bfs_path", "astar_path"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nResults saved to {path}")


if __name__ == "__main__":
    print("MazePath Benchmark — BFS vs A*")
    print(f"Sizes  : {SIZES}")
    print(f"Trials : {TRIALS}  (seeds {BASE_SEED}–{BASE_SEED + TRIALS - 1})\n")

    rows = run_benchmark()
    save_csv(rows)

    # Cross-check summary
    mismatches = [r for r in rows if r["bfs_path"] != r["astar_path"]]
    if mismatches:
        print(f"\n⚠ PATH LENGTH MISMATCH at sizes: {[r['size'] for r in mismatches]}")
    else:
        print("\n✓ All sizes: BFS and A* returned identical path lengths.")

    print("\nRun `python plot_results.py` to generate benchmark_plot.png")
