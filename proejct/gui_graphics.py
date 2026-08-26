# ============================================================
# member4_gui_graphics.py
# Member 4 work: GUI, System Testing, Warnings, Documentation UI
#
# This file creates the window that the user can click.
# It connects the map, A* planner, and virtual robot.
# ============================================================

# tkinter is Python's built-in window-making library.
import tkinter as tk

# These give us pop-up boxes and file chooser windows.
from tkinter import filedialog, messagebox, simpledialog

# Simple color theme. Keeping colors in one place makes them easy to memorize.
COLORS = {
    "window": "#0F172A",
    "panel": "#111827",
    "card": "#1E293B",
    "free": "#F8FAFC",
    "grid": "#CBD5E1",
    "obstacle": "#334155",
    "start": "#22C55E",
    "goal": "#EF4444",
    "explored": "#BAE6FD",
    "path": "#FDE047",
    "travelled": "#FB923C",
    "robot": "#8B5CF6",
    "text": "#F8FAFC",
    "muted": "#CBD5E1",
    "button": "#2563EB",
    "button_active": "#1D4ED8",
}


# This class creates the full graphical interface.
class RobotGUI:

    # The main program gives all other modules to this GUI.
    def __init__(self, root, grid_map, planner, robot):
        # Save the main window.
        self.root = root
        # Save Member 1's map object.
        self.map = grid_map
        # Save Member 2's A* planner object.
        self.planner = planner
        # Save Member 3's robot object.
        self.robot = robot

        # Set a title on the program window.
        self.root.title("Group 6 - Autonomous Indoor Navigation Robot")
        # Give the program a comfortable starting size.
        self.root.geometry("1180x780")
        # Prevent the window becoming too tiny.
        self.root.minsize(950, 650)
        self.root.configure(bg=COLORS["window"])

        # Apply one clean style to every normal Tkinter button.
        self.root.option_add("*Button.Background", COLORS["button"])
        self.root.option_add("*Button.Foreground", "white")
        self.root.option_add("*Button.ActiveBackground", COLORS["button_active"])
        self.root.option_add("*Button.ActiveForeground", "white")
        self.root.option_add("*Button.Relief", "flat")
        self.root.option_add("*Button.Cursor", "hand2")
        self.root.option_add("*Button.Font", ("Arial", 10, "bold"))

        # Mouse clicks will add obstacles at first.
        self.mode = "obstacle"
        # A* path starts empty.
        self.path = []
        # Explored cells start empty.
        self.explored = []
        # Save latest A* result information.
        self.last_result = None
        # Store Tkinter's timer ID here.
        self.timer_id = None
        # Delay between robot moves in milliseconds.
        self.step_delay = 350

        # Build all visible controls.
        self.build_controls()
        # Build the map drawing area.
        self.build_canvas()
        # Draw the first map.
        self.draw_grid()
        # Show a first status message.
        self.set_status("Ready. Choose Start and Destination, then run A*.")
        # Show blank performance information.
        self.update_performance(None)

    # Make the left-side button panel.
    def build_controls(self):
        # Create the left frame.
        self.control_frame = tk.Frame(
            self.root, bg=COLORS["panel"], padx=14, pady=14
        )
        # Put it on the left.
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Add the project title.
        tk.Label(
            self.control_frame,
            text="A* Robot Simulator",
            font=("Arial", 16, "bold"),
            bg=COLORS["panel"],
            fg=COLORS["text"],
        ).pack(pady=(0, 8))

        # Explain the basic click idea.
        tk.Label(
            self.control_frame,
            text="Choose a tool, then click a grid cell.",
            wraplength=230,
            justify=tk.LEFT,
            bg=COLORS["panel"],
            fg=COLORS["muted"],
        ).pack(pady=(0, 8))

        # Button for adding an obstacle.
        tk.Button(
            self.control_frame,
            text="Add Obstacle",
            width=24,
            command=lambda: self.change_mode("obstacle"),
        ).pack(pady=2)

        # Button for removing an obstacle.
        tk.Button(
            self.control_frame,
            text="Remove Obstacle",
            width=24,
            command=lambda: self.change_mode("erase"),
        ).pack(pady=2)

        # Button for selecting start.
        tk.Button(
            self.control_frame,
            text="Choose Start",
            width=24,
            command=lambda: self.change_mode("start"),
        ).pack(pady=2)

        # Button for selecting goal.
        tk.Button(
            self.control_frame,
            text="Choose Destination",
            width=24,
            command=lambda: self.change_mode("goal"),
        ).pack(pady=2)

        # Draw a divider.
        self.add_divider()

        # Button that calculates A* path only.
        tk.Button(
            self.control_frame,
            text="Find A* Path",
            width=24,
            command=self.find_path,
        ).pack(pady=2)

        # Button that starts the robot.
        tk.Button(
            self.control_frame,
            text="Run Robot",
            width=24,
            command=self.run_robot,
        ).pack(pady=2)

        # Pause/Resume button saved in a variable because its text changes.
        self.pause_button = tk.Button(
            self.control_frame,
            text="Pause",
            width=24,
            command=self.toggle_pause,
        )
        # Show the pause button.
        self.pause_button.pack(pady=2)

        # Stop button.
        tk.Button(
            self.control_frame,
            text="Stop",
            width=24,
            command=self.stop_robot,
        ).pack(pady=2)

        # Draw another divider.
        self.add_divider()

        # New grid button.
        tk.Button(
            self.control_frame,
            text="New Map / Grid Size",
            width=24,
            command=self.new_map,
        ).pack(pady=2)

        # Save map button.
        tk.Button(
            self.control_frame,
            text="Save Map",
            width=24,
            command=self.save_map,
        ).pack(pady=2)

        # Load map button.
        tk.Button(
            self.control_frame,
            text="Load Map",
            width=24,
            command=self.load_map,
        ).pack(pady=2)

        # Clear obstacles button.
        tk.Button(
            self.control_frame,
            text="Clear Grid Obstacles",
            width=24,
            command=self.clear_obstacles,
        ).pack(pady=2)

        # Reset whole simulation button.
        tk.Button(
            self.control_frame,
            text="Reset Simulation",
            width=24,
            command=self.reset_simulation,
        ).pack(pady=2)

        # Testing button.
        tk.Button(
            self.control_frame,
            text="Run System Tests",
            width=24,
            command=self.run_system_tests,
        ).pack(pady=2)

        # Divider before performance dashboard.
        self.add_divider()

        # Performance title.
        tk.Label(
            self.control_frame,
            text="PERFORMANCE",
            font=("Arial", 10, "bold"),
            bg=COLORS["panel"],
            fg="#60A5FA",
        ).pack(anchor="w")

        # This variable lets us change performance text easily.
        self.performance_text = tk.StringVar()
        # Show the performance information.
        tk.Label(
            self.control_frame,
            textvariable=self.performance_text,
            justify=tk.LEFT,
            wraplength=230,
            bg=COLORS["card"],
            fg=COLORS["text"],
            padx=10,
            pady=8,
        ).pack(anchor="w")

        # Divider before color guide.
        self.add_divider()

        # Explain every map color.
        legend = (
            "COLOR GUIDE\n"
            "Free = white\n"
            "Wall = dark gray\n"
            "Start = green     Goal = red\n"
            "Explored = blue   Path = yellow\n"
            "Travelled = orange\n"
            "Robot = purple"
        )
        # Display the legend.
        tk.Label(
            self.control_frame,
            text=legend,
            justify=tk.LEFT,
            bg=COLORS["panel"],
            fg=COLORS["muted"],
        ).pack(anchor="w")

        # Divider before status.
        self.add_divider()

        # Variable for changing status text.
        self.status_text = tk.StringVar()
        # Display status.
        tk.Label(
            self.control_frame,
            textvariable=self.status_text,
            wraplength=230,
            justify=tk.LEFT,
            bg=COLORS["card"],
            fg=COLORS["text"],
            padx=10,
            pady=8,
        ).pack(anchor="w")

    # Small helper that draws a horizontal divider.
    def add_divider(self):
        # A sunken frame looks like a thin line.
        tk.Frame(
            self.control_frame,
            height=2,
            bg="#334155",
            bd=0,
        ).pack(fill=tk.X, pady=8)

    # Build the big right-side drawing area.
    def build_canvas(self):
        # Make a frame for the grid.
        self.canvas_frame = tk.Frame(
            self.root, bg=COLORS["window"], padx=14, pady=14
        )
        # Use all remaining space.
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Small heading above the map makes the project look presentation-ready.
        tk.Label(
            self.canvas_frame,
            text="LIVE INDOOR NAVIGATION MAP",
            font=("Arial", 13, "bold"),
            bg=COLORS["window"],
            fg=COLORS["text"],
        ).pack(anchor="w", pady=(0, 8))

        # Create the drawing canvas.
        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg=COLORS["free"],
            highlightthickness=2,
            highlightbackground="#475569",
        )
        # Stretch canvas with window.
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Handle mouse clicks on cells.
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        # Redraw when window size changes.
        self.canvas.bind("<Configure>", lambda event: self.draw_grid())

    # Update status message.
    def set_status(self, message):
        # Put message into Tkinter variable.
        self.status_text.set(message)

    # Update performance dashboard.
    def update_performance(self, result):
        # If no A* result exists yet, show zero values.
        if result is None:
            self.performance_text.set(
                "Path length: 0\n"
                "Explored nodes: 0\n"
                "Calculation time: 0.000 ms"
            )
            return

        # Build text from A* result.
        self.performance_text.set(
            f"Path length: {result['path_length']}\n"
            f"Explored nodes: {result['explored_count']}\n"
            f"Calculation time: {result['calculation_time_ms']:.3f} ms"
        )

    # Change what clicking the map does.
    def change_mode(self, new_mode):
        # Save the mode.
        self.mode = new_mode
        # Easy names for status text.
        names = {
            "obstacle": "Add Obstacle",
            "erase": "Remove Obstacle",
            "start": "Choose Start",
            "goal": "Choose Destination",
        }
        # Tell user what tool is active.
        self.set_status(f"Tool selected: {names[new_mode]}. Click a cell.")

    # Calculate cell width and height.
    def cell_geometry(self):
        # Current canvas width.
        width = max(self.canvas.winfo_width(), 1)
        # Current canvas height.
        height = max(self.canvas.winfo_height(), 1)
        # Width of one cell.
        cell_width = width / self.map.columns
        # Height of one cell.
        cell_height = height / self.map.rows
        # Return both sizes.
        return cell_width, cell_height

    # Decide the color of one map cell.
    def get_cell_color(self, position):
        # Robot gets highest visual priority.
        if position == self.robot.current_position:
            return COLORS["robot"]

        # Travelled cells are orange.
        if position in self.robot.travelled:
            return COLORS["travelled"]

        # Start is green.
        if position == self.map.start:
            return COLORS["start"]

        # Goal is red.
        if position == self.map.goal:
            return COLORS["goal"]

        # Remaining route is yellow.
        if position in self.robot.remaining or position in self.path:
            return COLORS["path"]

        # Explored cells are light blue.
        if position in self.explored:
            return COLORS["explored"]

        # Obstacles are black.
        row, col = position
        if self.map.grid[row][col] == 1:
            return COLORS["obstacle"]

        # All other cells are white.
        return COLORS["free"]

    # Draw the entire grid.
    def draw_grid(self):
        # Do nothing if canvas does not exist yet.
        if not hasattr(self, "canvas"):
            return

        # Clear old drawing.
        self.canvas.delete("all")

        # Get cell size.
        cell_width, cell_height = self.cell_geometry()

        # Draw every row.
        for row in range(self.map.rows):
            # Draw every column.
            for col in range(self.map.columns):
                # Top-left x coordinate.
                x1 = col * cell_width
                # Top-left y coordinate.
                y1 = row * cell_height
                # Bottom-right x coordinate.
                x2 = x1 + cell_width
                # Bottom-right y coordinate.
                y2 = y1 + cell_height
                # Cell position tuple.
                position = (row, col)
                # Get cell color.
                color = self.get_cell_color(position)

                # Draw the rectangle.
                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline=COLORS["grid"],
                )

                # Draw a simple X pattern on walls.
                if self.map.grid[row][col] == 1:
                    pad = min(cell_width, cell_height) * 0.25
                    self.canvas.create_line(
                        x1 + pad, y1 + pad, x2 - pad, y2 - pad,
                        fill="#64748B", width=2,
                    )
                    self.canvas.create_line(
                        x2 - pad, y1 + pad, x1 + pad, y2 - pad,
                        fill="#64748B", width=2,
                    )

                # Yellow dots make the route easy to follow.
                if position in self.robot.remaining or position in self.path:
                    radius = min(cell_width, cell_height) * 0.12
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    self.canvas.create_oval(
                        center_x - radius, center_y - radius,
                        center_x + radius, center_y + radius,
                        fill="#CA8A04", outline="",
                    )

        # Draw easy symbols above the colored cells.
        self.draw_marker(self.map.start, "S", COLORS["start"])
        self.draw_marker(self.map.goal, "G", COLORS["goal"])
        self.draw_robot(self.robot.current_position)

    # Draw a white ring and letter for Start or Goal.
    def draw_marker(self, position, letter, color):
        if position is None:
            return

        cell_width, cell_height = self.cell_geometry()
        row, col = position
        center_x = col * cell_width + cell_width / 2
        center_y = row * cell_height + cell_height / 2
        radius = min(cell_width, cell_height) * 0.30

        self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill=color, outline="white", width=2,
        )
        self.canvas.create_text(
            center_x, center_y, text=letter,
            fill="white", font=("Arial", 11, "bold"),
        )

    # Draw a tiny robot face using only circles and one line.
    def draw_robot(self, position):
        if position is None:
            return

        cell_width, cell_height = self.cell_geometry()
        row, col = position
        center_x = col * cell_width + cell_width / 2
        center_y = row * cell_height + cell_height / 2
        size = min(cell_width, cell_height)
        radius = size * 0.32

        self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill=COLORS["robot"], outline="white", width=2,
        )
        eye = max(1.5, size * 0.045)
        for offset in (-radius * 0.35, radius * 0.35):
            self.canvas.create_oval(
                center_x + offset - eye, center_y - eye * 2,
                center_x + offset + eye, center_y,
                fill="white", outline="",
            )
        self.canvas.create_line(
            center_x - radius * 0.35, center_y + radius * 0.35,
            center_x + radius * 0.35, center_y + radius * 0.35,
            fill="white", width=2,
        )

    # Draw one letter in the center of a cell.
    def draw_letter(self, position, letter, text_color):
        # If there is no position, there is nothing to draw.
        if position is None:
            return

        # Get cell size.
        cell_width, cell_height = self.cell_geometry()
        # Read row and column.
        row, col = position
        # Find center x.
        center_x = col * cell_width + cell_width / 2
        # Find center y.
        center_y = row * cell_height + cell_height / 2

        # Draw the letter.
        self.canvas.create_text(
            center_x,
            center_y,
            text=letter,
            fill=text_color,
            font=("Arial", 12, "bold"),
        )

    # Convert a mouse click into a row-column cell.
    def click_to_cell(self, event):
        # Get cell size.
        cell_width, cell_height = self.cell_geometry()
        # Convert y coordinate to row.
        row = int(event.y / cell_height)
        # Convert x coordinate to column.
        col = int(event.x / cell_width)

        # Check the result is inside the map.
        if self.map.inside(row, col):
            return row, col

        # Return nothing for an invalid click.
        return None

    # Handle a mouse click on the map.
    def on_canvas_click(self, event):
        # Find which cell was clicked.
        cell = self.click_to_cell(event)
        # Ignore click outside map.
        if cell is None:
            return

        # Split position into row and column.
        row, col = cell

        # ADD OBSTACLE mode.
        if self.mode == "obstacle":
            # Try to add obstacle.
            worked = self.map.add_obstacle(row, col)

            # Explain result.
            if worked:
                self.set_status(f"Obstacle added at {cell}.")

                # If robot is moving and this obstacle blocks the remaining route,
                # the robot will detect it on the next step and automatically replan.
                if self.robot.running and cell in self.robot.remaining:
                    self.set_status(
                        f"Dynamic obstacle added at {cell}. Robot will stop before it and replan."
                    )
            else:
                self.set_status("Cannot place an obstacle on Start or Destination.")

        # REMOVE OBSTACLE mode.
        elif self.mode == "erase":
            # Remove obstacle.
            self.map.remove_obstacle(row, col)
            # Tell user.
            self.set_status(f"Obstacle removed from {cell}.")

        # CHOOSE START mode.
        elif self.mode == "start":
            # Try setting start.
            if self.map.set_start(row, col):
                # Reset old path because start changed.
                self.clear_path_state()
                # Tell user.
                self.set_status(f"Start selected at {cell}.")
            else:
                # Warn about blocked cell.
                self.set_status("Start must be placed on a free cell.")

        # CHOOSE GOAL mode.
        elif self.mode == "goal":
            # Try setting goal.
            if self.map.set_goal(row, col):
                # Reset old path because goal changed.
                self.clear_path_state()
                # Tell user.
                self.set_status(f"Destination selected at {cell}.")
            else:
                # Warn about blocked cell.
                self.set_status("Destination must be placed on a free cell.")

        # Redraw after every click.
        self.draw_grid()

    # Clear A*/robot path information but keep the map.
    def clear_path_state(self):
        # Stop any timer first.
        self.cancel_timer()
        # Clear drawn path.
        self.path = []
        # Clear explored cells.
        self.explored = []
        # Clear latest A* result.
        self.last_result = None
        # Reset robot.
        self.robot.reset()
        # Reset performance display.
        self.update_performance(None)

    # Run A* and show result.
    def find_path(self):
        # Ask Member 2's A* module to calculate.
        result = self.planner.find_path(
            self.map.grid,
            self.map.start,
            self.map.goal,
        )

        # Save the result.
        self.last_result = result
        # Save the path for drawing.
        self.path = result["path"]
        # Save explored cells for drawing.
        self.explored = result["explored"]
        # Update dashboard.
        self.update_performance(result)
        # Show A* message.
        self.set_status(result["message"])
        # Redraw map.
        self.draw_grid()

        # If no path exists, show a clear warning.
        if not result["success"]:
            messagebox.showwarning("A* Result", result["message"])

        # Return result so other GUI methods can reuse it.
        return result

    # Start the virtual robot.
    def run_robot(self):
        # If robot is paused, resume it instead of restarting everything.
        if self.robot.running and self.robot.paused:
            # Resume Member 3's robot.
            self.robot.resume()
            # Change button text back.
            self.pause_button.config(text="Pause")
            # Update status.
            self.set_status("Robot resumed.")
            # Continue movement loop.
            self.schedule_next_step()
            return

        # If robot is already moving, do not start a second loop.
        if self.robot.running:
            self.set_status("Robot is already moving.")
            return

        # Calculate a fresh A* path.
        result = self.find_path()

        # Stop if A* failed.
        if not result["success"]:
            return

        # Load the path into Member 3's robot.
        self.robot.load_path(result["path"])
        # Start the robot.
        self.robot.start()
        # Clear general path drawing because robot.remaining now controls it.
        self.path = []
        # Tell user.
        self.set_status("Robot started. You can add a dynamic obstacle while it moves.")
        # Redraw.
        self.draw_grid()
        # Schedule first movement.
        self.schedule_next_step()

    # Pause or resume robot.
    def toggle_pause(self):
        # If no robot is running, there is nothing to pause.
        if not self.robot.running:
            self.set_status("Robot is not running.")
            return

        # If currently paused, resume.
        if self.robot.paused:
            # Resume robot.
            self.robot.resume()
            # Change button label.
            self.pause_button.config(text="Pause")
            # Update status.
            self.set_status("Robot resumed.")
            # Continue movement.
            self.schedule_next_step()
        else:
            # Pause robot.
            self.robot.pause()
            # Change button label.
            self.pause_button.config(text="Resume")
            # Cancel current timer so no hidden movement happens.
            self.cancel_timer()
            # Update status.
            self.set_status("Robot paused. Position is safely preserved.")

    # Stop robot movement.
    def stop_robot(self):
        # Cancel future movement.
        self.cancel_timer()
        # Stop Member 3's robot.
        self.robot.stop()
        # Reset pause button text.
        self.pause_button.config(text="Pause")
        # Tell user.
        self.set_status("Robot stopped at its current cell.")
        # Redraw.
        self.draw_grid()

    # Schedule one robot step after a short delay.
    def schedule_next_step(self):
        # Do nothing if robot is not running.
        if not self.robot.running:
            return

        # Do nothing while paused.
        if self.robot.paused:
            return

        # Prevent duplicate timers.
        self.cancel_timer()

        # Ask Tkinter to call robot_step later.
        self.timer_id = self.root.after(self.step_delay, self.robot_step)

    # Perform one robot movement step.
    def robot_step(self):
        # Timer has now fired, so clear its ID.
        self.timer_id = None

        # Ask Member 3's robot to move one cell safely.
        state = self.robot.step(self.map.grid)

        # If next route cell became blocked, ask A* to replan.
        if state == "blocked":
            # Tell user what is happening.
            self.set_status("Dynamic obstacle detected. Replanning from current robot position...")

            # Ask Member 2's planner for a new route.
            result = self.planner.replan(
                self.map.grid,
                self.robot.current_position,
                self.map.goal,
            )

            # Save A* result for display.
            self.last_result = result
            # Save explored cells.
            self.explored = result["explored"]
            # Update performance dashboard.
            self.update_performance(result)

            # If a new path exists, give it to the robot.
            if result["success"]:
                # Apply new path from current position.
                self.robot.apply_replanned_path(result["path"])
                # Tell user success.
                self.set_status("Dynamic obstacle avoided. New A* route found.")
                # Redraw new route.
                self.draw_grid()
                # Keep moving.
                self.schedule_next_step()
                return

            # No new route exists, so stop safely.
            self.robot.apply_replanned_path([])
            # Redraw stopped robot.
            self.draw_grid()
            # Show clear warning requested in Member 4's work plan.
            messagebox.showwarning(
                "Destination Unreachable",
                "The new obstacle blocks every possible route. The robot stopped safely.",
            )
            # Update status.
            self.set_status("Destination became unreachable. Robot stopped safely.")
            return

        # Redraw after a normal movement.
        self.draw_grid()

        # If robot reached the goal, celebrate and stop scheduling.
        if state == "finished":
            # Reset button text.
            self.pause_button.config(text="Pause")
            # Tell user.
            self.set_status("Success! Robot reached the destination.")
            # Show a small information box.
            messagebox.showinfo("Simulation Complete", "Robot reached the destination safely.")
            return

        # If one normal move happened, schedule the next one.
        if state == "moved":
            self.schedule_next_step()

    # Cancel Tkinter movement timer safely.
    def cancel_timer(self):
        # Only cancel when a timer exists.
        if self.timer_id is not None:
            try:
                # Ask Tkinter to cancel it.
                self.root.after_cancel(self.timer_id)
            except tk.TclError:
                # Ignore if Tkinter already removed it.
                pass
            # Forget old timer ID.
            self.timer_id = None

    # Create a fresh map with a chosen size.
    def new_map(self):
        # Ask for row count.
        rows = simpledialog.askinteger(
            "New Map",
            "Number of rows (5 to 40):",
            minvalue=5,
            maxvalue=40,
        )

        # If user pressed Cancel, stop.
        if rows is None:
            return

        # Ask for column count.
        columns = simpledialog.askinteger(
            "New Map",
            "Number of columns (5 to 50):",
            minvalue=5,
            maxvalue=50,
        )

        # If user pressed Cancel, stop.
        if columns is None:
            return

        # Stop old simulation.
        self.clear_path_state()
        # Ask Member 1's map module to create new grid.
        self.map.new_map(rows, columns)
        # Redraw.
        self.draw_grid()
        # Tell user.
        self.set_status(f"New {rows} x {columns} map created.")

    # Save current map to a JSON file.
    def save_map(self):
        # Open a Save As window.
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON map", "*.json")],
            title="Save Map",
        )

        # Stop if user cancels.
        if not filename:
            return

        try:
            # Ask Member 1's module to save.
            self.map.save(filename)
            # Tell user.
            self.set_status("Map saved successfully.")
        except Exception as error:
            # Show easy error message.
            messagebox.showerror("Save Error", str(error))

    # Load a saved JSON map.
    def load_map(self):
        # Open a file chooser.
        filename = filedialog.askopenfilename(
            filetypes=[("JSON map", "*.json")],
            title="Load Map",
        )

        # Stop if user cancels.
        if not filename:
            return

        try:
            # Clear old simulation first.
            self.clear_path_state()
            # Ask Member 1's map module to load.
            self.map.load(filename)
            # Redraw loaded map.
            self.draw_grid()
            # Tell user.
            self.set_status("Map loaded successfully.")
        except Exception as error:
            # Show clear load error.
            messagebox.showerror("Load Error", str(error))

    # Clear all obstacles but keep map size, start, and destination.
    def clear_obstacles(self):
        # Stop old movement and path.
        self.clear_path_state()
        # Ask Member 1 to clear obstacles.
        self.map.clear_obstacles()
        # Redraw.
        self.draw_grid()
        # Tell user.
        self.set_status("All obstacles were cleared.")

    # Reset simulation information while keeping the obstacle map.
    def reset_simulation(self):
        # Clear route and robot state.
        self.clear_path_state()
        # Also remove start and destination for a full simulation reset.
        self.map.start = None
        self.map.goal = None
        # Redraw.
        self.draw_grid()
        # Reset pause button text.
        self.pause_button.config(text="Pause")
        # Tell user.
        self.set_status("Simulation reset. Choose a new Start and Destination.")

    # Run several automatic tests and report PASS/FAIL.
    def run_system_tests(self):
        # Make a list to store readable test results.
        results = []

        # ---------------- TEST 1 ----------------
        # Simple reachable map.
        test_grid_1 = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        # Run A*.
        answer_1 = self.planner.find_path(test_grid_1, (0, 0), (2, 2))
        # PASS if a valid route exists.
        results.append(("Reachable path", answer_1["success"]))

        # ---------------- TEST 2 ----------------
        # Goal is completely separated by a wall.
        test_grid_2 = [
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ]
        # Run A*.
        answer_2 = self.planner.find_path(test_grid_2, (0, 0), (2, 2))
        # PASS if A* correctly says no route.
        results.append(("Unreachable goal", not answer_2["success"]))

        # ---------------- TEST 3 ----------------
        # Narrow passage map.
        test_grid_3 = [
            [0, 1, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 0, 1],
            [1, 1, 0, 0],
        ]
        # Run A*.
        answer_3 = self.planner.find_path(test_grid_3, (0, 0), (3, 3))
        # PASS if route exists and validates.
        valid_3 = answer_3["success"] and self.planner.validate_path(test_grid_3, answer_3["path"])
        results.append(("Narrow passage", valid_3))

        # ---------------- TEST 4 ----------------
        # Check robot never enters a blocked next cell.
        # First build a tiny path manually.
        self.robot.reset()
        # Give it a short route.
        self.robot.load_path([(0, 0), (0, 1), (0, 2)])
        # Start it.
        self.robot.start()
        # Put an obstacle directly in front of robot.
        test_grid_4 = [[0, 1, 0]]
        # Ask robot to step.
        robot_state = self.robot.step(test_grid_4)
        # PASS if robot reports blocked and stays at (0, 0).
        valid_4 = robot_state == "blocked" and self.robot.current_position == (0, 0)
        results.append(("Robot obstacle safety", valid_4))

        # Reset robot after test so test data does not appear on real map.
        self.robot.reset()
        # Redraw real map.
        self.draw_grid()

        # Count passed tests.
        passed = sum(1 for _, success in results if success)
        # Count total tests.
        total = len(results)

        # Build readable multi-line result text.
        lines = []
        # Add each test line.
        for test_name, success in results:
            # Write PASS or FAIL.
            state = "PASS" if success else "FAIL"
            # Save the line.
            lines.append(f"{test_name}: {state}")

        # Add summary line.
        lines.append(f"\nTotal: {passed}/{total} tests passed")
        # Join lines into one message.
        report = "\n".join(lines)

        # Show test report.
        messagebox.showinfo("System Test Results", report)
        # Also show short status.
        self.set_status(f"System testing completed: {passed}/{total} tests passed.")
