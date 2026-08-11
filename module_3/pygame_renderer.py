# module_3/pygame_renderer.py
import pygame
import numpy as np
from config import GRID_X, GRID_Y, GRID_Z

# UI Screen Layout Constants
CELL_W = 40  # Isometric cell horizontal width diameter
CELL_H = 20  # Isometric cell vertical height diameter
SIDEBAR_W = 260
SCREEN_WIDTH = 950
SCREEN_HEIGHT = 700

# Color Configurations
COLOR_BG = (18, 20, 28)
COLOR_FLOOR_UNVISITED = (230, 235, 240)
COLOR_FLOOR_VISITED   = (160, 230, 170)
COLOR_HUD_PANEL       = (30, 34, 46)
COLOR_WHITE           = (255, 255, 255)

# 3D Solid Shading (Top face, Left face, Right face shadow)
BLOCK_TOP   = (90, 95, 105)
BLOCK_LEFT  = (65, 70, 80)
BLOCK_RIGHT = (45, 50, 60)

DRONE_COLORS = [(0, 140, 255), (255, 50, 120), (255, 210, 0)]

class SwarmDashboard3D:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Segoe UI", 15)
        self.font_bold = pygame.font.SysFont("Segoe UI", 16, bold=True)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("3D Disaster Response Swarm Telemetry Hub")
        
        # Center the 3D isometric anchor vector point on screen
        self.origin_x = (SCREEN_WIDTH - SIDEBAR_W) // 2
        self.origin_y = 120
        self.show_heatmap = False

    def toggle_heatmap(self):
        self.show_heatmap = not self.show_heatmap

    def to_iso(self, x, y, z=0):
        """
        Projects true 3D coordinates (x, y, z) into 2D isometric screen space.
        Drones use the z coordinate to dynamically hover or dive.
        """
        # Base translation for the flat horizontal plane
        iso_x = self.origin_x + (x - y) * (CELL_W // 2)
        iso_y = self.origin_y + (x + y) * (CELL_H // 2)
        
        # Scale z-axis coordinate value directly into vertical pixel displacements
        altitude_scale = 25  
        iso_y -= (z * altitude_scale)
        
        return iso_x, iso_y

    def draw_solid_block(self, x_pixel, y_pixel, height=30, color_top=BLOCK_TOP, color_left=BLOCK_LEFT, color_right=BLOCK_RIGHT):
        """Renders an extruded structural block solid asset with directional face shadows."""
        w_half = CELL_W // 2
        h_half = CELL_H // 2

        # 1. Left Vertical Face Polygon
        left_face = [(x_pixel, y_pixel), (x_pixel - w_half, y_pixel - h_half), (x_pixel - w_half, y_pixel - h_half - height), (x_pixel, y_pixel - height)]
        pygame.draw.polygon(self.screen, color_left, left_face)

        # 2. Right Vertical Face Polygon
        right_face = [(x_pixel, y_pixel), (x_pixel + w_half, y_pixel - h_half), (x_pixel + w_half, y_pixel - h_half - height), (x_pixel, y_pixel - height)]
        pygame.draw.polygon(self.screen, color_right, right_face)

        # 3. Top Horizontal Diamond Face Polygon
        top_face = [(x_pixel, y_pixel - height), (x_pixel - w_half, y_pixel - h_half - height), (x_pixel, y_pixel - CELL_H - height), (x_pixel + w_half, y_pixel - h_half - height)]
        pygame.draw.polygon(self.screen, color_top, top_face)
        pygame.draw.polygon(self.screen, (120, 125, 135), top_face, width=1)

    def render_frame(self, telemetry):
        self.screen.fill(COLOR_BG)
        
        # Ingest 3D matrices from Member 2's environment
        grid_3d = telemetry.grid_matrix                  # Dim: (GRID_X, GRID_Y, GRID_Z)
        heatmap_3d = telemetry.visit_count_matrix        # Dim: (GRID_X, GRID_Y, GRID_Z)

        # ─── LAYER 1: RENDER GROUND TILE MATRIX (z = 0 Base Layer) ───
        for x in range(GRID_X):
            for y in range(GRID_Y):
                cx, cy = self.to_iso(x, y, z=0)
                w_half = CELL_W // 2
                h_half = CELL_H // 2
                floor_diamond = [(cx, cy), (cx - w_half, cy - h_half), (cx, cy - CELL_H), (cx + w_half, cy - h_half)]

                # Look at ground level activity or scan profiles
                is_visited = np.any(heatmap_3d[x, y, :] > 0)
                
                if self.show_heatmap:
                    total_cell_visits = np.sum(heatmap_3d[x, y, :])
                    if total_cell_visits > 0:
                        intensity = min(255, 80 + (total_cell_visits * 30))
                        floor_color = (intensity, 45, 65)
                    else:
                        floor_color = COLOR_FLOOR_UNVISITED
                else:
                    floor_color = COLOR_FLOOR_VISITED if is_visited else COLOR_FLOOR_UNVISITED

                pygame.draw.polygon(self.screen, floor_color, floor_diamond)
                pygame.draw.polygon(self.screen, (42, 46, 56), floor_diamond, width=1)

        # ─── LAYER 2: RENDER 3D HEIGHT STRUCTURES (Obstacles & Survivors) ───
        for z in range(GRID_Z):
            for x in range(GRID_X):
                for y in range(GRID_Y):
                    cell_type = grid_3d[x, y, z]
                    if cell_type == 0:
                        continue
                        
                    # Calculate correct structural spatial depth offset for height rendering
                    cx, cy = self.to_iso(x, y, z=z)
                    
                    if cell_type == 1:    # 3D Debris / Building Block
                        self.draw_solid_block(cx, cy, height=25)
                    elif cell_type == 2:  # 3D Floating Rescue Target Survivor
                        self.draw_solid_block(cx, cy, height=12, color_top=(255, 90, 70), color_left=(220, 50, 40), color_right=(180, 30, 20))

        # ─── LAYER 3: RENDER FLOATING 3D DRONES WITH INTERACTIVE ALTITUDE LINES ───
        for idx, pos in enumerate(telemetry.drone_positions):
            # pos is a true 3D point array match: (x, y, z)
            dx, dy, dz = pos.x, pos.y, pos.z
            
            ground_x, ground_y = self.to_iso(dx, dy, z=0)  # Reference point flat on earth
            drone_x, drone_y = self.to_iso(dx, dy, z=dz)   # True 3D coordinate floating up in altitude

            # Draw ground projection shadow disk at earth level
            pygame.draw.ellipse(self.screen, (10, 12, 18, 140), (ground_x - 10, ground_y - 6, 20, 12))
            
            # Draw vertical altitude tether line connecting shadow to floating drone
            pygame.draw.line(self.screen, DRONE_COLORS[idx], (ground_x, ground_y), (drone_x, drone_y), 1)
            
            # Draw primary floating 3D agent sphere core
            pygame.draw.circle(self.screen, DRONE_COLORS[idx], (drone_x, drone_y), 8)
            pygame.draw.circle(self.screen, COLOR_WHITE, (drone_x, drone_y), 8, width=2)

        # ─── LAYER 4: SIDEBAR DASHBOARD DISPLAY UTILITY PANEL ───
        sidebar_panel = pygame.Rect(SCREEN_WIDTH - SIDEBAR_W, 0, SIDEBAR_W, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_HUD_PANEL, sidebar_panel)
        pygame.draw.line(self.screen, (55, 62, 80), (SCREEN_WIDTH - SIDEBAR_W, 0), (SCREEN_WIDTH - SIDEBAR_W, SCREEN_HEIGHT), 2)

        hud_strings = [
            ("3D SWARM MISSION DATA", True),
            (f"Strategy: {telemetry.active_paradigm}", False),
            (f"Runtime Step: {telemetry.step_number}", False),
            (f"Area Scanned: {telemetry.coverage_percentage:.2f}%", False),
            (f"Survivors Found: {telemetry.survivors_found}/{telemetry.total_survivors}", False),
            ("────────────────────", False),
            ("3D LIVE DRONE ALTITUDE", True),
            (f"Drone 1: (Z={telemetry.drone_positions[0].z}) {telemetry.drone_batteries[0]:.1f}%", False),
            (f"Drone 2: (Z={telemetry.drone_positions[1].z}) {telemetry.drone_batteries[1]:.1f}%", False),
            (f"Drone 3: (Z={telemetry.drone_positions[2].z}) {telemetry.drone_batteries[2]:.1f}%", False),
            ("────────────────────", False),
            ("DISPLAY SETTINGS", True),
            ("Press [H] to Toggle 3D Heatmap", False)
        ]

        text_y = 30
        for text, is_bold in hud_strings:
            font_face = self.font_bold if is_bold else self.font
            color = (0, 195, 255) if is_bold else COLOR_WHITE
            txt_surf = font_face.render(text, True, color)
            self.screen.blit(txt_surf, (SCREEN_WIDTH - SIDEBAR_W + 20, text_y))
            text_y += 26

        pygame.display.flip()