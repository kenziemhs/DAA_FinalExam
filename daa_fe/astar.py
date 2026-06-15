import heapq
from typing import List, Tuple, Optional, Dict


def _manhattan(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Admissible Manhattan-distance heuristic h(n) for grid mazes."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid: List[List[int]],
          start: Tuple[int, int],
          goal: Tuple[int, int]) -> Tuple[Optional[List[Tuple[int, int]]], int]:
    """
    Run A* on *grid* from *start* to *goal* using the Manhattan heuristic.

    Parameters
    ----------
    grid  : 2-D list  — 0 = open, 1 = wall
    start : (row, col) — source cell
    goal  : (row, col) — target cell

    Returns
    -------
    path          : list of (row, col) from start to goal inclusive,
                    or None if no path exists.
    nodes_visited : total cells popped from the open set (work done).
    """
    H = len(grid)
    W = len(grid[0])

    # g[cell] = best known cost from start to cell
    g: Dict[Tuple[int, int], int] = {start: 0}
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    nodes_visited = 0

    # Min-heap entries: (f, g, cell)
    # We include g as a tiebreaker so the heap is fully ordered.
    open_heap: List[Tuple[int, int, Tuple[int, int]]] = []
    heapq.heappush(open_heap, (0 + _manhattan(start, goal), 0, start))

    DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_heap:
        f, g_cur, cur = heapq.heappop(open_heap)

        # Lazy deletion: skip stale heap entries
        if g_cur > g.get(cur, float("inf")):
            continue

        nodes_visited += 1

        if cur == goal:
            return _reconstruct(parent, goal), nodes_visited

        r, c = cur
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            nxt = (nr, nc)
            if not (0 <= nr < H and 0 <= nc < W and grid[nr][nc] == 0):
                continue
            g_new = g_cur + 1          # uniform edge weight = 1
            if g_new < g.get(nxt, float("inf")):
                g[nxt] = g_new
                parent[nxt] = cur
                f_new = g_new + _manhattan(nxt, goal)
                heapq.heappush(open_heap, (f_new, g_new, nxt))

    return None, nodes_visited


def _reconstruct(parent: Dict, goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Walk parent pointers from goal back to start and reverse."""
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


if __name__ == "__main__":
    from maze_generator import generate_maze, get_start_goal, print_maze

    grid = generate_maze(10, 20, seed=42)
    start, goal = get_start_goal(grid)
    path, visited = astar(grid, start, goal)

    print(f"A* path length  : {len(path) if path else 'No path'}")
    print(f"Nodes visited   : {visited}")
    print_maze(grid, path=path, start=start, goal=goal)
