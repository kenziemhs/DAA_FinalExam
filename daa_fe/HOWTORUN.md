# MazePath — How to Run

A complete guide to running the demo, game, benchmark, and plot scripts.

---

## Prerequisites

- **Python 3.10+** (tested on Python 3.12)
- **pip** to install dependencies

Check your Python version:
```bash
python --version
```

---

## 1. Clone & Enter the Folder

```bash
git clone https://github.com/[your-username]/mazepath.git
cd mazepath
```

---

## 2. Install Dependencies

```bash
pip install matplotlib numpy pygame
```

> `heapq` and `collections` are Python built-ins — no installation needed.

---

## 3. Run the Interactive Demo

### ASCII mode (no matplotlib required)
```bash
python demo.py --size 10 --seed 42 --no-plot
```

Example output:
```
============================================================
  MazePath Demo  —  size=10x10  seed=42
============================================================

Grid : 21x21  |  Open cells (vertices) : 199
Start: (1, 1)   Goal: (19, 19)

Algorithm     Path len  Nodes visited  Time (ms)
--------------------------------------------------
BFS                 93             99     0.0974
A*                  93             93     0.2203

Path-length cross-check : ✓ MATCH

── BFS solution ──
█████████████████████
█S█···█···█·········█
█·█·█·█·█·█·███████·█
...
█ █             █  G█
█████████████████████
```

### With plot (requires matplotlib)
```bash
python demo.py --size 15 --seed 42
```
A two-panel window (BFS vs A*) will appear and the image will be saved as `demo_output.png`.

### Available options
| Flag | Default | Description |
|------|---------|-------------|
| `--size N` | 15 | Maze side length N×N (actual grid = 2N+1 × 2N+1) |
| `--seed S` | 42 | Random seed for reproducibility |
| `--no-plot` | off | Skip the matplotlib window |

Example variations:
```bash
# Small maze (easy to read)
python demo.py --size 5 --seed 42 --no-plot

# Large maze
python demo.py --size 50 --seed 99 --no-plot

# Different seed = different maze layout
python demo.py --size 15 --seed 123 --no-plot
```

---

## 4. Play the Interactive Game

```bash
python game.py
```

A pygame window will open with a playable maze. Navigate from **S** (green square) to **G** (red square) using the keyboard.

### Controls

| Key | Action |
|-----|--------|
| `↑ ↓ ← →` or `WASD` | Move player |
| `H` | Toggle BFS hint path (blue) |
| `A` | Toggle A* hint path (green) |
| `R` | Restart with a new maze |
| `+` / `-` | Increase / decrease maze size |
| `ESC` | Quit |

> Using a hint adds a **+5 step penalty**. Try to beat the optimal path length shown in the HUD!

When you reach the goal, a results screen compares your steps and time against the BFS and A* optimal solutions.

---

## 5. Run the Benchmark (Reproduce Timing Data)

Single command to regenerate all timing data:

```bash
# Linux / macOS
python benchmark.py && python plot_results.py

# Windows PowerShell
python benchmark.py; python plot_results.py
```

Example benchmark output:
```
MazePath Benchmark — BFS vs A*
Sizes  : [10, 25, 50, 100, 250, 500, 750, 1000]
Trials : 5  (seeds 42–46)

  Size   Vertices   BFS (ms)    A* (ms)    BFS vis     A* vis  Match?
----------------------------------------------------------------------
    10        199      0.085      0.182        111        102       ✓
    25       1249      0.506      1.023        642        585       ✓
    50       4999      2.742      6.690       3190       3046       ✓
   100      19999     10.553     20.967      11760      11608       ✓
   250     124999     83.253    171.876      79328      78020       ✓
   500     499999    322.028    652.709     274158     271977       ✓
   750    1124999    797.234   1498.028     638688     630309       ✓
  1000    1999999   1193.862   2392.911    1053796    1043539       ✓

✓ All sizes: BFS and A* returned identical path lengths.
```

Generated files:
- `results.csv` — raw timing data
- `benchmark_plot.png` — log-log runtime & nodes visited plots

---

## 6. Generate Plot Only (from existing CSV)

```bash
python plot_results.py
```

---

## File Structure

```
mazepath/
├── maze_generator.py   # DFS-based maze generator
├── bfs.py              # BFS algorithm (from scratch)
├── astar.py            # A* algorithm (from scratch)
├── demo.py             # Static visualisation demo
├── game.py             # Interactive pygame game
├── benchmark.py        # Benchmark harness → results.csv
├── plot_results.py     # Plot generator → benchmark_plot.png
├── HOWTORUN.md         # This guide
└── README.md           # Full project description
```

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'matplotlib'`**
```bash
pip install matplotlib numpy
```

**`ModuleNotFoundError: No module named 'pygame'`**
```bash
pip install pygame
```

**Plot window does not appear but no error is shown**  
Add `--no-plot` and check `demo_output.png` in the same folder.

**`&&` is not recognised in PowerShell**  
Use `;` instead:
```powershell
python benchmark.py; python plot_results.py
```

**Benchmark is slow at size 1000**  
This is expected — size 1000 means ~2 million vertices. Estimated time: 1–3 minutes depending on your machine.
