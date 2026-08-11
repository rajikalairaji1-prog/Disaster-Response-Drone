# config.py
"""
Central configuration settings for the 3D Disaster Response Drone.
Shared across AI (Member 1), Environment (Member 2), and UI (Member 3).
"""

# ----------------------------------------------------
# 1. 3D Grid World Dimensions
# ----------------------------------------------------
GRID_X: int = 10  # East-West axis
GRID_Y: int = 10  # North-South axis
GRID_Z: int = 5   # Altitude layers (0 = Ground level)

# ----------------------------------------------------
# 2. Drone Fleet & Constraint Settings
# ----------------------------------------------------
NUM_DRONES: int = 3
INITIAL_BATTERY: float = 100.0
BATTERY_DRAIN_PER_STEP: float = 1.0

# Episode limits
MAX_STEPS_PER_EPISODE: int = 100

# ----------------------------------------------------
# 3. Key World Locations (x, y, z)
# ----------------------------------------------------
START_POSITION: tuple = (0, 0, 0)
SURVIVOR_POSITION: tuple = (8, 8, 2)

# ----------------------------------------------------
# 4. Visualization / Dashboard Settings (Member 3)
# ----------------------------------------------------
FPS: int = 8  # Animation speed (frames per second)
WINDOW_WIDTH: int = 1280
WINDOW_HEIGHT: int = 720
SHOW_HEATMAP_DEFAULT: bool = False

# ----------------------------------------------------
# 5. Reinforcement Learning Hyperparameters (Member 1)
# ----------------------------------------------------
LEARNING_RATE: float = 0.1
GAMMA: float = 0.95            # Discount factor
EPSILON_START: float = 1.0     # Exploration rate start
EPSILON_MIN: float = 0.05      # Minimum exploration rate
EPSILON_DECAY: float = 0.995   # Decay rate per episode
TOTAL_TRAINING_EPISODES: int = 500