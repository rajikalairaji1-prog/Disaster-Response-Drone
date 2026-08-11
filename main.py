# main.py
import time
import pygame
from config import GRID_X, GRID_Y, GRID_Z
from module_1.random_walk import RandomWalkAgent3D
from module_2.grid import GridEnv3D
from module_3.pygame_renderer import PygameRenderer3D

def run_visual_test():
    # 1. Initialize Environment (Member 2), Agent (You), and Renderer (Member 3)
    env = GridEnv3D(dim_x=GRID_X, dim_y=GRID_Y, dim_z=GRID_Z)
    agent = RandomWalkAgent3D()
    renderer = PygameRenderer3D(grid_x=GRID_X, grid_y=GRID_Y, grid_z=GRID_Z)
    
    print("🚀 Launching Full 3D Visual Drone Test...")
    
    state = env.reset()
    running = True
    
    while running:
        # Check if user closed the Pygame window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Step 1: AI (You) picks a 3D action
        action = agent.get_action(state)
        
        # Step 2: Env (Member 2) updates drone physics & position
        next_state, reward, done = env.step(action)
        
        # Step 3: UI (Member 3) updates the Pygame display window
        renderer.render(next_state)
        
        state = next_state
        time.sleep(0.15) # Controls step delay on screen
        
        if done:
            print("🎉 Survivor Located!")
            time.sleep(2)
            break
            
    pygame.quit()

if __name__ == "__main__":
    run_visual_test()