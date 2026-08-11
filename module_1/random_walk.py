# module_1_ai/random_walk.py
"""
Day 1 Baseline: 3D Uninformed Random Walk Agent.
Picks a uniform random action from 6 directions in 3D space.
"""

import random
from typing import Tuple
from config import GRID_X, GRID_Y, GRID_Z
from interfaces import Action3D, Position3D, AgentState


class RandomWalkAgent3D:
    def __init__(self, start_pos: Tuple[int, int, int] = (0, 0, 0)):
        self.position = Position3D(*start_pos)
        self.actions = list(Action3D)

    def get_action(self, state: AgentState = None) -> Action3D:
        """Picks a random 3D action."""
        return random.choice(self.actions)

    def predict_next_position(self, current_pos: Position3D, action: Action3D) -> Position3D:
        """
        Helper method to calculate the next position after an action, 
        ensuring the drone stays within 3D grid bounds (0 to GRID_MAX - 1).
        """
        x, y, z = current_pos.x, current_pos.y, current_pos.z

        if action == Action3D.FORWARD:
            y = min(GRID_Y - 1, y + 1)
        elif action == Action3D.BACKWARD:
            y = max(0, y - 1)
        elif action == Action3D.RIGHT:
            x = min(GRID_X - 1, x + 1)
        elif action == Action3D.LEFT:
            x = max(0, x - 1)
        elif action == Action3D.ASCEND:
            z = min(GRID_Z - 1, z + 1)
        elif action == Action3D.DESCEND:
            z = max(0, z - 1)

        return Position3D(x, y, z)