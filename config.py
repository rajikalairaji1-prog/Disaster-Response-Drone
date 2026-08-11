# config.py
"""
Central configuration settings for the 3D Disaster Response Drone.
"""

# 3D Grid World Dimensions (X = Width, Y = Length, Z = Altitude)
GRID_X: int = 10  # East-West axis
GRID_Y: int = 10  # North-South axis
GRID_Z: int = 5   # Height / Altitude layers

# Drone Constraints
MAX_STEPS_PER_EPISODE: int = 100
INITIAL_BATTERY: int = 100

# Start & Goal Locations (x, y, z)
START_POSITION: tuple = (0, 0, 0)
SURVIVOR_POSITION: tuple = (8, 8, 2)