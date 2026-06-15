import random
from typing import List, Tuple


def generate_maze(rows: int, cols: int, seed: int = 42) -> List[List[int]]:
    """
    Generate a perfect maze of size (rows x cols) using iterative DFS.

    The actual grid dimensions are (2*rows+1) x (2*cols+1) because walls
    occupy their own cells.

    Parameters
    ----------
    rows : int  — number of logical cells vertically   (≥ 1)
    cols : int  — number of logical cells horizontally (≥ 1)
    seed : int  — random seed for reproducibility

    Returns
    -------
    grid : List[List[int]]
        2-D list of 0/1 values; 0 = passage, 1 = wall.
        grid[0][0] is top-left; grid[H-1][W-1] is bottom-right.
    """
    rng = random.Random(seed)

    H = 2 * rows + 1
    W = 2 * cols + 1

    # Start fully walled
    grid = [[1] * W for _ in range(H)]

    def cell_to_grid(r: int, c: int) -> Tuple[int, int]:
        return 2 * r + 1, 2 * c + 1

    def neighbours(r: int, c: int) -> List[Tuple[int, int]]:
        """Return logical cell neighbours (not yet visited)."""
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        result = []
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                result.append((nr, nc))
        return result

    visited = [[False] * cols for _ in range(rows)]
    start_r, start_c = 0, 0
    visited[start_r][start_c] = True
    gr, gc = cell_to_grid(start_r, start_c)
    grid[gr][gc] = 0

    stack = [(start_r, start_c)]

    while stack:
        r, c = stack[-1]
        nbrs = [(nr, nc) for nr, nc in neighbours(r, c) if not visited[nr][nc]]
        if not nbrs:
            stack.pop()
        else:
            nr, nc = rng.choice(nbrs)
            visited[nr][nc] = True
            # Carve wall between (r,c) and (nr,nc)
            wr = 2 * r + 1 + (nr - r)
            wc = 2 * c + 1 + (nc - c)
            grid[wr][wc] = 0
            gr2, gc2 = cell_to_grid(nr, nc)
            grid[gr2][gc2] = 0
            stack.append((nr, nc))

    return grid


def get_start_goal(grid: List[List[int]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Return (start, goal) positions for a maze grid.
    Start = top-left open cell, Goal = bottom-right open cell.
    """
    H = len(grid)
    W = len(grid[0])
    return (1, 1), (H - 2, W - 2)


def print_maze(grid: List[List[int]],
               path: List[Tuple[int, int]] = None,
               start: Tuple[int, int] = None,
               goal: Tuple[int, int] = None) -> None:
    """Pretty-print a maze to stdout with optional path overlay."""
    path_set = set(path) if path else set()
    for r, row in enumerate(grid):
        line = ""
        for c, cell in enumerate(row):
            pos = (r, c)
            if pos == start:
                line += "S"
            elif pos == goal:
                line += "G"
            elif pos in path_set:
                line += "·"
            elif cell == 1:
                line += "█"
            else:
                line += " "
        print(line)


if __name__ == "__main__":
    grid = generate_maze(10, 20, seed=42)
    start, goal = get_start_goal(grid)
    print_maze(grid, start=start, goal=goal)
