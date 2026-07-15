"""
Test script for the A* path-planning module.
Group 6 - CSE440 Section 2
Author: Md. Sadman Bin Murtoza (2232901642)

Runs the A* algorithm against three sample grids of increasing difficulty
and reports whether a correct path is found (or correctly reported as
unreachable).
"""

from astar import a_star_search


def print_result(name, grid, start, goal):
    result = a_star_search(grid, start, goal)
    print(f"--- {name} ---")
    print(f"Start: {start}, Goal: {goal}")
    if result["found"]:
        print(f"Path found ({len(result['path'])} cells): {result['path']}")
    else:
        print("No path found.")
    print(f"Explored {len(result['explored'])} cells.\n")
    return result


if __name__ == "__main__":
    # Test 1: Simple open grid, direct path expected
    grid_1 = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    print_result("Test 1: Open grid", grid_1, (0, 0), (3, 3))

    # Test 2: Grid with a wall, requiring the path to go around
    grid_2 = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
    ]
    print_result("Test 2: Grid with obstacles", grid_2, (0, 0), (4, 4))

    # Test 3: Grid with the goal completely walled off (unreachable)
    grid_3 = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 1, 0, 0, 1],
        [0, 1, 0, 1, 1],
        [0, 0, 0, 1, 0],
    ]
    print_result("Test 3: Unreachable goal", grid_3, (0, 0), (4, 4))
