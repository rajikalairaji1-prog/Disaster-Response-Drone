# config.py

# Grid & World Parameters
GRID_WIDTH = 20
GRID_HEIGHT = 20
CELL_SIZE = 30  # Pygame pixel dimensions per cell
NUM_DRONES = 3
NUM_SURVIVORS = 5
NUM_OBSTACLES = 15

# Drone Capabilities
INITIAL_BATTERY = 100.0
BATTERY_DRAIN_PER_STEP = 0.5

# Reinforcement Learning Hyperparameters
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.95
EPSILON_START = 1.0
EPSILON_MIN = 0.05
EPSILON_DECAY = 0.995
NUM_EPISODES = 1000