# ============================================================
# main.py
# Autonomous Robot for Indoor Navigation Using A* Search
# This program is made to be simple for a beginner to read.
# It uses only Python's built-in libraries.
# ============================================================

# tkinter makes windows, buttons, labels, and drawing areas.
import tkinter as tk
# These extra tkinter tools give us file boxes, pop-up messages, and input boxes.
from tkinter import filedialog, messagebox, simpledialog
# Import our map class from map_model.py.
from map_model import GridMap
# Import our A* search function from astar.py.
from astar import astar_search


# This class is the whole graphical robot simulator.
class RobotNavigationApp:
    # This function runs automatically when the app starts.
    def __init__(self, root):
        # Save the main tkinter window inside the object.
        self.root = root
        # Put a title at the top of the window.
        self.root.title("Autonomous Robot - A* Indoor Navigation")
        # Give the window a useful starting size.
        self.root.geometry("1100x760")
        # Do not allow the window to become too tiny.
        self.root.minsize(900, 650)

        # Create our first map with 15 rows and 20 columns.
        self.map = GridMap(15, 20)
        # This tells us what a mouse click should do right now.
        self.mode = "obstacle"
        # This list will store the final route found by A*.
        self.path = []
        # This list will store cells that A* checked while searching.
        self.explored = []
        # This list will store cells the robot has already travelled through.
        self.travelled = []
        # This number tells us where the robot currently is inside self.path.
        self.robot_index = 0
        # False means the robot is not moving right now.
        self.running = False
        # False means the robot is not paused right now.
        self.paused = False
        # We save the tkinter timer ID here so it can be cancelled later.
        self.timer_id = None
        # Each robot step waits this many milliseconds.
        self.step_delay = 300

        # Build all buttons and labels.
        self.build_controls()
        # Build the canvas where the map will be drawn.
        self.build_canvas()
        # Draw the first empty map.
        self.draw_grid()
        # Show a helpful first message.
        self.set_status("Ready. Choose a tool, then click a grid cell.")

    # Build the left control panel.
    def build_controls(self):
        # Make a frame to hold the controls.
        self.control_frame = tk.Frame(self.root, padx=10, pady=10)
        # Put the frame on the left side of the window.
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Add a project title label.
        title = tk.Label(self.control_frame, text="A* Robot Simulator", font=("Arial", 16, "bold"))
        # Show the title with some space below it.
        title.pack(pady=(0, 10))

        # Add a short instruction label.
        instruction = tk.Label(
            self.control_frame,
            text="Choose a tool below,\nthen click a cell on the map.",
            justify=tk.LEFT,
        )
        # Show the instruction.
        instruction.pack(pady=(0, 10))

        # Create the button used to choose obstacle-placement mode.
        tk.Button(self.control_frame, text="Add Obstacle", width=22, command=lambda: self.change_mode("obstacle")).pack(pady=2)
        # Create the button used to remove obstacles.
        tk.Button(self.control_frame, text="Remove Obstacle", width=22, command=lambda: self.change_mode("erase")).pack(pady=2)
        # Create the button used to select the start point.
        tk.Button(self.control_frame, text="Choose Start", width=22, command=lambda: self.change_mode("start")).pack(pady=2)
        # Create the button used to select the destination.
        tk.Button(self.control_frame, text="Choose Destination", width=22, command=lambda: self.change_mode("goal")).pack(pady=2)

        # Add a small divider line.
        tk.Frame(self.control_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

        # Create a button that runs A* but does not move the robot yet.
        tk.Button(self.control_frame, text="Find A* Path", width=22, command=self.find_path).pack(pady=2)
        # Create a button that finds a path and starts robot movement.
        tk.Button(self.control_frame, text="Run Robot", width=22, command=self.run_robot).pack(pady=2)
        # Create a button that pauses or continues the robot.
        self.pause_button = tk.Button(self.control_frame, text="Pause", width=22, command=self.toggle_pause)
        # Show the pause button.
        self.pause_button.pack(pady=2)
        # Create a button that stops the current movement.
        tk.Button(self.control_frame, text="Stop", width=22, command=self.stop_robot).pack(pady=2)

        # Add another divider line.
        tk.Frame(self.control_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

        # Create a button for a completely new map.
        tk.Button(self.control_frame, text="New Map / Grid Size", width=22, command=self.new_map).pack(pady=2)
        # Create a button for saving the map.
        tk.Button(self.control_frame, text="Save Map", width=22, command=self.save_map).pack(pady=2)
        # Create a button for loading a saved map.
        tk.Button(self.control_frame, text="Load Map", width=22, command=self.load_map).pack(pady=2)
        # Create a button that clears obstacles only.
        tk.Button(self.control_frame, text="Clear Obstacles", width=22, command=self.clear_obstacles).pack(pady=2)
        # Create a button that resets path/robot state but keeps the map.
        tk.Button(self.control_frame, text="Reset Simulation", width=22, command=self.reset_simulation).pack(pady=2)

        # Add a divider before the legend.
        tk.Frame(self.control_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

        # Explain the map colors in very simple words.
        legend_text = (
            "COLOR GUIDE\n"
            "White = Free cell (0)\n"
            "Black = Obstacle (1)\n"
            "Green = Start\n"
            "Red = Destination\n"
            "Light blue = Explored\n"
            "Yellow = Path\n"
            "Orange = Travelled\n"
            "Purple = Robot"
        )
        # Show the legend on the left.
        tk.Label(self.control_frame, text=legend_text, justify=tk.LEFT).pack(anchor="w")

        # Add a divider before the status message.
        tk.Frame(self.control_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

        # This StringVar lets us easily change the status label later.
        self.status_text = tk.StringVar()
        # Make the status label and allow it to wrap onto more than one line.
        self.status_label = tk.Label(self.control_frame, textvariable=self.status_text, wraplength=220, justify=tk.LEFT)
        # Show the status label.
        self.status_label.pack(anchor="w")

    # Build the map drawing area.
    def build_canvas(self):
        # Make a frame for the right side of the application.
        self.canvas_frame = tk.Frame(self.root, padx=10, pady=10)
        # Let this frame use all remaining window space.
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        # Create a white drawing canvas.
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", highlightthickness=1, highlightbackground="gray")
        # Let the canvas stretch with the window.
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # When the user clicks the canvas, run on_canvas_click().
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        # When the window size changes, redraw the grid to fit nicely.
        self.canvas.bind("<Configure>", lambda event: self.draw_grid())

    # Change what clicking a cell does.
    def change_mode(self, new_mode):
        # Save the selected mode.
        self.mode = new_mode
        # Make an easy sentence for the user.
        names = {
            "obstacle": "Add obstacle",
            "erase": "Remove obstacle",
            "start": "Choose start",
            "goal": "Choose destination",
        }
        # Show the selected tool in the status area.
        self.set_status("Tool selected: " + names[new_mode] + ". Now click a grid cell.")

    # Change the message shown in the status area.
    def set_status(self, message):
        # Put the new text inside our StringVar.
        self.status_text.set(message)

    # Find the size of each square cell so the map fits the canvas.
    def cell_geometry(self):
        # Get the current canvas width; 1 protects us before the window fully appears.
        canvas_width = max(self.canvas.winfo_width(), 1)
        # Get the current canvas height.
        canvas_height = max(self.canvas.winfo_height(), 1)
        # Divide width by the number of columns.
        cell_width = canvas_width / self.map.columns
        # Divide height by the number of rows.
        cell_height = canvas_height / self.map.rows
        # Return both sizes.
        return cell_width, cell_height

    # Decide which color one cell should have.
    def get_cell_color(self, position):
        # Read row and column from the position tuple.
        row, column = position
        # If this is the robot's current cell, use purple first.
        if self.path and 0 <= self.robot_index < len(self.path) and position == self.path[self.robot_index]:
            return "purple"
        # If the robot already travelled through it, use orange.
        if position in self.travelled:
            return "orange"
        # If this is the chosen start point, use green.
        if position == self.map.start:
            return "green"
        # If this is the destination, use red.
        if position == self.map.goal:
            return "red"
        # If the map stores 1 here, it is an obstacle.
        if self.map.grid[row][column] == 1:
            return "black"
        # If this cell belongs to the final path, use yellow.
        if position in self.path:
            return "yellow"
        # If A* explored the cell, use light blue.
        if position in self.explored:
            return "lightblue"
        # Otherwise the cell is free, so use white.
        return "white"

    # Draw the whole occupancy grid again.
    def draw_grid(self):
        # Remove all old drawings from the canvas.
        self.canvas.delete("all")
        # Find the size of each grid square.
        cell_width, cell_height = self.cell_geometry()
        # Go through every row.
        for row in range(self.map.rows):
            # Go through every column inside this row.
            for column in range(self.map.columns):
                # Find the left x coordinate of the square.
                x1 = column * cell_width
                # Find the top y coordinate of the square.
                y1 = row * cell_height
                # Find the right x coordinate.
                x2 = x1 + cell_width
                # Find the bottom y coordinate.
                y2 = y1 + cell_height
                # Ask which color this cell needs.
                color = self.get_cell_color((row, column))
                # Draw the square with its color and a gray border.
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                # Only draw 0/1 text when cells are large enough to read.
                if cell_width >= 25 and cell_height >= 25:
                    # Read the stored occupancy value.
                    value = self.map.grid[row][column]
                    # Use white text on black obstacles, otherwise dark text.
                    text_color = "white" if value == 1 else "gray20"
                    # Draw the occupancy number in the middle of the cell.
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(value), fill=text_color)

    # Convert a mouse click into a grid row and column.
    def click_to_cell(self, mouse_x, mouse_y):
        # Get cell width and height.
        cell_width, cell_height = self.cell_geometry()
        # Find the clicked column by dividing x by cell width.
        column = int(mouse_x / cell_width)
        # Find the clicked row by dividing y by cell height.
        row = int(mouse_y / cell_height)
        # Return the row and column.
        return row, column

    # Run whenever the user clicks a grid cell.
    def on_canvas_click(self, event):
        # Convert mouse coordinates into grid coordinates.
        row, column = self.click_to_cell(event.x, event.y)
        # Ignore clicks outside the real grid.
        if not self.map.inside(row, column):
            return
        # Save the clicked position as a tuple.
        position = (row, column)

        # If the user chose obstacle mode, add an obstacle.
        if self.mode == "obstacle":
            # Try to add the obstacle.
            changed = self.map.add_obstacle(row, column)
            # If the obstacle was added, tell the user.
            if changed:
                self.set_status(f"Obstacle added at row {row}, column {column}.")
                # A map change may make an old path wrong, so clear the old path display.
                if not self.running:
                    self.clear_path_display()
                # If the robot is moving, a new obstacle is a dynamic obstacle.
                if self.running:
                    self.handle_dynamic_obstacle(position)
            # If it failed, the cell may be start or destination.
            else:
                self.set_status("Cannot put an obstacle on the start or destination cell.")

        # If the user chose erase mode, remove an obstacle.
        elif self.mode == "erase":
            # Make the cell free again.
            self.map.remove_obstacle(row, column)
            # Clear old search drawings because the map changed.
            if not self.running:
                self.clear_path_display()
            # Tell the user what happened.
            self.set_status(f"Cell ({row}, {column}) is now free.")

        # If the user chose start mode, set the start point.
        elif self.mode == "start":
            # Try to set this free cell as start.
            if self.map.set_start(row, column):
                # Reset robot/path information because the start changed.
                self.reset_simulation(quiet=True)
                # Tell the user the selected start.
                self.set_status(f"Start selected at row {row}, column {column}.")
            else:
                # Explain why it failed.
                self.set_status("Start must be on a free cell, not an obstacle.")

        # If the user chose destination mode, set the goal point.
        elif self.mode == "goal":
            # Try to set this free cell as destination.
            if self.map.set_goal(row, column):
                # Reset the old path because the destination changed.
                self.reset_simulation(quiet=True)
                # Tell the user the selected destination.
                self.set_status(f"Destination selected at row {row}, column {column}.")
            else:
                # Explain the problem.
                self.set_status("Destination must be on a free cell, not an obstacle.")

        # Redraw the map so the user sees the change immediately.
        self.draw_grid()

    # Clear only the path-related drawings and data.
    def clear_path_display(self):
        # Remove the final path list.
        self.path = []
        # Remove explored-cell information.
        self.explored = []
        # Remove travelled-cell information.
        self.travelled = []
        # Move robot index back to the beginning.
        self.robot_index = 0

    # Run the A* algorithm and display its answer.
    def find_path(self):
        # We need both a start and a destination first.
        if self.map.start is None or self.map.goal is None:
            # Show an easy warning pop-up.
            messagebox.showwarning("Missing Points", "Please choose both START and DESTINATION first.")
            # Stop this function here.
            return False
        # Ask A* to search this map.
        path, explored = astar_search(self.map.grid, self.map.start, self.map.goal)
        # Save all explored cells for visualization.
        self.explored = explored
        # Save the final route.
        self.path = path
        # Clear previous travelled cells.
        self.travelled = []
        # Put the virtual robot at the first path cell.
        self.robot_index = 0
        # Redraw everything to show explored cells and path.
        self.draw_grid()
        # If A* returned no path, explain it.
        if not path:
            self.set_status("No safe path exists. Try removing some obstacles.")
            # Tell other functions that search failed.
            return False
        # Calculate number of moves; path includes the starting cell.
        number_of_moves = len(path) - 1
        # Show the successful result.
        self.set_status(f"A* found a safe path with {number_of_moves} moves.")
        # Tell other functions that the search worked.
        return True

    # Find a path and start moving the virtual robot.
    def run_robot(self):
        # Stop an old timer if one exists.
        self.cancel_timer()
        # Find a fresh path from the selected start to destination.
        if not self.find_path():
            return
        # The robot is now running.
        self.running = True
        # It starts in an unpaused state.
        self.paused = False
        # Make sure the button says Pause.
        self.pause_button.config(text="Pause")
        # Tell the user what is happening.
        self.set_status("Robot is moving. You may add a NEW obstacle while it moves.")
        # Start the first timed robot step.
        self.schedule_next_step()

    # Ask tkinter to call move_one_step after a short delay.
    def schedule_next_step(self):
        # Only schedule movement when running and not paused.
        if self.running and not self.paused:
            # Save the timer ID so we can cancel it if needed.
            self.timer_id = self.root.after(self.step_delay, self.move_one_step)

    # Move the virtual robot forward by exactly one path cell.
    def move_one_step(self):
        # This timer has now fired, so clear its saved ID.
        self.timer_id = None
        # Stop if the robot is no longer running.
        if not self.running:
            return
        # Stop here if the user paused the robot.
        if self.paused:
            return
        # If robot is already on the final path cell, finish.
        if self.robot_index >= len(self.path) - 1:
            self.finish_robot()
            return
        # Remember the cell the robot is leaving.
        old_position = self.path[self.robot_index]
        # Add it to travelled cells if it is not already there.
        if old_position not in self.travelled:
            self.travelled.append(old_position)
        # Move the robot index forward by one.
        self.robot_index += 1
        # Read the robot's new cell.
        current_position = self.path[self.robot_index]
        # Redraw the map to show the movement.
        self.draw_grid()
        # Show the current robot position in the status message.
        self.set_status(f"Robot moved to row {current_position[0]}, column {current_position[1]}.")
        # If we reached the destination, finish now.
        if current_position == self.map.goal:
            self.finish_robot()
            return
        # Otherwise schedule the next step.
        self.schedule_next_step()

    # Finish the movement when the robot reaches the destination.
    def finish_robot(self):
        # Mark the simulator as no longer running.
        self.running = False
        # Mark it as not paused.
        self.paused = False
        # Make the button label normal again.
        self.pause_button.config(text="Pause")
        # Redraw one final time.
        self.draw_grid()
        # Tell the user the robot succeeded.
        self.set_status("Success! The virtual robot reached the destination.")

    # Add a dynamic obstacle while the robot is moving.
    def handle_dynamic_obstacle(self, obstacle_position):
        # Find the robot's current position on the old path.
        current_position = self.path[self.robot_index]
        # Look only at the route still ahead of the robot.
        remaining_route = self.path[self.robot_index + 1:]
        # If the new obstacle is not on the remaining route, no replanning is needed.
        if obstacle_position not in remaining_route:
            self.set_status("Dynamic obstacle added. It does not block the current route.")
            return
        # Tell the user that the current route was blocked.
        self.set_status("Dynamic obstacle blocks the route. A* is finding a new path...")
        # Run A* again, starting from the robot's current cell.
        new_path, new_explored = astar_search(self.map.grid, current_position, self.map.goal)
        # Save the latest explored cells.
        self.explored = new_explored
        # If no new route exists, stop the robot safely.
        if not new_path:
            # Cancel any old movement timer.
            self.cancel_timer()
            # Mark the robot as stopped.
            self.running = False
            # Clear the final route because there is no route now.
            self.path = []
            # Reset robot index because path is empty.
            self.robot_index = 0
            # Redraw the map.
            self.draw_grid()
            # Explain the result.
            self.set_status("Robot stopped: the new obstacle leaves no safe route.")
            return
        # Replace the old route with the newly calculated route.
        self.path = new_path
        # Put robot at index 0 because new_path starts at its current position.
        self.robot_index = 0
        # Redraw to show the changed route.
        self.draw_grid()
        # Tell the user replanning worked.
        self.set_status("A* created a new route around the dynamic obstacle.")

    # Pause or continue the robot.
    def toggle_pause(self):
        # If the robot is not running, there is nothing to pause.
        if not self.running:
            self.set_status("The robot is not running yet.")
            return
        # If the robot is currently moving, pause it.
        if not self.paused:
            # Mark it paused.
            self.paused = True
            # Cancel the waiting movement timer.
            self.cancel_timer()
            # Change button text so the user knows it can continue.
            self.pause_button.config(text="Continue")
            # Show status.
            self.set_status("Robot paused.")
        # Otherwise the robot is paused, so continue it.
        else:
            # Mark it unpaused.
            self.paused = False
            # Change the button text back.
            self.pause_button.config(text="Pause")
            # Show status.
            self.set_status("Robot continued.")
            # Schedule the next movement.
            self.schedule_next_step()

    # Stop robot movement but keep the map visible.
    def stop_robot(self):
        # Cancel any waiting timer.
        self.cancel_timer()
        # Mark the robot as stopped.
        self.running = False
        # Remove pause state.
        self.paused = False
        # Reset button text.
        self.pause_button.config(text="Pause")
        # Tell the user it stopped.
        self.set_status("Robot stopped.")

    # Safely cancel a tkinter timer.
    def cancel_timer(self):
        # Only try to cancel when a timer actually exists.
        if self.timer_id is not None:
            # Ask tkinter to cancel that scheduled call.
            self.root.after_cancel(self.timer_id)
            # Clear the saved timer ID.
            self.timer_id = None

    # Ask for a new grid size and create a new map.
    def new_map(self):
        # Ask the user for row count.
        rows = simpledialog.askinteger("New Map", "How many rows? (5 to 40)", initialvalue=self.map.rows, minvalue=5, maxvalue=40)
        # If Cancel was pressed, stop here.
        if rows is None:
            return
        # Ask for column count.
        columns = simpledialog.askinteger("New Map", "How many columns? (5 to 50)", initialvalue=self.map.columns, minvalue=5, maxvalue=50)
        # If Cancel was pressed, stop here.
        if columns is None:
            return
        # Stop any old simulation.
        self.cancel_timer()
        # Build the fresh map.
        self.map.new_map(rows, columns)
        # Reset simulation data.
        self.clear_path_display()
        # Mark robot stopped.
        self.running = False
        # Redraw the new empty grid.
        self.draw_grid()
        # Tell the user the size.
        self.set_status(f"New empty map created: {rows} rows x {columns} columns.")

    # Save the map into a JSON file chosen by the user.
    def save_map(self):
        # Open a Save As window.
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Map", "*.json")],
            title="Save Occupancy Grid",
        )
        # If the user cancelled, stop here.
        if not filename:
            return
        # Try to save the map.
        try:
            # Ask GridMap to write the JSON file.
            self.map.save(filename)
            # Show success.
            self.set_status("Map saved successfully.")
        # If something goes wrong, show the error instead of crashing.
        except Exception as error:
            # Show a pop-up with the problem.
            messagebox.showerror("Save Error", str(error))

    # Load a JSON map chosen by the user.
    def load_map(self):
        # Open a file selection window.
        filename = filedialog.askopenfilename(
            filetypes=[("JSON Map", "*.json"), ("All Files", "*.*")],
            title="Load Occupancy Grid",
        )
        # If no file was chosen, stop here.
        if not filename:
            return
        # Stop the old simulation first.
        self.cancel_timer()
        # Try loading the map.
        try:
            # Ask GridMap to read the selected file.
            self.map.load(filename)
            # Clear old path and robot drawings.
            self.clear_path_display()
            # Mark robot stopped.
            self.running = False
            # Redraw the loaded map.
            self.draw_grid()
            # Show success.
            self.set_status("Map loaded successfully.")
        # If the file is bad, show the problem.
        except Exception as error:
            # Display a friendly error pop-up.
            messagebox.showerror("Load Error", str(error))

    # Remove all obstacle cells but keep start and destination.
    def clear_obstacles(self):
        # Stop movement first.
        self.stop_robot()
        # Make every occupancy-grid cell equal to 0.
        self.map.clear_obstacles()
        # Clear the old route and search drawings.
        self.clear_path_display()
        # Draw the clean map.
        self.draw_grid()
        # Explain what changed.
        self.set_status("All obstacles were removed. Start and destination were kept.")

    # Reset only the simulation state; keep map, obstacles, start, and destination.
    def reset_simulation(self, quiet=False):
        # Cancel robot movement if it is active.
        self.cancel_timer()
        # Mark the robot stopped.
        self.running = False
        # Remove pause state.
        self.paused = False
        # Reset pause button text.
        self.pause_button.config(text="Pause")
        # Clear path, explored cells, travelled cells, and robot index.
        self.clear_path_display()
        # Redraw the unchanged map.
        self.draw_grid()
        # Only show a message when quiet is False.
        if not quiet:
            # Explain what reset means.
            self.set_status("Simulation reset. The map, obstacles, start, and destination are still saved on screen.")


# This special check means: run the GUI only when main.py is started directly.
if __name__ == "__main__":
    # Create the main tkinter window.
    root = tk.Tk()
    # Create our robot simulator inside that window.
    app = RobotNavigationApp(root)
    # Keep the window open and listen for clicks and buttons.
    root.mainloop()
