# This file runs small automatic tests without opening the GUI.
# It helps us check that the map and A* logic work correctly.

# Import our map class.
from map_model import GridMap
# Import our A* algorithm.
from astar import astar_search

# Make a simple 5 x 5 map.
test_map = GridMap(5, 5)
# Put the start at the top-left corner.
test_map.set_start(0, 0)
# Put the destination at the bottom-right corner.
test_map.set_goal(4, 4)
# Build a small wall with one opening.
test_map.add_obstacle(1, 0)
test_map.add_obstacle(1, 1)
test_map.add_obstacle(1, 2)
test_map.add_obstacle(1, 3)
# Ask A* to find a safe route.
path, explored = astar_search(test_map.grid, test_map.start, test_map.goal)
# The path should begin at the start.
assert path[0] == (0, 0)
# The path should finish at the destination.
assert path[-1] == (4, 4)
# No path cell should be an obstacle.
assert all(test_map.grid[row][column] == 0 for row, column in path)
# Print a success message when every test passes.
print("All automatic tests passed.")
# Show the path so a beginner can see the answer.
print("Test path:", path)
# Show how many cells A* explored.
print("Explored cells:", len(explored))
