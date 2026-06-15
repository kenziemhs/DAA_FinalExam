# MazePath — Cara Menjalankan

Panduan lengkap untuk menjalankan demo, benchmark, dan plot.

---

## Prasyarat

- **Python 3.10+** (tested on Python 3.12)
- **pip** untuk install dependensi

Cek versi Python kamu:
```bash
python --version
```

---

## 1. Clone & Masuk Folder

```bash
git clone https://github.com/[your-username]/mazepath.git
cd mazepath
```

---

## 2. Install Dependensi

```bash
pip install matplotlib numpy
```

> `heapq` dan `collections` sudah built-in Python, tidak perlu install.

---

## 3. Jalankan Demo Interaktif

### Mode ASCII (tanpa matplotlib)
```bash
python demo.py --size 10 --seed 42 --no-plot
```

Contoh output:
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

### Mode dengan Plot (butuh matplotlib)
```bash
python demo.py --size 15 --seed 42
```
Akan muncul window dua panel (BFS vs A*) dan tersimpan ke `demo_output.png`.

### Opsi yang tersedia
| Flag | Default | Keterangan |
|------|---------|------------|
| `--size N` | 15 | Ukuran maze N×N (grid aktual = 2N+1 × 2N+1) |
| `--seed S` | 42 | Random seed untuk reproducibility |
| `--no-plot` | off | Skip window matplotlib |

Contoh variasi:
```bash
# Maze kecil (gampang diliat)
python demo.py --size 5 --seed 42 --no-plot

# Maze besar
python demo.py --size 50 --seed 99 --no-plot

# Seed berbeda = maze berbeda
python demo.py --size 15 --seed 123 --no-plot
```

---

## 4. Jalankan Benchmark (Reproduksi Data)

Satu perintah untuk regenerate semua data timing:

```bash
python benchmark.py && python plot_results.py
```

Contoh output benchmark:
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

File yang dihasilkan:
- `results.csv` — data timing mentah
- `benchmark_plot.png` — grafik log-log runtime & nodes visited

---

## 5. Hanya Generate Plot (dari CSV yang sudah ada)

```bash
python plot_results.py
```

---

## Struktur File

```
mazepath/
├── maze_generator.py   # Generator maze DFS
├── bfs.py              # Algoritma BFS (from scratch)
├── astar.py            # Algoritma A* (from scratch)
├── demo.py             # Demo interaktif
├── benchmark.py        # Benchmark harness → results.csv
├── plot_results.py     # Plot generator → benchmark_plot.png
├── HOWTORUN.md         # Panduan ini
└── README.md           # Deskripsi proyek lengkap
```

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'matplotlib'`**
```bash
pip install matplotlib numpy
```

**Plot tidak muncul tapi tidak error**  
Tambahkan `--no-plot` dan cek `demo_output.png` di folder yang sama.

**Benchmark lambat di size 1000**  
Normal — size 1000 artinya ~2 juta vertices. Estimasi waktu: 1–3 menit tergantung mesin.
