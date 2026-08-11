# main.py
import time
import pygame
import numpy as np

# Import shared settings and contracts
from config import GRID_X, GRID_Y, GRID_Z, FPS
from interfaces import Position3D, TelemetryData

# Import Team Modules
from module_1_ai.random_walk import RandomWalkAgent3D      # Member 1 (YOU)
from module_2.grid import Grid                              # Member 2
from module_3.pygame_renderer import SwarmDashboard3D       # Member 3


def run_simulation():
    # ----------------------------------------------------
    # 1. INITIALIZE ENVIRONMENT (Member 2)
    # ----------------------------------------------------
    env_grid = Grid(size=GRID_X)

    # Place obstacles on the ground layer
    env_grid.add_obstacle(5, 5)
    env_grid.add_obstacle(5, 6)
    env_grid.add_obstacle(6, 5)
    env_grid.add_obstacle(12, 8)
    env_grid.add_obstacle(12, 9)

    # Place survivors on the ground layer
    env_grid.add_survivor(10, 10)
    env_grid.add_survivor(15, 15)
    total_survivors = 2

    # Translate Member 2's 2D Grid into Member 3's 3D Matrix (Z=0 Ground Level)
    grid_3d = np.zeros((GRID_X, GRID_Y, GRID_Z), dtype=int)
    for r in range(GRID_X):
        for c in range(GRID_Y):
            grid_3d[r, c, 0] = env_grid.grid[r][c]

    visit_count_3d = np.zeros((GRID_X, GRID_Y, GRID_Z), dtype=int)

    # ----------------------------------------------------
    # 2. INITIALIZE AI DRONE SWARM (Member 1 - YOU)
    # ----------------------------------------------------
    # Create 3 Drones starting at different locations and altitudes
    drones = [
        {"agent": RandomWalkAgent3D(start_pos=(0, 0, 1)), "pos": Position3D(0, 0, 1), "battery": 100.0},
        {"agent": RandomWalkAgent3D(start_pos=(0, 19, 2)), "pos": Position3D(0, 19, 2), "battery": 95.0},
        {"agent": RandomWalkAgent3D(start_pos=(19, 0, 3)), "pos": Position3D(19, 0, 3), "battery": 90.0},
    ]

    # ----------------------------------------------------
    # 3. INITIALIZE 3D DASHBOARD UI (Member 3)
    # ----------------------------------------------------
    dashboard = SwarmDashboard3D()
    clock = pygame.time.Clock()

    survivors_found_set = set()
    step_number = 0
    running = True

    print("🚀 Launching 3D Swarm Simulation...")

    # ----------------------------------------------------
    # 4. MAIN GAME LOOP
    # ----------------------------------------------------
    while running:
        # --- Handle Pygame Window Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    dashboard.toggle_heatmap()  # Press 'H' to toggle heatmap!

        step_number += 1
        current_drone_positions = []
        current_drone_batteries = []

        # --- Update Each Drone (AI Step -> Env Step) ---
        for drone in drones:
            # 1. AI Decision (You)
            action = drone["agent"].get_action()

            # 2. Update Position
            new_pos = drone["agent"].predict_next_position(drone["pos"], action)
            drone["pos"] = new_pos

            # 3. Drain battery slightly per move
            drone["battery"] = max(0.0, drone["battery"] - 0.2)

            # Record position & visits
            current_drone_positions.append(drone["pos"])
            current_drone_batteries.append(drone["battery"])
            visit_count_3d[drone["pos"].x, drone["pos"].y, drone["pos"].z] += 1

            # Check if drone found a survivor at ground level (Z=0 or directly hovering above)
            if env_grid.is_survivor(drone["pos"].x, drone["pos"].y):
                survivors_found_set.add((drone["pos"].x, drone["pos"].y))

        # --- Calculate Telemetry Metrics ---
        visited_ground_cells = np.count_nonzero(np.sum(visit_count_3d, axis=2))
        coverage_pct = (visited_ground_cells / (GRID_X * GRID_Y)) * 100.0

        # --- Package Telemetry for Member 3's Dashboard ---
        telemetry = TelemetryData(
            grid_matrix=grid_3d,
            visit_count_matrix=visit_count_3d,
            drone_positions=current_drone_positions,
            drone_batteries=current_drone_batteries,
            active_paradigm="3D Random Walk Swarm",
            step_number=step_number,
            coverage_percentage=coverage_pct,
            survivors_found=len(survivors_found_set),
            total_survivors=total_survivors
        )

        # --- Render 3D Isometric Frame ---
        dashboard.render_frame(telemetry)
        clock.tick(FPS)

    pygame.quit()
    print("✅ Simulation ended cleanly.")


if __name__ == "__main__":
    run_simulation()