"""
Visualization module for the occupancy grid, obstacles, and computed path.
Group 6 - CSE440 Section 2
Author: Md. Sadman Bin Murtoza (2232901642)

Draws the grid using Matplotlib and saves the result as an image, so the
A* module's output can be inspected without the full GUI.
"""

import matplotlib
matplotlib.use("Agg")  # non-interactive backend, safe for headless runs
import matplotlib.pyplot as plt
import numpy as np


def visualize_grid(grid, path=None, explored=None, start=None, goal=None,
                    output_path="output/path_result.png"):
    """
    Draw the occupancy grid with the explored cells, computed path, start,
    and goal, then save it to output_path.

    Parameters
    ----------
    grid : list[list[int]]
        2D grid where 0 = free cell, 1 = blocked cell.
    path : list[tuple(int, int)], optional
        Cells that make up the final computed path.
    explored : list[tuple(int, int)], optional
        Cells expanded during the A* search.
    start : tuple(int, int), optional
        Starting cell.
    goal : tuple(int, int), optional
        Goal cell.
    output_path : str
        File path to save the rendered image to.
    """
    grid_array = np.array(grid)
    fig, ax = plt.subplots(figsize=(6, 6))

    # Base grid: free cells (white) and blocked cells (black)
    ax.imshow(grid_array, cmap="gray_r", vmin=0, vmax=1)

    # Explored cells
    if explored:
        rows = [c[0] for c in explored]
        cols = [c[1] for c in explored]
        ax.scatter(cols, rows, c="#a8d5ff", s=60, marker="s", label="Explored")

    # Final path
    if path:
        rows = [c[0] for c in path]
        cols = [c[1] for c in path]
        ax.plot(cols, rows, c="#1f77b4", linewidth=2, marker="o", label="Path")

    # Start and goal markers
    if start:
        ax.scatter(start[1], start[0], c="green", s=120, marker="*", label="Start")
    if goal:
        ax.scatter(goal[1], goal[0], c="red", s=120, marker="*", label="Goal")

    ax.set_xticks(range(grid_array.shape[1]))
    ax.set_yticks(range(grid_array.shape[0]))
    ax.set_title("A* Path Planning Result")
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
    fig.tight_layout()

    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Saved visualization to {output_path}")
