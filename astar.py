"""
A* Path-Planning Module
Group 6 - CSE440 Section 2
Author: Md. Sadman Bin Murtoza (2232901642)

Implements the A* search algorithm on a 2D occupancy grid to find the
shortest path between a start cell and a goal cell, avoiding blocked cells.
"""

import heapq


def manhattan_distance(a, b):
    """Heuristic: Manhattan distance between two grid cells (row, col)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(cell, grid):
    """Return valid, in-bounds, non-blocked neighboring cells (4-directional)."""
    rows, cols = len(grid), len(grid[0])
    row, col = cell
    candidates = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

    neighbors = []
    for r, c in candidates:
        if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0:
            neighbors.append((r, c))
    return neighbors


def reconstruct_path(came_from, current):
    """Rebuild the path from goal back to start using the came_from map."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def a_star_search(grid, start, goal):
    """
    Run A* search on a 2D occupancy grid.

    Parameters
    ----------
    grid : list[list[int]]
        2D grid where 0 = free cell, 1 = blocked cell.
    start : tuple(int, int)
        Starting cell (row, col).
    goal : tuple(int, int)
        Goal cell (row, col).

    Returns
    -------
    dict with keys:
        "path": list of (row, col) cells from start to goal, or [] if no path exists.
        "explored": list of (row, col) cells expanded during the search.
        "found": bool, True if a path was found.
    """
    if grid[start[0]][start[1]] == 1 or grid[goal[0]][goal[1]] == 1:
        return {"path": [], "explored": [], "found": False}

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, goal)}
    explored = []
    visited = set()

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

        for neighbor in get_neighbors(current, grid):
            if neighbor in visited:
                continue

            tentative_g = g_score[current] + 1  # uniform cost per step

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + manhattan_distance(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # Open set exhausted without reaching goal -> no path exists
    return {"path": [], "explored": explored, "found": False}
