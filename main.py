# main.py
import time
from interfaces import Position3D, AgentState
from module_1.random_walk import RandomWalkAgent3D

def test_3d_random_walk():
    agent = RandomWalkAgent3D(start_pos=(0, 0, 0))
    current_pos = Position3D(0, 0, 0)
    
    print("🚀 Starting 3D Random Walk Drone Test...\n")
    
    for step in range(1, 11):
        # 1. Agent picks random action
        action = agent.get_action()
        
        # 2. Update position
        current_pos = agent.predict_next_position(current_pos, action)
        
        print(f"Step {step:02d} | Action: {action.name:<8} | Drone Position (X,Y,Z): {current_pos.to_tuple()}")
        time.sleep(0.2)

if __name__ == "__main__":
    test_3d_random_walk()