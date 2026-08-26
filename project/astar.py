# ============================================================
# member2_sadman_astar.py
# Member 2 work: A* Path Planning Core
#
# This file does ONLY path-planning work.
# It finds a safe shortest route from START to GOAL.
# It also reports useful information for the GUI.
# ============================================================

# heapq gives us a "priority queue".
# A priority queue always gives us the most important item first.
import heapq

# time lets us measure how long A* needs to calculate a path.
import time


# This class keeps all A* path-planning jobs together.
class AStarPlanner:

    # Manhattan distance estimates how far one cell is from another.
    # We only move UP, DOWN, LEFT, or RIGHT.
    def heuristic(self, cell, goal):
        # Take the row number from the first cell.
        row1 = cell[0]
        # Take the column number from the first cell.
        col1 = cell[1]
        # Take the row number from the goal cell.
        row2 = goal[0]
        # Take the column number from the goal cell.
        col2 = goal[1]
        # Add row distance and column distance.
        return abs(row1 - row2) + abs(col1 - col2)

    # This helper gives all legal nearby cells.
    def get_neighbors(self, cell, rows, columns):
        # Read current row.
        row = cell[0]
        # Read current column.
        col = cell[1]

        # These are the four directions our robot can move.
        directions = [
            (-1, 0),  # UP
            (1, 0),   # DOWN
            (0, -1),  # LEFT
            (0, 1),   # RIGHT
        ]

        # Start with an empty neighbor list.
        neighbors = []

        # Check every direction one by one.
        for row_change, col_change in directions:
            # Calculate the possible new row.
            new_row = row + row_change
            # Calculate the possible new column.
            new_col = col + col_change

            # Only keep the cell if it is inside the map.
            if 0 <= new_row < rows and 0 <= new_col < columns:
                # Save the legal neighbor.
                neighbors.append((new_row, new_col))

        # Give the neighbor list back.
        return neighbors

    # This helper rebuilds the final path after A* reaches the goal.
    def rebuild_path(self, came_from, current):
        # Start the path at the goal cell.
        path = [current]

        # Keep moving backward while a parent cell exists.
        while current in came_from:
            # Go to the previous cell.
            current = came_from[current]
            # Save that cell too.
            path.append(current)

        # Right now the path is GOAL -> START.
        # Reverse it so it becomes START -> GOAL.
        path.reverse()

        # Return the correct path.
        return path

    # This checks whether a finished path is safe and legal.
    def validate_path(self, grid, path):
        # If there is no path, it cannot be valid.
        if not path:
            return False

        # Count the map rows.
        rows = len(grid)
        # Count the map columns.
        columns = len(grid[0]) if rows > 0 else 0

        # Check every cell in the path.
        for row, col in path:
            # The cell must stay inside the map.
            if not (0 <= row < rows and 0 <= col < columns):
                return False
            # The cell must not be an obstacle.
            if grid[row][col] == 1:
                return False

        # Check that every step moves only one square.
        for index in range(1, len(path)):
            # Read the previous cell.
            old_row, old_col = path[index - 1]
            # Read the next cell.
            new_row, new_col = path[index]
            # Manhattan distance between neighboring cells should be exactly 1.
            step_distance = abs(old_row - new_row) + abs(old_col - new_col)
            # If the jump is bigger or smaller than one, the path is bad.
            if step_distance != 1:
                return False

        # If every check passed, the path is valid.
        return True

    # This is the main A* search function.
    def find_path(self, grid, start, goal):
        # Record when the calculation starts.
        start_time = time.perf_counter()

        # Count rows in the grid.
        rows = len(grid)
        # Count columns in the grid.
        columns = len(grid[0]) if rows > 0 else 0

        # Prepare a result dictionary.
        # The GUI can read all useful information from this one object.
        result = {
            "path": [],
            "explored": [],
            "path_length": 0,
            "explored_count": 0,
            "calculation_time_ms": 0.0,
            "success": False,
            "message": "No path found.",
        }

        # Stop if the map is empty.
        if rows == 0 or columns == 0:
            result["message"] = "The map is empty."
            return result

        # Stop if start or goal was not selected.
        if start is None or goal is None:
            result["message"] = "Please choose both start and destination."
            return result

        # Stop if start is outside the map.
        if not (0 <= start[0] < rows and 0 <= start[1] < columns):
            result["message"] = "Start is outside the map."
            return result

        # Stop if goal is outside the map.
        if not (0 <= goal[0] < rows and 0 <= goal[1] < columns):
            result["message"] = "Destination is outside the map."
            return result

        # Stop if start is blocked.
        if grid[start[0]][start[1]] == 1:
            result["message"] = "Start cell is blocked."
            return result

        # Stop if goal is blocked.
        if grid[goal[0]][goal[1]] == 1:
            result["message"] = "Destination cell is blocked."
            return result

        # open_list stores cells A* may visit next.
        open_list = []

        # Put start cell into the priority queue.
        # The first number is its priority.
        heapq.heappush(open_list, (0, start))

        # came_from remembers the parent of each discovered cell.
        came_from = {}

        # g_score is the real number of steps from START to a cell.
        g_score = {start: 0}

        # closed_set remembers cells already fully checked.
        closed_set = set()

        # explored_order remembers the order A* checked cells.
        explored_order = []

        # Keep searching while cells remain in the queue.
        while open_list:
            # Take the cell with the smallest estimated total cost.
            _, current = heapq.heappop(open_list)

            # Skip cells already finished before.
            if current in closed_set:
                continue

            # Mark current cell as fully checked.
            closed_set.add(current)

            # Save it for visualization.
            explored_order.append(current)

            # If A* reached the goal, the search is complete.
            if current == goal:
                # Build the final path.
                path = self.rebuild_path(came_from, current)

                # Measure total calculation time.
                elapsed_ms = (time.perf_counter() - start_time) * 1000

                # Save all final information.
                result["path"] = path
                result["explored"] = explored_order
                # Path length means number of MOVES, so subtract one from cell count.
                result["path_length"] = max(0, len(path) - 1)
                result["explored_count"] = len(explored_order)
                result["calculation_time_ms"] = elapsed_ms
                result["success"] = self.validate_path(grid, path)
                result["message"] = "Safe shortest path found." if result["success"] else "Path failed validation."

                # Return the completed result.
                return result

            # Check each nearby cell.
            for neighbor in self.get_neighbors(current, rows, columns):
                # Read neighbor row.
                n_row = neighbor[0]
                # Read neighbor column.
                n_col = neighbor[1]

                # A 1 means obstacle, so the robot cannot enter this cell.
                if grid[n_row][n_col] == 1:
                    continue

                # Moving one square costs one step.
                new_g = g_score[current] + 1

                # Read the old best cost.
                old_g = g_score.get(neighbor, float("inf"))

                # Only save this route if it is better.
                if new_g < old_g:
                    # Remember how we reached this neighbor.
                    came_from[neighbor] = current
                    # Save the new real cost.
                    g_score[neighbor] = new_g
                    # f = real cost + estimated distance to goal.
                    f_score = new_g + self.heuristic(neighbor, goal)
                    # Put the neighbor into the queue.
                    heapq.heappush(open_list, (f_score, neighbor))

        # If the loop finishes, no route exists.
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        # Save explored cells even when search fails.
        result["explored"] = explored_order
        # Save explored count.
        result["explored_count"] = len(explored_order)
        # Save calculation time.
        result["calculation_time_ms"] = elapsed_ms
        # Explain the problem clearly.
        result["message"] = "No route exists between start and destination."

        # Return the failed result.
        return result

    # Dynamic replanning simply runs A* again from the robot's CURRENT cell.
    def replan(self, grid, current_position, goal):
        # Call the same safe A* function with a new start position.
        return self.find_path(grid, current_position, goal)
