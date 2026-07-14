"""Tkinter map editor for Week 1 and Week 2.

This GUI intentionally does not run A* yet. Connecting the map to A* is a
later-week task in the supplied work plan.
"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from map_storage import MapStorageError, load_map, save_map
from occupancy_grid import GridValidationError, OccupancyGrid


PROJECT_DIR = Path(__file__).resolve().parent
SAMPLE_DIR = PROJECT_DIR / "sample_maps"


class MapEditorApp:
    """Graphical occupancy-grid creator and obstacle editor."""

    CELL_COLORS = {
        "free": "#ffffff",
        "obstacle": "#343a40",
        "start": "#2f9e44",
        "destination": "#e03131",
    }

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Indoor Robot Map Editor - Week 1 & Week 2")
        self.root.minsize(900, 650)

        self.grid_model = OccupancyGrid.create_empty(10, 10)
        self.edit_mode = tk.StringVar(value="obstacle")
        self.rows_var = tk.StringVar(value="10")
        self.cols_var = tk.StringVar(value="10")
        self.sample_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready. Click a cell to edit the map.")

        self.canvas_margin = 12
        self.cell_size = 40

        self._build_layout()
        self._refresh_sample_names()
        self.draw_grid()

    def _build_layout(self) -> None:
        header = ttk.Frame(self.root, padding=(12, 12, 12, 6))
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Autonomous Indoor Robot - Occupancy Grid Editor",
            font=("TkDefaultFont", 17, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            header,
            text=(
                "Week 1: project structure and workflow | "
                "Week 2: create, load, save, and edit 0/1 maps"
            ),
        ).pack(anchor="w", pady=(3, 0))

        main = ttk.Frame(self.root, padding=12)
        main.pack(fill="both", expand=True)

        control_panel = ttk.LabelFrame(main, text="Map Controls", padding=12)
        control_panel.pack(side="left", fill="y", padx=(0, 12))

        canvas_panel = ttk.LabelFrame(main, text="Map Preview", padding=8)
        canvas_panel.pack(side="left", fill="both", expand=True)

        ttk.Label(control_panel, text="New map size").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )

        ttk.Label(control_panel, text="Rows:").grid(
            row=1, column=0, sticky="w", pady=(6, 0)
        )
        ttk.Entry(control_panel, textvariable=self.rows_var, width=8).grid(
            row=1, column=1, sticky="w", pady=(6, 0)
        )

        ttk.Label(control_panel, text="Columns:").grid(
            row=2, column=0, sticky="w", pady=(4, 0)
        )
        ttk.Entry(control_panel, textvariable=self.cols_var, width=8).grid(
            row=2, column=1, sticky="w", pady=(4, 0)
        )

        ttk.Button(
            control_panel, text="Create New Map", command=self.create_new_map
        ).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(8, 3))

        ttk.Separator(control_panel).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=10
        )

        ttk.Label(control_panel, text="Edit mode").grid(
            row=5, column=0, columnspan=2, sticky="w"
        )

        modes = [
            ("Place obstacle (1)", "obstacle"),
            ("Remove obstacle (0)", "erase"),
            ("Choose start", "start"),
            ("Choose destination", "destination"),
        ]
        for index, (label, value) in enumerate(modes, start=6):
            ttk.Radiobutton(
                control_panel,
                text=label,
                variable=self.edit_mode,
                value=value,
            ).grid(row=index, column=0, columnspan=2, sticky="w", pady=2)

        ttk.Button(
            control_panel, text="Clear All Obstacles", command=self.clear_obstacles
        ).grid(row=10, column=0, columnspan=2, sticky="ew", pady=(10, 3))
        ttk.Button(
            control_panel,
            text="Clear Start & Destination",
            command=self.clear_positions,
        ).grid(row=11, column=0, columnspan=2, sticky="ew", pady=3)

        ttk.Separator(control_panel).grid(
            row=12, column=0, columnspan=2, sticky="ew", pady=10
        )

        ttk.Button(control_panel, text="Save Map", command=self.save_current_map).grid(
            row=13, column=0, columnspan=2, sticky="ew", pady=3
        )
        ttk.Button(control_panel, text="Load Map", command=self.load_selected_map).grid(
            row=14, column=0, columnspan=2, sticky="ew", pady=3
        )

        ttk.Label(control_panel, text="Bundled sample map").grid(
            row=15, column=0, columnspan=2, sticky="w", pady=(12, 3)
        )
        self.sample_box = ttk.Combobox(
            control_panel,
            textvariable=self.sample_var,
            state="readonly",
            width=25,
        )
        self.sample_box.grid(row=16, column=0, columnspan=2, sticky="ew")

        ttk.Button(
            control_panel, text="Load Sample", command=self.load_sample_map
        ).grid(row=17, column=0, columnspan=2, sticky="ew", pady=(4, 3))

        ttk.Separator(control_panel).grid(
            row=18, column=0, columnspan=2, sticky="ew", pady=10
        )

        ttk.Label(control_panel, text="Legend", font=("TkDefaultFont", 10, "bold")).grid(
            row=19, column=0, columnspan=2, sticky="w"
        )
        legend_items = [
            ("White", "Free cell = 0"),
            ("Dark", "Obstacle = 1"),
            ("Green", "Start"),
            ("Red", "Destination"),
        ]
        for row_index, (name, meaning) in enumerate(legend_items, start=20):
            ttk.Label(control_panel, text=f"{name}: {meaning}").grid(
                row=row_index, column=0, columnspan=2, sticky="w", pady=1
            )

        self.canvas = tk.Canvas(
            canvas_panel,
            background="#e9ecef",
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Configure>", lambda _event: self.draw_grid())

        status_frame = ttk.Frame(self.root, padding=(12, 0, 12, 12))
        status_frame.pack(fill="x")
        ttk.Label(status_frame, textvariable=self.status_var).pack(anchor="w")

    def _refresh_sample_names(self) -> None:
        names = sorted(path.name for path in SAMPLE_DIR.glob("*.json"))
        self.sample_box["values"] = names
        if names:
            self.sample_var.set(names[0])

    def create_new_map(self) -> None:
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
            self.grid_model = OccupancyGrid.create_empty(rows, cols)
        except ValueError:
            messagebox.showerror("Invalid size", "Rows and columns must be integers.")
            return
        except GridValidationError as exc:
            messagebox.showerror("Invalid size", str(exc))
            return

        self.status_var.set(f"Created a new empty {rows} x {cols} map.")
        self.draw_grid()

    def _calculate_geometry(self) -> tuple[int, int, int]:
        canvas_width = max(self.canvas.winfo_width(), 300)
        canvas_height = max(self.canvas.winfo_height(), 300)

        available_width = canvas_width - (2 * self.canvas_margin)
        available_height = canvas_height - (2 * self.canvas_margin)

        cell_size = max(
            8,
            min(
                available_width // self.grid_model.cols,
                available_height // self.grid_model.rows,
                50,
            ),
        )

        grid_width = cell_size * self.grid_model.cols
        grid_height = cell_size * self.grid_model.rows
        offset_x = max(self.canvas_margin, (canvas_width - grid_width) // 2)
        offset_y = max(self.canvas_margin, (canvas_height - grid_height) // 2)
        return cell_size, offset_x, offset_y

    def draw_grid(self) -> None:
        self.canvas.delete("all")
        cell_size, offset_x, offset_y = self._calculate_geometry()
        self.cell_size = cell_size
        self.grid_offset_x = offset_x
        self.grid_offset_y = offset_y

        for row in range(self.grid_model.rows):
            for col in range(self.grid_model.cols):
                x1 = offset_x + col * cell_size
                y1 = offset_y + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                position = (row, col)
                if position == self.grid_model.start:
                    fill = self.CELL_COLORS["start"]
                    label = "S"
                elif position == self.grid_model.destination:
                    fill = self.CELL_COLORS["destination"]
                    label = "D"
                elif self.grid_model.cells[row][col] == 1:
                    fill = self.CELL_COLORS["obstacle"]
                    label = ""
                else:
                    fill = self.CELL_COLORS["free"]
                    label = ""

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=fill,
                    outline="#adb5bd",
                )
                if label and cell_size >= 18:
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=label,
                        fill="white",
                        font=("TkDefaultFont", max(8, cell_size // 3), "bold"),
                    )

        info = (
            f"{self.grid_model.rows} x {self.grid_model.cols} map | "
            f"Obstacles: {self.grid_model.count_obstacles()} | "
            f"Start: {self.grid_model.start or 'not selected'} | "
            f"Destination: {self.grid_model.destination or 'not selected'}"
        )
        self.canvas.create_text(
            10,
            10,
            anchor="nw",
            text=info,
            fill="#212529",
            font=("TkDefaultFont", 9, "bold"),
        )

    def on_canvas_click(self, event: tk.Event) -> None:
        col = (event.x - self.grid_offset_x) // self.cell_size
        row = (event.y - self.grid_offset_y) // self.cell_size

        if not self.grid_model.in_bounds(row, col):
            return

        mode = self.edit_mode.get()
        try:
            if mode == "obstacle":
                self.grid_model.set_obstacle(row, col)
                action = "Placed obstacle"
            elif mode == "erase":
                self.grid_model.remove_obstacle(row, col)
                action = "Removed obstacle"
            elif mode == "start":
                self.grid_model.set_start(row, col)
                action = "Selected start"
            elif mode == "destination":
                self.grid_model.set_destination(row, col)
                action = "Selected destination"
            else:
                return
        except GridValidationError as exc:
            messagebox.showwarning("Cannot edit cell", str(exc))
            return

        self.status_var.set(f"{action} at row {row}, column {col}.")
        self.draw_grid()

    def clear_obstacles(self) -> None:
        self.grid_model.clear_obstacles()
        self.status_var.set("All obstacles were removed.")
        self.draw_grid()

    def clear_positions(self) -> None:
        self.grid_model.clear_positions()
        self.status_var.set("Start and destination were cleared.")
        self.draw_grid()

    def save_current_map(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Save occupancy grid",
            initialdir=str(PROJECT_DIR),
            defaultextension=".json",
            filetypes=[("JSON map", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            saved_path = save_map(self.grid_model, path)
        except MapStorageError as exc:
            messagebox.showerror("Save failed", str(exc))
            return

        self.status_var.set(f"Map saved to {saved_path.name}.")
        messagebox.showinfo("Map saved", f"Saved successfully:\n{saved_path}")

    def load_selected_map(self) -> None:
        path = filedialog.askopenfilename(
            title="Load occupancy grid",
            initialdir=str(PROJECT_DIR),
            filetypes=[("JSON map", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return

        self._load_path(Path(path))

    def load_sample_map(self) -> None:
        selected = self.sample_var.get()
        if not selected:
            messagebox.showwarning("No sample", "No sample map is available.")
            return
        self._load_path(SAMPLE_DIR / selected)

    def _load_path(self, path: Path) -> None:
        try:
            loaded_grid = load_map(path)
        except MapStorageError as exc:
            messagebox.showerror("Load failed", str(exc))
            return

        self.grid_model = loaded_grid
        self.rows_var.set(str(loaded_grid.rows))
        self.cols_var.set(str(loaded_grid.cols))
        self.status_var.set(f"Loaded map: {path.name}")
        self.draw_grid()


def run_gui() -> None:
    """Start the Tkinter application."""
    root = tk.Tk()
    MapEditorApp(root)
    root.mainloop()
