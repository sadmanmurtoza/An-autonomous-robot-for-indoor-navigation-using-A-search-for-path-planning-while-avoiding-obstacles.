"""
astar_planner.py

Grid-based A* path planner for the indoor navigation robot project.

Represents the environment as a 2D occupancy grid (0 = free, 1 = occupied)
and computes the lowest-cost path between a start and goal cell using A*
search with 8-connectivity (cardinal + diagonal moves) and an octile
distance heuristic (admissible for 8-connected grids).

Output is an ordered list of (row, col) waypoints, which downstream modules
(path follower) convert into linear/angular velocity commands.
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


def a_star(grid, start, goal):
    """
    Returns the optimal waypoint path from start to goal as a list of
    (row, col) tuples, or None if no path exists.
    """
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        if current in visited:
            continue
        visited.add(current)

        for neighbor, move_cost in get_neighbors(current, grid):
            tentative_g = g_score[current] + move_cost
            if tentative_g < g_score.get(neighbor, math.inf):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + octile_heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return None  # no path found


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


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
    path = a_star(test_grid, start, goal)

    if path:
        print(f"Path found ({len(path)} waypoints, "
              f"cost={sum(1 for _ in path):.0f} cells):")
        print(path)
    else:
        print("No path found.")
