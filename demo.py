"""Standalone demo/test for robot.py.

Run this directly (`python demo_robot.py`) to see:
  1. A path computed and loaded onto the virtual robot.
  2. Normal step-by-step movement with travelled/remaining cells shown.
  3. Pause -> Run resuming cleanly without losing position.
  4. A NEW obstacle dropped onto the upcoming path mid-route, triggering
     an automatic replan.
  5. Reset and Clear behaving as separate controls.
  6. An unreachable-goal case reported cleanly (no crash).

This does not depend on support/astar.py -- it uses the placeholder BFS
planner in robot.py so it can be run and tested right now.
"""

from occupancy_grid import OccupancyGrid
from robot import VirtualRobot, RobotStatus, placeholder_bfs_planner


def print_state(robot: VirtualRobot, label: str) -> None:
    print(f"[{label}] status={robot.status.value} "
          f"pos={robot.current_position} "
          f"travelled={robot.travelled} "
          f"remaining={robot.remaining_path} "
          f"replans={robot.replan_count}")


def scenario_normal_run_with_dynamic_obstacle() -> None:
    print("\n=== Scenario 1: normal run + dynamic obstacle mid-route ===")

    grid = OccupancyGrid.create_empty(5, 5)
    grid.set_start(0, 0)
    grid.set_destination(4, 4)

    path = placeholder_bfs_planner(grid, grid.start, grid.destination)
    assert path is not None, "Expected a path on an empty 5x5 grid."

    robot = VirtualRobot(grid=grid, planner=placeholder_bfs_planner)
    robot.load_path(path)
    print_state(robot, "loaded")

    robot.run()
    for _ in range(2):
        robot.step()
        print_state(robot, "step")

    # Pause mid-route, confirm position/remaining path are untouched.
    robot.pause()
    print_state(robot, "paused")
    robot.step()  # should be a no-op while paused
    print_state(robot, "still paused (no-op step)")

    # Resume, then drop a NEW obstacle onto the still-ahead part of the path.
    robot.run()
    blocked_cell = robot.remaining_path[1]
    grid.set_obstacle(*blocked_cell)
    robot.notify_obstacle_added(blocked_cell)
    print_state(robot, f"after obstacle at {blocked_cell} -> replanned")

    # Run to completion.
    while robot.status == RobotStatus.RUNNING:
        robot.step()
    print_state(robot, "final")


def scenario_reset_vs_clear() -> None:
    print("\n=== Scenario 2: Reset vs Clear Grid controls ===")

    grid = OccupancyGrid.create_empty(4, 4)
    grid.set_start(0, 0)
    grid.set_destination(3, 3)
    path = placeholder_bfs_planner(grid, grid.start, grid.destination)

    robot = VirtualRobot(grid=grid, planner=placeholder_bfs_planner)
    robot.load_path(path)
    robot.run()
    robot.step()
    robot.step()
    print_state(robot, "mid-route")

    robot.reset()
    print_state(robot, "after reset (same path, back to start)")

    robot.clear()
    print_state(robot, "after clear (path dropped entirely)")


def scenario_unreachable_goal() -> None:
    print("\n=== Scenario 3: unreachable goal handled cleanly ===")

    grid = OccupancyGrid.create_empty(3, 3)
    # Wall off the destination completely.
    grid.set_obstacle(0, 2)
    grid.set_obstacle(1, 2)
    grid.set_start(0, 0)
    grid.set_destination(2, 2)
    grid.set_obstacle(2, 1)

    path = placeholder_bfs_planner(grid, grid.start, grid.destination)
    print(f"Planner result for an unreachable goal: {path}")


if __name__ == "__main__":
    scenario_normal_run_with_dynamic_obstacle()
    scenario_reset_vs_clear()
    scenario_unreachable_goal()
