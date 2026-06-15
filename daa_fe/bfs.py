from collections import deque
from typing import List, Tuple, Optional, Dict


def bfs(grid: List[List[int]],
        start: Tuple[int, int],
        goal: Tuple[int, int]) -> Tuple[Optional[List[Tuple[int, int]]], int]:
    """
    Run BFS on *grid* from *start* to *goal*.

    Parameters
    ----------
    grid  : 2-D list  — 0 = open, 1 = wall
    start : (row, col) — source cell
    goal  : (row, col) — target cell

    Returns
    -------
    path          : list of (row, col) from start to goal inclusive,
                    or None if no path exists.
    nodes_visited : total number of cells dequeued (work done).
    """
    H = len(grid)
    W = len(grid[0])

    # parent[cell] = cell we came from; used to reconstruct path
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    queue: deque = deque([start])
    nodes_visited = 0

    DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        cur = queue.popleft()
        nodes_visited += 1

        if cur == goal:
            return _reconstruct(parent, goal), nodes_visited

        r, c = cur
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            nxt = (nr, nc)
            if (0 <= nr < H and 0 <= nc < W
                    and grid[nr][nc] == 0
                    and nxt not in parent):
                parent[nxt] = cur
                queue.append(nxt)

    return None, nodes_visited   # no path found


def _reconstruct(parent: Dict, goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Walk the parent pointers from goal back to start and reverse."""
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
    path, visited = bfs(grid, start, goal)

    print(f"BFS path length : {len(path) if path else 'No path'}")
    print(f"Nodes visited   : {visited}")
    print_maze(grid, path=path, start=start, goal=goal)
