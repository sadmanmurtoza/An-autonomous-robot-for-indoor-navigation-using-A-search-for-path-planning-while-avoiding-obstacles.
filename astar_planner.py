"""
astar_planner.py

Grid-based A* path planner for the indoor navigation robot project.

Represents the environment as a 2D occupancy grid (0 = free, 1 = occupied)
and computes the lowest-cost path between a start and goal cell using A*
search with 8-connectivity (cardinal + diagonal moves) and an octile
distance heuristic (admissible for 8-connected grids).

Exposes two entry points:
  - a_star_search(grid, start, goal) -> dict
        Drop-in replacement for support.astar.a_star_search. Returns
        {"path": [...], "explored": [...], "found": bool}, so main.py
        needs no changes beyond the import line.
  - a_star(grid, start, goal) -> list | None
        Original, simpler interface kept for standalone use/testing.
"""

import heapq
import math


def octile_heuristic(a, b):
    """Admissible heuristic for 8-connected grids."""
    dr = abs(a[0] - b[0])
    dc = abs(a[1] - b[1])
    return (dr + dc) + (math.sqrt(2) - 2) * min(dr, dc)


def get_neighbors(node, grid):
    rows, cols = len(grid), len(grid[0])
    r, c = node
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1),
              (-1, -1), (-1, 1), (1, -1), (1, 1)]
    neighbors = []
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            # Prevent cutting diagonally through two blocked corner cells
            if dr != 0 and dc != 0:
                if grid[r + dr][c] == 1 and grid[r][c + dc] == 1:
                    continue
            cost = math.sqrt(2) if dr != 0 and dc != 0 else 1.0
            neighbors.append(((nr, nc), cost))
    return neighbors


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def a_star_search(grid, start, goal):
    """
    Run A* search and return a result dict in the same shape as
    support.astar.a_star_search, so this function is a drop-in
    replacement for it in main.py:

        {"path": [(row, col), ...], "explored": [(row, col), ...], "found": bool}

    "explored" lists cells in the order they were expanded (popped from
    the open set), useful for the performance reporting mentioned in the
    Week 6 plan (path length, explored-node count).
    """
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    visited = set()
    explored = []

    while open_set:
        _, current = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.add(current)
        explored.append(current)

        if current == goal:
            return {
                "path": reconstruct_path(came_from, current),
                "explored": explored,
                "found": True,
            }

        for neighbor, move_cost in get_neighbors(current, grid):
            if neighbor in visited:
                continue
            tentative_g = g_score[current] + move_cost
            if tentative_g < g_score.get(neighbor, math.inf):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + octile_heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return {"path": [], "explored": explored, "found": False}


def a_star(grid, start, goal):
    """
    Simpler interface kept for standalone use and existing tests:
    returns the waypoint list directly, or None if no path exists.
    """
    result = a_star_search(grid, start, goal)
    return result["path"] if result["found"] else None


if __name__ == "__main__":
    # Synthetic 10x10 test grid (0 = free, 1 = obstacle)
    test_grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
    ]

    start, goal = (0, 0), (9, 9)

    # Test the new dict interface (what main.py will call)
    result = a_star_search(test_grid, start, goal)
    if result["found"]:
        print(f"Path found ({len(result['path'])} cells): {result['path']}")
        print(f"Explored {len(result['explored'])} cells during search.")
    else:
        print("No path exists between the start and goal cells.")

    # Test the original list/None interface
    path = a_star(test_grid, start, goal)
    assert path == result["path"], "a_star() and a_star_search() disagree"
    print("\na_star() legacy interface matches a_star_search() output — OK")
