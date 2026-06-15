import csv
import math
import os

OUTPUT_PLOT = "benchmark_plot.png"
CSV_FILE    = "results.csv"


def read_csv(path: str) -> list:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def fit_slope(xs: list, ys: list) -> float:
    """Least-squares linear fit on log-log data → empirical exponent."""
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys if y > 0]
    n = min(len(lx), len(ly))
    lx, ly = lx[:n], ly[:n]
    mean_x = sum(lx) / n
    mean_y = sum(ly) / n
    num   = sum((lx[i] - mean_x) * (ly[i] - mean_y) for i in range(n))
    denom = sum((lx[i] - mean_x) ** 2 for i in range(n))
    return num / denom if denom != 0 else 0.0


def plot(rows: list) -> None:
    try:
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker
    except ImportError:
        print("matplotlib not installed. Run: pip install matplotlib")
        return

    V      = [float(r["n_vertices"])   for r in rows]
    bfs_t  = [float(r["bfs_ms"])       for r in rows]
    as_t   = [float(r["astar_ms"])     for r in rows]
    bfs_v  = [float(r["bfs_visited"])  for r in rows]
    as_v   = [float(r["astar_visited"])for r in rows]

    slope_bfs_t  = fit_slope(V, bfs_t)
    slope_as_t   = fit_slope(V, as_t)
    slope_bfs_v  = fit_slope(V, bfs_v)
    slope_as_v   = fit_slope(V, as_v)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # ── Plot 1: Runtime ──
    ax1.loglog(V, bfs_t, "o-",  color="#2196F3", linewidth=2,
               label=f"BFS   (slope ≈ {slope_bfs_t:.2f})")
    ax1.loglog(V, as_t,  "s--", color="#4CAF50", linewidth=2,
               label=f"A*    (slope ≈ {slope_as_t:.2f})")
    ax1.set_xlabel("Number of vertices (V)", fontsize=11)
    ax1.set_ylabel("Runtime (ms)", fontsize=11)
    ax1.set_title("Runtime vs. Graph Size (log-log)", fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(True, which="both", linestyle="--", alpha=0.5)
    ax1.xaxis.set_major_formatter(ticker.ScalarFormatter())

    # ── Plot 2: Nodes visited ──
    ax2.loglog(V, bfs_v, "o-",  color="#2196F3", linewidth=2,
               label=f"BFS   (slope ≈ {slope_bfs_v:.2f})")
    ax2.loglog(V, as_v,  "s--", color="#4CAF50", linewidth=2,
               label=f"A*    (slope ≈ {slope_as_v:.2f})")
    ax2.set_xlabel("Number of vertices (V)", fontsize=11)
    ax2.set_ylabel("Nodes visited", fontsize=11)
    ax2.set_title("Nodes Visited vs. Graph Size (log-log)", fontsize=12)
    ax2.legend(fontsize=10)
    ax2.grid(True, which="both", linestyle="--", alpha=0.5)
    ax2.xaxis.set_major_formatter(ticker.ScalarFormatter())

    fig.suptitle("MazePath — BFS vs A* Benchmark", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT, dpi=150, bbox_inches="tight")
    print(f"Plot saved to {OUTPUT_PLOT}")
    plt.show()


if __name__ == "__main__":
    if not os.path.exists(CSV_FILE):
        print(f"'{CSV_FILE}' not found. Run `python benchmark.py` first.")
    else:
        rows = read_csv(CSV_FILE)
        plot(rows)
        # Print slope summary
        V     = [float(r["n_vertices"]) for r in rows]
        bfs_t = [float(r["bfs_ms"])     for r in rows]
        as_t  = [float(r["astar_ms"])   for r in rows]
        print(f"\nEmpirical growth exponent (runtime):")
        print(f"  BFS : {fit_slope(V, bfs_t):.3f}   (theory: ~1.0  O(V))")
        print(f"  A*  : {fit_slope(V, as_t):.3f}   (theory: ~1.15 O(V log V))")
