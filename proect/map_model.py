# ============================================================
# map_model.py
# This file stores and manages the indoor occupancy grid.
# 0 means FREE cell and 1 means BLOCKED cell.
# ============================================================

# json lets us save the map into a simple text file and load it later.
import json


class GridMap:
    # This function runs when a new GridMap object is created.
    def __init__(self, rows=15, columns=20):
        # Save the number of rows.
        self.rows = rows
        # Save the number of columns.
        self.columns = columns
        # Make a new empty grid filled with zeroes.
        self.grid = [[0 for _ in range(columns)] for _ in range(rows)]
        # Start is empty until the user chooses a start cell.
        self.start = None
        # Goal is empty until the user chooses a destination cell.
        self.goal = None

    # Make a completely new empty map.
    def new_map(self, rows, columns):
        # Save the new row count.
        self.rows = rows
        # Save the new column count.
        self.columns = columns
        # Build a fresh free-cell grid.
        self.grid = [[0 for _ in range(columns)] for _ in range(rows)]
        # Remove the old start point.
        self.start = None
        # Remove the old destination.
        self.goal = None

    # Check whether a row-column position is inside the map.
    def inside(self, row, column):
        # True means both row and column are within valid limits.
        return 0 <= row < self.rows and 0 <= column < self.columns

    # Add one obstacle to the map.
    def add_obstacle(self, row, column):
        # Only continue if the cell is inside the map.
        if self.inside(row, column):
            # Do not place an obstacle on the selected start point.
            if (row, column) == self.start:
                return False
            # Do not place an obstacle on the selected goal point.
            if (row, column) == self.goal:
                return False
            # Change the cell from free (0) to blocked (1).
            self.grid[row][column] = 1
            # Tell the caller that the change worked.
            return True
        # Tell the caller that the cell was not valid.
        return False

    # Remove one obstacle from the map.
    def remove_obstacle(self, row, column):
        # Only continue if the position is inside the map.
        if self.inside(row, column):
            # Change the cell to free (0).
            self.grid[row][column] = 0
            # Tell the caller that it worked.
            return True
        # The position was outside the grid.
        return False

    # Choose the robot's starting position.
    def set_start(self, row, column):
        # The cell must be inside the map and must not be an obstacle.
        if self.inside(row, column) and self.grid[row][column] == 0:
            # Save this position as the start.
            self.start = (row, column)
            # Tell the caller that it worked.
            return True
        # Otherwise, setting the start failed.
        return False

    # Choose the destination position.
    def set_goal(self, row, column):
        # The cell must be inside the map and must not be blocked.
        if self.inside(row, column) and self.grid[row][column] == 0:
            # Save the destination.
            self.goal = (row, column)
            # Tell the caller that it worked.
            return True
        # Otherwise, setting the destination failed.
        return False

    # Remove all obstacles while keeping the same grid size.
    def clear_obstacles(self):
        # Create a fresh grid full of free cells.
        self.grid = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

    # Save the whole map to a JSON file.
    def save(self, filename):
        # Put all important map information into one dictionary.
        data = {
            "rows": self.rows,
            "columns": self.columns,
            "grid": self.grid,
            "start": list(self.start) if self.start is not None else None,
            "goal": list(self.goal) if self.goal is not None else None,
        }
        # Open the file in write mode.
        with open(filename, "w", encoding="utf-8") as file:
            # Write the dictionary as easy-to-read JSON text.
            json.dump(data, file, indent=4)

    # Load a previously saved JSON map.
    def load(self, filename):
        # Open the selected file in read mode.
        with open(filename, "r", encoding="utf-8") as file:
            # Read JSON text and turn it back into a Python dictionary.
            data = json.load(file)
        # Read the saved grid.
        loaded_grid = data["grid"]
        # Basic safety check: the grid must contain at least one row.
        if not loaded_grid:
            raise ValueError("The saved map is empty.")
        # Find the number of rows from the loaded grid.
        loaded_rows = len(loaded_grid)
        # Find the number of columns from the first row.
        loaded_columns = len(loaded_grid[0])
        # Make sure every row has the same number of columns.
        if any(len(row) != loaded_columns for row in loaded_grid):
            raise ValueError("The saved map has uneven row sizes.")
        # Make sure every cell contains only 0 or 1.
        if any(cell not in (0, 1) for row in loaded_grid for cell in row):
            raise ValueError("Map cells must contain only 0 or 1.")
        # Save the checked map size.
        self.rows = loaded_rows
        # Save the checked column count.
        self.columns = loaded_columns
        # Save the loaded grid.
        self.grid = loaded_grid
        # Convert the saved start list back into a tuple if it exists.
        self.start = tuple(data["start"]) if data.get("start") is not None else None
        # Convert the saved goal list back into a tuple if it exists.
        self.goal = tuple(data["goal"]) if data.get("goal") is not None else None
