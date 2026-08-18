# ============================================================
# astar.py
# This file contains the A* path-finding algorithm.
# A* helps our virtual robot find a short safe path to the goal.
# ============================================================

# heapq gives us a special list where the smallest value comes first.
import heapq


def heuristic(a, b):
    # a is one grid position, for example (2, 3).
    # b is another grid position, for example (7, 8).
    # We find how far the two positions are from each other.
    # abs() changes a negative number into a positive number.
    row_distance = abs(a[0] - b[0])
    # We also find the left-right distance.
    column_distance = abs(a[1] - b[1])
    # We add both distances and return the answer.
    return row_distance + column_distance


def get_neighbors(position, rows, columns):
    # position stores the robot's current row and column.
    row, column = position
    # This empty list will store nearby cells that are inside the map.
    neighbors = []
    # These four pairs mean: up, down, left, and right.
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # We check every possible direction one by one.
    for row_change, column_change in directions:
        # Find the new row after moving in this direction.
        new_row = row + row_change
        # Find the new column after moving in this direction.
        new_column = column + column_change
        # Make sure the new cell is still inside the grid.
        if 0 <= new_row < rows and 0 <= new_column < columns:
            # Add the safe grid position to our neighbor list.
            neighbors.append((new_row, new_column))
    # Give the list of nearby positions back to A*.
    return neighbors


def rebuild_path(came_from, current):
    # Start the final path with the destination cell.
    path = [current]
    # Keep going backward while we know where the cell came from.
    while current in came_from:
        # Move to the cell that came before the current cell.
        current = came_from[current]
        # Add that earlier cell to the path.
        path.append(current)
    # We built the path backward, so reverse it to start -> destination.
    path.reverse()
    # Return the correctly ordered path.
    return path


def astar_search(grid, start, goal):
    # Count how many rows the map has.
    rows = len(grid)
    # Count how many columns the map has.
    columns = len(grid[0]) if rows > 0 else 0
    # If the grid is empty, there is nothing to search.
    if rows == 0 or columns == 0:
        return [], []
    # If no start or goal was selected, we cannot find a path.
    if start is None or goal is None:
        return [], []
    # If the start or goal is blocked by an obstacle, stop.
    if grid[start[0]][start[1]] == 1 or grid[goal[0]][goal[1]] == 1:
        return [], []

    # This priority queue stores cells A* may visit next.
    open_list = []
    # Put the start cell in the queue.
    heapq.heappush(open_list, (0, start))
    # came_from remembers the parent of each visited cell.
    came_from = {}
    # g_score means the real number of steps used to reach a cell.
    g_score = {start: 0}
    # This set helps us avoid processing the same cell again and again.
    closed_set = set()
    # This list remembers the order of explored cells for visualization.
    explored_order = []

    # Continue while there is at least one cell left to check.
    while open_list:
        # Take the cell with the smallest estimated total cost.
        _, current = heapq.heappop(open_list)
        # Skip it if we already completely checked it before.
        if current in closed_set:
            continue
        # Mark the cell as fully checked.
        closed_set.add(current)
        # Remember it so the GUI can show explored cells.
        explored_order.append(current)

        # If this cell is the destination, our search is finished.
        if current == goal:
            # Build and return the final path plus explored cells.
            return rebuild_path(came_from, current), explored_order

        # Look at every up/down/left/right neighbor.
        for neighbor in get_neighbors(current, rows, columns):
            # Read the neighbor's row number.
            neighbor_row = neighbor[0]
            # Read the neighbor's column number.
            neighbor_column = neighbor[1]
            # A value of 1 means there is an obstacle, so do not enter it.
            if grid[neighbor_row][neighbor_column] == 1:
                continue
            # Moving to one neighboring cell costs one step.
            tentative_g_score = g_score[current] + 1
            # Read the best old cost; infinity means we never saw it before.
            old_g_score = g_score.get(neighbor, float("inf"))
            # Only save this route if it is better than the old route.
            if tentative_g_score < old_g_score:
                # Remember that current is the parent of neighbor.
                came_from[neighbor] = current
                # Save the new best real cost.
                g_score[neighbor] = tentative_g_score
                # f_score = real cost + estimated distance to destination.
                f_score = tentative_g_score + heuristic(neighbor, goal)
                # Put the neighbor into the priority queue.
                heapq.heappush(open_list, (f_score, neighbor))

    # If the loop ends, no safe path exists.
    return [], explored_order
