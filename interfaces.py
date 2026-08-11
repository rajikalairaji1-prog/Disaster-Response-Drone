# interfaces.py
"""
Shared data contracts between AI (Member 1), Environment (Member 2), and UI (Member 3).
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple
import numpy as np


class Action3D(Enum):
    """6 Movement directions in 3D Space."""

    FORWARD = "FORWARD"  # +Y (North)
    BACKWARD = "BACKWARD"  # -Y (South)
    LEFT = "LEFT"  # -X (West)
    RIGHT = "RIGHT"  # +X (East)
    ASCEND = "ASCEND"  # +Z (Up in Altitude)
    DESCEND = "DESCEND"  # -Z (Down in Altitude)


@dataclass(frozen=True)
class Position3D:
    """3D Coordinates for grid positioning."""

    x: int
    y: int
    z: int

    def to_tuple(self) -> Tuple[int, int, int]:
        return (self.x, self.y, self.z)


@dataclass
class AgentState:
    """Current state snapshot passed to the AI module."""

    position: Position3D
    battery: int = 100
    has_found_survivor: bool = False


@dataclass
class TelemetryData:
    """Telemetry bundle passed to Member 3's Pygame Dashboard."""

    grid_matrix: np.ndarray  # Dim: (GRID_X, GRID_Y, GRID_Z)
    visit_count_matrix: np.ndarray  # Dim: (GRID_X, GRID_Y, GRID_Z)
    drone_positions: List[Position3D]
    drone_batteries: List[float]
    active_paradigm: str
    step_number: int
    coverage_percentage: float
    survivors_found: int
    total_survivors: int