# ============================================================
# member3_fahima_robot.py
# Member 3 work: Virtual Robot and Dynamic Replanning
#
# This file controls the robot's changing state.
# It does NOT draw the GUI by itself.
# The GUI asks this robot to move one step at a time.
# ============================================================


# This class represents our virtual robot.
class VirtualRobot:

    # This function creates a fresh robot.
    def __init__(self):
        # Current position starts as empty.
        self.current_position = None
        # Full current route starts empty.
        self.path = []
        # Travelled cells start empty.
        self.travelled = []
        # Remaining cells start empty.
        self.remaining = []
        # False means the robot is not running.
        self.running = False
        # False means the robot is not paused.
        self.paused = False
        # This remembers whether the robot has reached the goal.
        self.finished = False
        # This stores a human-readable robot message.
        self.message = "Robot is ready."

    # Give the robot a new path produced by A*.
    def load_path(self, path):
        # Make a copy so outside code cannot accidentally change our list.
        self.path = list(path)

        # If the path is empty, the robot cannot move.
        if not self.path:
            # Clear current position.
            self.current_position = None
            # Clear travelled cells.
            self.travelled = []
            # Clear remaining cells.
            self.remaining = []
            # Stop running.
            self.running = False
            # Mark not finished because no goal was reached.
            self.finished = False
            # Explain what happened.
            self.message = "Robot has no path to follow."
            # Tell caller that loading failed.
            return False

        # Robot begins at the first cell in the path.
        self.current_position = self.path[0]
        # The starting cell counts as already visited.
        self.travelled = [self.current_position]
        # All later cells are still remaining.
        self.remaining = self.path[1:]
        # Robot is prepared but not moving until start() is called.
        self.running = False
        # Robot is not paused yet.
        self.paused = False
        # Robot has not finished yet unless path has only one cell.
        self.finished = len(self.path) == 1
        # Update the message.
        self.message = "Path loaded. Robot is ready to move."
        # Tell caller loading worked.
        return True

    # Start or resume movement.
    def start(self):
        # Robot needs a current position first.
        if self.current_position is None:
            self.message = "Cannot run because no path is loaded."
            return False

        # If already finished, there is nothing to move through.
        if self.finished:
            self.message = "Robot is already at the destination."
            return False

        # Mark robot as running.
        self.running = True
        # Make sure pause is off.
        self.paused = False
        # Update message.
        self.message = "Robot is moving."
        # Tell caller it worked.
        return True

    # Pause the robot without losing its position.
    def pause(self):
        # Only pause when it is running.
        if self.running:
            # Set pause state.
            self.paused = True
            # Update message.
            self.message = "Robot is paused."
            # Tell caller it worked.
            return True

        # Otherwise nothing changed.
        return False

    # Continue after a pause.
    def resume(self):
        # Robot must still be running and paused.
        if self.running and self.paused:
            # Turn pause off.
            self.paused = False
            # Update message.
            self.message = "Robot resumed."
            # Tell caller it worked.
            return True

        # Otherwise nothing changed.
        return False

    # Stop movement but keep the current robot position.
    def stop(self):
        # Turn running off.
        self.running = False
        # Turn pause off.
        self.paused = False
        # Update message.
        self.message = "Robot stopped."

    # Reset all robot information.
    def reset(self):
        # Remove position.
        self.current_position = None
        # Remove route.
        self.path = []
        # Remove travelled history.
        self.travelled = []
        # Remove remaining route.
        self.remaining = []
        # Stop robot.
        self.running = False
        # Remove pause.
        self.paused = False
        # Remove finished state.
        self.finished = False
        # Update message.
        self.message = "Robot reset."

    # Check whether the robot's NEXT planned cell became blocked.
    def next_cell_is_blocked(self, grid):
        # If no cells remain, there is nothing to check.
        if not self.remaining:
            return False

        # Look at only the next cell.
        next_row, next_col = self.remaining[0]

        # A 1 means obstacle.
        return grid[next_row][next_col] == 1

    # Replace the old remaining route with a newly replanned route.
    def apply_replanned_path(self, new_path):
        # A useful new path must exist.
        if not new_path:
            # Stop the robot because destination became unreachable.
            self.running = False
            # Turn pause off.
            self.paused = False
            # Remove remaining route.
            self.remaining = []
            # Explain the failure.
            self.message = "Destination is unreachable after the new obstacle."
            # Tell caller replanning failed.
            return False

        # The first cell should be the robot's CURRENT position.
        if new_path[0] != self.current_position:
            # Reject a route that begins somewhere else.
            self.message = "Replanned path does not start at the robot's current cell."
            return False

        # Save the new full route from current position to goal.
        self.path = list(new_path)
        # The first cell is current, so only later cells remain.
        self.remaining = self.path[1:]
        # Robot can continue moving.
        self.running = True
        # It should not be paused after a successful automatic replan.
        self.paused = False
        # It is not finished unless there is no remaining cell.
        self.finished = len(self.remaining) == 0
        # Update message.
        self.message = "New route accepted. Robot will continue."
        # Tell caller success.
        return True

    # Move exactly ONE cell.
    # The GUI calls this repeatedly with a small delay.
    def step(self, grid):
        # Do not move if robot is not running.
        if not self.running:
            return "stopped"

        # Do not move while paused.
        if self.paused:
            return "paused"

        # If no cells remain, robot already reached the destination.
        if not self.remaining:
            # Stop running.
            self.running = False
            # Mark finished.
            self.finished = True
            # Update message.
            self.message = "Robot reached the destination."
            # Tell GUI the trip finished.
            return "finished"

        # Read next planned cell.
        next_row, next_col = self.remaining[0]

        # Safety check: never move into a blocked cell.
        if grid[next_row][next_col] == 1:
            # Keep the robot exactly where it is.
            self.message = "Next cell became blocked. Replanning is needed."
            # Tell GUI it must call A* again.
            return "blocked"

        # Move robot to the next cell.
        self.current_position = self.remaining.pop(0)

        # Save the moved-to cell in travelled history.
        if self.current_position not in self.travelled:
            self.travelled.append(self.current_position)

        # If nothing remains now, robot reached the destination.
        if not self.remaining:
            # Stop running.
            self.running = False
            # Mark finished.
            self.finished = True
            # Update message.
            self.message = "Robot reached the destination."
            # Tell GUI finished.
            return "finished"

        # Otherwise movement was one normal step.
        self.message = "Robot moved one cell."
        # Tell GUI to schedule another step.
        return "moved"
