"""JSON map saving and loading functions for Week 2."""

from __future__ import annotations

import json
from pathlib import Path

from occupancy_grid import GridValidationError, OccupancyGrid


class MapStorageError(RuntimeError):
    """Raised when a map cannot be saved or loaded."""


def normalize_json_path(path: str | Path) -> Path:
    """Return a Path whose filename ends with .json."""
    result = Path(path)
    if result.suffix.lower() != ".json":
        result = result.with_suffix(".json")
    return result


def save_map(grid: OccupancyGrid, path: str | Path) -> Path:
    """Save an occupancy grid as formatted JSON and return the final path."""
    output_path = normalize_json_path(path)

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(grid.to_dict(), file, indent=2)
    except OSError as exc:
        raise MapStorageError(f"Could not save map: {exc}") from exc

    return output_path


def load_map(path: str | Path) -> OccupancyGrid:
    """Load and validate an occupancy grid from a JSON file."""
    input_path = Path(path)

    try:
        with input_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as exc:
        raise MapStorageError(f"Map file not found: {input_path}") from exc
    except json.JSONDecodeError as exc:
        raise MapStorageError(
            f"The selected file does not contain valid JSON: {exc}"
        ) from exc
    except OSError as exc:
        raise MapStorageError(f"Could not read map: {exc}") from exc

    try:
        return OccupancyGrid.from_dict(data)
    except (GridValidationError, TypeError) as exc:
        raise MapStorageError(f"Invalid map data: {exc}") from exc
