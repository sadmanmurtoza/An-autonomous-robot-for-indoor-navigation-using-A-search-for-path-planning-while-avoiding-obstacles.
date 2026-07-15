"""
Main entry point for the Autonomous Indoor Navigation Robot simulation.
Group 6 - CSE440 Section 2

Currently wires together: sample floor plan loading, A* path planning,
and visualization of the result. Robot movement and the full graphical
interface will be integrated as those modules are completed by the team.
"""

import csv
import os

from support.astar import a_star_search
from support.visualize import visualize_grid


def load_grid(csv_path):
    """Load a 2D occupancy grid (0 = free, 1 = blocked) from a CSV file."""
    grid = []
    with open(csv_path, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            grid.append([int(cell) for cell in row])
    return grid


def main():
    grid_path = os.path.join("data", "floorplan_v1.csv")
    grid = load_grid(grid_path)

    start = (0, 0)
    goal = (len(grid) - 1, len(grid[0]) - 1)

    result = a_star_search(grid, start, goal)

    if result["found"]:
        print(f"Path found with {len(result['path'])} cells.")
        print(f"Explored {len(result['explored'])} cells during search.")
    else:
        print("No path exists between the start and goal cells.")

    os.makedirs("output", exist_ok=True)
    visualize_grid(
        grid,
        path=result["path"],
        explored=result["explored"],
        start=start,
        goal=goal,
        output_path=os.path.join("output", "path_result.png"),
    )


if __name__ == "__main__":
    main()
