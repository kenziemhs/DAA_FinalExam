import argparse
import time

from maze_generator import generate_maze, get_start_goal, print_maze
from bfs import bfs
from astar import astar


def run_demo(size: int = 15, seed: int = 42, plot: bool = True) -> None:
    print("=" * 60)
    print(f"  MazePath Demo  —  size={size}x{size}  seed={seed}")
    print("=" * 60)

    grid = generate_maze(size, size, seed=seed)
    start, goal = get_start_goal(grid)

    H, W = len(grid), len(grid[0])
    open_cells = sum(grid[r][c] == 0 for r in range(H) for c in range(W))
    print(f"\nGrid : {H}x{W}  |  Open cells (vertices) : {open_cells}")
    print(f"Start: {start}   Goal: {goal}\n")

    # --- BFS ---
    t0 = time.perf_counter()
    bfs_path, bfs_visited = bfs(grid, start, goal)
    bfs_time = time.perf_counter() - t0

    # --- A* ---
    t0 = time.perf_counter()
    as_path, as_visited = astar(grid, start, goal)
    as_time = time.perf_counter() - t0

    # Results table
    bfs_len = len(bfs_path) if bfs_path else -1
    as_len  = len(as_path)  if as_path  else -1
    match   = "✓ MATCH" if bfs_len == as_len else "✗ MISMATCH"

    print(f"{'Algorithm':<12} {'Path len':>9} {'Nodes visited':>14} {'Time (ms)':>10}")
    print("-" * 50)
    print(f"{'BFS':<12} {bfs_len:>9} {bfs_visited:>14} {bfs_time*1000:>10.4f}")
    print(f"{'A*':<12} {as_len:>9} {as_visited:>14} {as_time*1000:>10.4f}")
    print(f"\nPath-length cross-check : {match}\n")

    # ASCII render (BFS path)
    print("── BFS solution ──")
    print_maze(grid, path=bfs_path, start=start, goal=goal)
    print()
    print("── A* solution ──")
    print_maze(grid, path=as_path, start=start, goal=goal)

    # Matplotlib visualisation
    if plot:
        _plot(grid, bfs_path, as_path, start, goal, size, seed)


def _plot(grid, bfs_path, as_path, start, goal, size, seed):
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("\n[demo] matplotlib not installed — skipping plot.")
        return

    H, W = len(grid), len(grid[0])
    arr = np.array(grid, dtype=float)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    titles = ["BFS (Breadth-First Search)", "A* (Manhattan heuristic)"]
    paths  = [bfs_path, as_path]
    colors = ["#2196F3", "#4CAF50"]   # blue for BFS, green for A*

    for ax, title, path, color in zip(axes, titles, paths, colors):
        # Base maze
        display = arr.copy()
        ax.imshow(display, cmap="binary", interpolation="nearest", vmin=0, vmax=1)

        # Path overlay
        if path:
            pr = [p[0] for p in path]
            pc = [p[1] for p in path]
            ax.plot(pc, pr, color=color, linewidth=2, alpha=0.85, label="Path")

        # Start / Goal markers
        ax.plot(start[1], start[0], "rs", markersize=8, label="Start")
        ax.plot(goal[1],  goal[0],  "g*", markersize=12, label="Goal")

        path_len = len(path) if path else -1
        ax.set_title(f"{title}\nPath length = {path_len}", fontsize=11)
        ax.legend(loc="upper right", fontsize=8)
        ax.axis("off")

    fig.suptitle(f"MazePath — size={size}x{size}, seed={seed}", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig("demo_output.png", dpi=120, bbox_inches="tight")
    print("[demo] Plot saved to demo_output.png")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MazePath interactive demo")
    parser.add_argument("--size",    type=int,  default=15, help="Maze side (default 15)")
    parser.add_argument("--seed",    type=int,  default=42, help="Random seed (default 42)")
    parser.add_argument("--no-plot", action="store_true",   help="Skip matplotlib window")
    args = parser.parse_args()
    run_demo(size=args.size, seed=args.seed, plot=not args.no_plot)
