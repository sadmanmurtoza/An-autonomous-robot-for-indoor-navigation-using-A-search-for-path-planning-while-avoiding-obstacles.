"""Virtual robot movement and dynamic replanning module.

Owner: Fahima Shameem (Member 3)

Scope of this file (per the Week 1-7 work plan):
- Follow a path produced by the A* module cell by cell.
- Track the robot's current position and the cells travelled / remaining.
- Detect when the next cell on the path has just become blocked, and
  trigger a fresh search from the robot's current position.
- React to Run, Pause, Clear Grid, and Reset controls without corrupting
  the robot's position or the remaining path.

This file deliberately does NOT:
- Implement A* search itself (that's support/astar.py, owned by Sadman).
- Define or store the occupancy grid (that's occupancy_grid.py, owned by
  Asraful). We only *use* OccupancyGrid from that module.
- Draw anything on screen (that's gui.py, also Asraful's).

Until support/astar.py is pushed to the repo, `placeholder_bfs_planner`
below stands in for it so this module can be built and tested on its own.
Swap it out later for the real function -- see "Wiring in the real A*"
at the bottom of this file.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional

from occupancy_grid import OccupancyGrid

Position = tuple[int, int]

# A planner is any callable matching this shape: given the grid, a start
# cell, and a goal cell, return an ordered list of (row, col) cells from
# start to goal inclusive, or None/[] if no path exists.
PlannerFn = Callable[[OccupancyGrid, Position, Position], Optional[list[Position]]]


class RobotStatus(Enum):
    IDLE = "idle"                 # no path loaded, or loaded but not started
    RUNNING = "running"           # actively stepping along the path
    PAUSED = "paused"             # stopped mid-route, resumable
    REPLANNING = "replanning"     # momentary state while planner() runs
    ARRIVED = "arrived"           # reached the goal cell
    NO_PATH = "no_path"           # replanning failed to find a route


class RobotError(RuntimeError):
    """Raised when the robot is asked to do something invalid."""


def placeholder_bfs_planner(
    grid: OccupancyGrid, start: Position, goal: Position
) -> Optional[list[Position]]:
    """Minimal BFS pathfinder -- a stand-in for support/astar.py.

    Use this ONLY until the real A* function is available. It matches the
    exact signature the real one should have: planner(grid, start, goal)
    -> path or None. Swap the reference in VirtualRobot.planner once
    Sadman's module is pushed; nothing else in this file needs to change.
    """
    if start == goal:
        return [start]

    visited = {start}
    queue: deque[list[Position]] = deque([[start]])

    while queue:
        path = queue.popleft()
        row, col = path[-1]
        for d_row, d_col in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            n_row, n_col = row + d_row, col + d_col
            if not grid.in_bounds(n_row, n_col):
                continue
            if grid.is_blocked(n_row, n_col):
                continue
            next_cell = (n_row, n_col)
            if next_cell in visited:
                continue
            new_path = path + [next_cell]
            if next_cell == goal:
                return new_path
            visited.add(next_cell)
            queue.append(new_path)

    return None


@dataclass
class VirtualRobot:
    """Owns the robot's own moving state -- nothing about the grid itself."""

    grid: OccupancyGrid
    planner: PlannerFn = placeholder_bfs_planner
    status: RobotStatus = RobotStatus.IDLE
    path: list[Position] = field(default_factory=list)
    travelled: list[Position] = field(default_factory=list)
    step_index: int = 0
    replan_count: int = 0

    # ---- setup -----------------------------------------------------

    def load_path(self, path: list[Position]) -> None:
        """Accept a freshly computed path from the A* module."""
        if not path:
            raise RobotError("Cannot load an empty path.")
        for cell in path:
            if not self.grid.in_bounds(*cell):
                raise RobotError(f"Path cell {cell} is outside the grid.")
            if self.grid.is_blocked(*cell):
                raise RobotError(f"Path cell {cell} is blocked.")

        self.path = list(path)
        self.travelled = [self.path[0]]
        self.step_index = 0
        self.replan_count = 0
        self.status = RobotStatus.IDLE

    # ---- read-only state for the interface to display ---------------

    @property
    def current_position(self) -> Optional[Position]:
        return self.travelled[-1] if self.travelled else None

    @property
    def remaining_path(self) -> list[Position]:
        """Cells from the current position to the goal, inclusive."""
        return self.path[self.step_index:]

    @property
    def is_at_goal(self) -> bool:
        return self.status == RobotStatus.ARRIVED

    # ---- controls the interface (Run / Pause / Clear Grid / Reset) --

    def run(self) -> None:
        """Start, or resume from a pause."""
        if not self.path:
            raise RobotError("No path loaded. Call load_path() first.")
        if self.status == RobotStatus.ARRIVED:
            return
        self.status = RobotStatus.RUNNING

    def pause(self) -> None:
        """Stop mid-route without losing position or remaining path."""
        if self.status == RobotStatus.RUNNING:
            self.status = RobotStatus.PAUSED

    def reset(self) -> None:
        """Send the robot back to the start of its CURRENT path."""
        if self.path:
            self.travelled = [self.path[0]]
            self.step_index = 0
        self.replan_count = 0
        self.status = RobotStatus.IDLE

    def clear(self) -> None:
        """Full reset for 'Clear Grid': drop the path entirely."""
        self.path = []
        self.travelled = []
        self.step_index = 0
        self.replan_count = 0
        self.status = RobotStatus.IDLE

    # ---- core movement ----------------------------------------------

    def step(self) -> bool:
        """Advance exactly one cell along the path.

        Call this repeatedly from a timer/loop with a short delay between
        calls, per the work plan's "short delay between steps so the
        motion is visible." Returns True if the robot moved or replanned,
        False if paused/idle/arrived/stuck.
        """
        if self.status != RobotStatus.RUNNING:
            return False

        if self.step_index >= len(self.path) - 1:
            self.status = RobotStatus.ARRIVED
            return False

        next_cell = self.path[self.step_index + 1]

        if self.grid.is_blocked(*next_cell):
            return self._replan()

        self.step_index += 1
        self.travelled.append(next_cell)
        if self.step_index == len(self.path) - 1:
            self.status = RobotStatus.ARRIVED
        return True

    def notify_obstacle_added(self, cell: Position) -> bool:
        """Call this whenever the grid/GUI module reports a new obstacle.

        Only triggers a replan if the new obstacle actually sits on the
        part of the path still ahead of the robot.
        """
        upcoming = self.path[self.step_index + 1:]
        if cell in upcoming:
            return self._replan()
        return False

    def _replan(self) -> bool:
        current = self.current_position
        if current is None or not self.path:
            self.status = RobotStatus.NO_PATH
            return False

        goal = self.path[-1]
        self.status = RobotStatus.REPLANNING
        new_path = self.planner(self.grid, current, goal)
        self.replan_count += 1

        if not new_path:
            self.status = RobotStatus.NO_PATH
            return False

        # Keep everything already travelled, splice in the fresh route
        # from the current cell onward.
        self.path = self.path[: self.step_index] + new_path
        self.status = RobotStatus.RUNNING
        return True


# ---------------------------------------------------------------------
# Wiring in the real A* once support/astar.py exists:
#
#   from support.astar import astar
#   robot = VirtualRobot(grid=my_grid, planner=astar)
#
# As long as astar(grid, start, goal) returns a list of (row, col) tuples
# or None, nothing else in this file needs to change.
# ---------------------------------------------------------------------
