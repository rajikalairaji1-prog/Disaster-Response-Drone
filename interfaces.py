# interfaces.py

from dataclasses import dataclass
from enum import Enum
from typing import Tuple, List, Set


class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    STAY = 4


@dataclass
class AgentState:
    agent_id: int
    position: Tuple[int, int]  # (x, y) coordinates on the grid
    battery: float
    survivors_rescued: int
    is_active: bool = True     # False if battery depleted or crashed


@dataclass
class EnvironmentState:
    grid_bounds: Tuple[int, int]         # (width, height)
    agent_states: List[AgentState]
    survivor_positions: List[Tuple[int, int]]
    obstacle_positions: List[Tuple[int, int]]
    global_visited_cells: Set[Tuple[int, int]]  # Combined coverage map