"""Occupancy-grid data model for the indoor robot simulator.

Week 2 scope:
- 0 means a free cell.
- 1 means a blocked/obstacle cell.
- The start and destination are stored separately from the 0/1 grid.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


Position = tuple[int, int]


class GridValidationError(ValueError):
    """Raised when grid data or a requested grid operation is invalid."""


@dataclass
class OccupancyGrid:
    """Store and update a two-dimensional occupancy grid."""

    rows: int = 10
    cols: int = 10
    cells: list[list[int]] = field(default_factory=list)
    start: Optional[Position] = None
    destination: Optional[Position] = None

    MIN_SIZE = 3
    MAX_SIZE = 50

    def __post_init__(self) -> None:
        self._validate_size(self.rows, self.cols)

        if not self.cells:
            self.cells = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self._validate_cells(self.cells)

        if self.start is not None:
            self._validate_position(self.start)
            if self.is_blocked(*self.start):
                raise GridValidationError("The start position cannot be on an obstacle.")

        if self.destination is not None:
            self._validate_position(self.destination)
            if self.is_blocked(*self.destination):
                raise GridValidationError(
                    "The destination position cannot be on an obstacle."
                )

        if (
            self.start is not None
            and self.destination is not None
            and self.start == self.destination
        ):
            raise GridValidationError(
                "The start and destination positions must be different."
            )

    @classmethod
    def create_empty(cls, rows: int, cols: int) -> "OccupancyGrid":
        """Create an empty grid containing only free cells."""
        return cls(rows=rows, cols=cols)

    def _validate_size(self, rows: int, cols: int) -> None:
        if not isinstance(rows, int) or not isinstance(cols, int):
            raise GridValidationError("Rows and columns must be integers.")
        if not (self.MIN_SIZE <= rows <= self.MAX_SIZE):
            raise GridValidationError(
                f"Rows must be between {self.MIN_SIZE} and {self.MAX_SIZE}."
            )
        if not (self.MIN_SIZE <= cols <= self.MAX_SIZE):
            raise GridValidationError(
                f"Columns must be between {self.MIN_SIZE} and {self.MAX_SIZE}."
            )

    def _validate_cells(self, cells: list[list[int]]) -> None:
        if len(cells) != self.rows:
            raise GridValidationError(
                f"Expected {self.rows} rows, but received {len(cells)}."
            )

        for row_index, row in enumerate(cells):
            if len(row) != self.cols:
                raise GridValidationError(
                    f"Row {row_index} must contain exactly {self.cols} cells."
                )
            for value in row:
                if value not in (0, 1):
                    raise GridValidationError(
                        "Every occupancy-grid value must be either 0 or 1."
                    )

    def _validate_position(self, position: Position) -> None:
        if (
            not isinstance(position, tuple)
            or len(position) != 2
            or not all(isinstance(value, int) for value in position)
        ):
            raise GridValidationError("A position must be a (row, column) tuple.")

        row, col = position
        if not self.in_bounds(row, col):
            raise GridValidationError(
                f"Position ({row}, {col}) is outside the current map."
            )

    def in_bounds(self, row: int, col: int) -> bool:
        """Return True when a row-column position is inside the grid."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_blocked(self, row: int, col: int) -> bool:
        """Return True if a cell contains an obstacle."""
        if not self.in_bounds(row, col):
            raise GridValidationError(
                f"Position ({row}, {col}) is outside the current map."
            )
        return self.cells[row][col] == 1

    def set_obstacle(self, row: int, col: int) -> None:
        """Mark a cell as blocked."""
        self._validate_position((row, col))
        if self.start == (row, col):
            raise GridValidationError("An obstacle cannot replace the start position.")
        if self.destination == (row, col):
            raise GridValidationError(
                "An obstacle cannot replace the destination position."
            )
        self.cells[row][col] = 1

    def remove_obstacle(self, row: int, col: int) -> None:
        """Mark a cell as free."""
        self._validate_position((row, col))
        self.cells[row][col] = 0

    def toggle_obstacle(self, row: int, col: int) -> None:
        """Switch a cell between free and blocked."""
        if self.is_blocked(row, col):
            self.remove_obstacle(row, col)
        else:
            self.set_obstacle(row, col)

    def set_start(self, row: int, col: int) -> None:
        """Set the virtual robot's starting cell."""
        self._validate_position((row, col))
        if self.is_blocked(row, col):
            raise GridValidationError("The start position must be on a free cell.")
        if self.destination == (row, col):
            raise GridValidationError(
                "The start position must be different from the destination."
            )
        self.start = (row, col)

    def set_destination(self, row: int, col: int) -> None:
        """Set the target/destination cell."""
        self._validate_position((row, col))
        if self.is_blocked(row, col):
            raise GridValidationError(
                "The destination position must be on a free cell."
            )
        if self.start == (row, col):
            raise GridValidationError(
                "The destination must be different from the start position."
            )
        self.destination = (row, col)

    def clear_obstacles(self) -> None:
        """Remove every obstacle without changing start or destination."""
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col] = 0

    def clear_positions(self) -> None:
        """Remove the selected start and destination positions."""
        self.start = None
        self.destination = None

    def count_obstacles(self) -> int:
        """Return the number of blocked cells."""
        return sum(sum(row) for row in self.cells)

    def to_dict(self) -> dict[str, Any]:
        """Convert the grid into JSON-compatible data."""
        return {
            "format_version": 1,
            "rows": self.rows,
            "cols": self.cols,
            "cells": [row[:] for row in self.cells],
            "start": list(self.start) if self.start is not None else None,
            "destination": (
                list(self.destination) if self.destination is not None else None
            ),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OccupancyGrid":
        """Create an OccupancyGrid from saved JSON-compatible data."""
        if not isinstance(data, dict):
            raise GridValidationError("Map data must be a JSON object.")

        required = {"rows", "cols", "cells"}
        missing = required.difference(data)
        if missing:
            raise GridValidationError(
                "The map file is missing: " + ", ".join(sorted(missing))
            )

        start_data = data.get("start")
        destination_data = data.get("destination")

        start = tuple(start_data) if start_data is not None else None
        destination = (
            tuple(destination_data) if destination_data is not None else None
        )

        return cls(
            rows=data["rows"],
            cols=data["cols"],
            cells=data["cells"],
            start=start,
            destination=destination,
        )
