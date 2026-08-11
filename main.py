# main.py
import random
import pygame
import numpy as np

# Config & Contracts
from config import (
    GRID_X, GRID_Y, GRID_Z, 
    NUM_DRONES, INITIAL_BATTERY, BATTERY_DRAIN_PER_STEP,
    MAX_STEPS_PER_EPISODE, START_POSITION, SURVIVOR_POSITION, 
    FPS
)
from interfaces import Action3D, Position3D, AgentState, TelemetryData

# Team Modules
from module_2.grid import Grid
from module_3.pygame_renderer import SwarmDashboard3D


def apply_action(pos: Position3D, action: Action3D) -> Position3D:
    """Calculates the target position given an Action3D move."""
    dx, dy, dz = 0, 0, 0

    if action == Action3D.RIGHT:
        dx = 1  # +X
    elif action == Action3D.LEFT:
        dx = -1  # -X
    elif action == Action3D.FORWARD:
        dy = 1  # +Y
    elif action == Action3D.BACKWARD:
        dy = -1  # -Y
    elif action == Action3D.ASCEND:
        dz = 1  # +Z
    elif action == Action3D.DESCEND:
        dz = -1  # -Z

    new_x = max(0, min(GRID_X - 1, pos.x + dx))
    new_y = max(0, min(GRID_Y - 1, pos.y + dy))
    new_z = max(0, min(GRID_Z - 1, pos.z + dz))

    return Position3D(new_x, new_y, new_z)


def run_simulation():
    # ----------------------------------------------------
    # 1. ENVIRONMENT SETUP (Member 2 Grid -> 3D Space)
    # ----------------------------------------------------
    env_2d = Grid(size=GRID_X)  # 10x10 Grid from config

    # Add ground obstacles from Member 2's style
    env_2d.add_obstacle(3, 3)
    env_2d.add_obstacle(3, 4)
    env_2d.add_obstacle(4, 3)

    # Convert 2D Grid to 3D matrix for Member 3's UI
    grid_3d = np.zeros((GRID_X, GRID_Y, GRID_Z), dtype=int)

    # Populate Z=0 Ground level obstacles from Member 2's Grid
    for x in range(GRID_X):
        for y in range(GRID_Y):
            grid_3d[x, y, 0] = env_2d.grid[x][y]

    # Place Survivor defined in config.py (e.g., at x=8, y=8, z=2)
    surv_x, surv_y, surv_z = SURVIVOR_POSITION
    grid_3d[surv_x, surv_y, surv_z] = 2

    visit_count_3d = np.zeros((GRID_X, GRID_Y, GRID_Z), dtype=int)

    # ----------------------------------------------------
    # 2. DRONE SWARM INITIALIZATION (Member 1 AI Agents)
    # ----------------------------------------------------
    start_pos = Position3D(*START_POSITION)

    # 3 Drones starting near base position at different altitudes
    drones = [
        AgentState(
            position=Position3D(start_pos.x, start_pos.y, 1),
            battery=INITIAL_BATTERY,
        ),
        AgentState(
            position=Position3D(start_pos.x + 1, start_pos.y, 2),
            battery=INITIAL_BATTERY,
        ),
        AgentState(
            position=Position3D(start_pos.x, start_pos.y + 1, 3),
            battery=INITIAL_BATTERY,
        ),
    ]

    # ----------------------------------------------------
    # 3. UI DASHBOARD (Member 3 Renderer)
    # ----------------------------------------------------
    dashboard = SwarmDashboard3D()
    clock = pygame.time.Clock()

    survivors_found = 0
    total_survivors = 1
    step_number = 0
    running = True

    print(
        f"🚀 Simulation active with 3D Grid size ({GRID_X}x{GRID_Y}x{GRID_Z})..."
    )

    # ----------------------------------------------------
    # 4. SIMULATION LOOP
    # ----------------------------------------------------
    while running and step_number < MAX_STEPS_PER_EPISODE:
        # Handle Pygame UI Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    dashboard.toggle_heatmap()

        step_number += 1
        actions = list(Action3D)

        current_positions = []
        current_batteries = []

        # Update each drone state
        for idx, drone in enumerate(drones):
            if drone.battery <= 0:
                current_positions.append(drone.position)
                current_batteries.append(0)
                continue

            # 1. Choose action (Random movement policy for demonstration)
            chosen_action = random.choice(actions)

            # 2. Calculate next move
            next_pos = apply_action(drone.position, chosen_action)

            # 3. Update drone state & drain battery
            drone.position = next_pos
            drone.battery = max(0, drone.battery - 1)

            # 4. Check survivor discovery match
            if (
                drone.position.x == surv_x
                and drone.position.y == surv_y
                and drone.position.z == surv_z
            ):
                drone.has_found_survivor = True
                survivors_found = 1

            # Log step in heat-map
            visit_count_3d[next_pos.x, next_pos.y, next_pos.z] += 1

            current_positions.append(drone.position)
            current_batteries.append(float(drone.battery))

        # Calculate visited coverage percentage across ground level
        visited_cells = np.count_nonzero(np.sum(visit_count_3d, axis=2))
        coverage_pct = (visited_cells / (GRID_X * GRID_Y)) * 100.0

        # Construct Telemetry Payload for UI
        telemetry = TelemetryData(
            grid_matrix=grid_3d,
            visit_count_matrix=visit_count_3d,
            drone_positions=current_positions,
            drone_batteries=current_batteries,
            active_paradigm="3D Random Explorer",
            step_number=step_number,
            coverage_percentage=coverage_pct,
            survivors_found=survivors_found,
            total_survivors=total_survivors,
        )

        # Render dashboard frame
        dashboard.render_frame(telemetry)
        clock.tick(8)  # 8 FPS execution speed

    pygame.quit()
    print("✅ Run completed.")


if __name__ == "__main__":
    run_simulation()    