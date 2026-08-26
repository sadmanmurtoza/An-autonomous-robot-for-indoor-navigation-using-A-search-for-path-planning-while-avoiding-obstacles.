# Simple non-GUI integration test for all core modules.
from map_model import GridMap
from astar import AStarPlanner
from virtual_robot import VirtualRobot


def run_tests():
    # Create member objects.
    grid_map = GridMap(5, 5)
    planner = AStarPlanner()
    robot = VirtualRobot()

    # Add a small obstacle wall with a gap.
    grid_map.add_obstacle(1, 1)
    grid_map.add_obstacle(1, 2)
    grid_map.add_obstacle(1, 3)

    # Select start and goal.
    grid_map.set_start(0, 0)
    grid_map.set_goal(4, 4)

    # Member 2 finds a path.
    result = planner.find_path(grid_map.grid, grid_map.start, grid_map.goal)
    assert result["success"], "A* should find a path."
    assert planner.validate_path(grid_map.grid, result["path"]), "Path should be valid."

    # Member 3 loads it.
    assert robot.load_path(result["path"]), "Robot should accept path."
    assert robot.start(), "Robot should start."

    # Move one step.
    state = robot.step(grid_map.grid)
    assert state in ("moved", "finished"), "Robot should move safely."

    # If there is another remaining cell, block it dynamically.
    if robot.remaining:
        block_row, block_col = robot.remaining[0]
        grid_map.add_obstacle(block_row, block_col)
        state = robot.step(grid_map.grid)
        assert state == "blocked", "Robot should detect a dynamic obstacle."

        # Member 2 replans from current robot position.
        replan = planner.replan(grid_map.grid, robot.current_position, grid_map.goal)
        if replan["success"]:
            assert robot.apply_replanned_path(replan["path"]), "Robot should accept new route."

    print("ALL CORE INTEGRATION TESTS PASSED")


if __name__ == "__main__":
    run_tests()
