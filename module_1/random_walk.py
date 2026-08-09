# module_1_ai/random_walk.py

import random
from typing import Optional
from interfaces import Action, AgentState, EnvironmentState

class RandomWalkAgent:
    """
    Day 1 Baseline Agent: Picks random actions uniformly.
    Serves as the baseline control group and unblocks team integration.
    """
    def __init__(self, agent_id: int, seed: Optional[int] = None):
        self.agent_id = agent_id
        if seed is not None:
            random.seed(seed + agent_id)

    def select_action(self, state: AgentState, env_state: EnvironmentState) -> Action:
        """Randomly chooses one of the available discrete movement actions."""
        return random.choice(list(Action))

    def update(self, state: AgentState, action: Action, reward: float, 
               next_state: AgentState, done: bool) -> None:
        """
        No-op for baseline random agent. 
        Maintains interface compatibility for Q-learning.
        """
        pass