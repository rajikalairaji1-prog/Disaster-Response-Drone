"""
3D Disaster Response Environment

Member 2 - Environment Module

The environment represents a disaster area as a 3D grid.

X -> Left / Right
Y -> Forward / Backward
Z -> Altitude

0 = Empty
1 = Obstacle
2 = Survivor
"""

import sys
import os

# Allow importing interfaces.py from the root folder
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from interfaces import Action3D, Position3D, AgentState


class DisasterEnvironment:
    """
    3D disaster-response environment for reinforcement learning.

    The drone moves in six possible directions:
        FORWARD
        BACKWARD
        LEFT
        RIGHT
        ASCEND
        DESCEND
    """

    def __init__(
        self,
        grid_x=20,
        grid_y=20,
        grid_z=5,
        max_steps=1000
    ):

        # 3D grid dimensions
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_z = grid_z

        # Maximum steps
        self.max_steps = max_steps

        # Current step count
        self.steps = 0

        # Survivor information
        self.survivors = set()
        self.survivors_found = set()

        # Obstacles
        self.obstacles = set()

        # Episode status
        self.done = False

        # Drone starting position
        self.start_position = Position3D(0, 0, 0)

        self.position = self.start_position

        # Battery
        self.battery = 100

        # Create disaster scenario
        self.create_scenario()

    # ==================================================
    # CREATE SCENARIO
    # ==================================================

    def create_scenario(self):
        """
        Create obstacles and survivors in the 3D disaster area.
        """

        self.obstacles = {
            # Ground-level obstacles
            (5, 5, 0),
            (5, 6, 0),
            (6, 5, 0),

            (8, 10, 0),
            (8, 11, 0),
            (9, 10, 0),

            (12, 14, 0),
            (13, 14, 0),
            (14, 14, 0),

            # Obstacles at higher altitude
            (5, 5, 1),
            (5, 6, 1),

            (10, 10, 2),
            (10, 11, 2),

            (15, 15, 1)
        }

        self.survivors = {
            (2, 1, 0),
            (10, 10, 0),
            (15, 15, 1)
        }

        self.survivors_found = set()

    # ==================================================
    # GET STATE
    # ==================================================

    def get_state(self):
        """
        Return the current AgentState.
        """

        return AgentState(
            position=self.position,
            battery=self.battery,
            has_found_survivor=len(self.survivors_found) > 0
        )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):
        """
        Reset the environment.
        """

        self.position = self.start_position

        self.steps = 0

        self.battery = 100

        self.done = False

        self.create_scenario()

        return self.get_state()

    # ==================================================
    # VALID POSITION
    # ==================================================

    def is_valid_position(self, position):
        """
        Check whether a 3D position is inside the environment.
        """

        return (
            0 <= position.x < self.grid_x
            and
            0 <= position.y < self.grid_y
            and
            0 <= position.z < self.grid_z
        )

    # ==================================================
    # OBSTACLE CHECK
    # ==================================================

    def is_obstacle(self, position):
        """
        Check whether a position contains an obstacle.
        """

        return position.to_tuple() in self.obstacles

    # ==================================================
    # SURVIVOR CHECK
    # ==================================================

    def is_survivor(self, position):
        """
        Check whether a survivor exists at this position.
        """

        return (
            position.to_tuple() in self.survivors
            and
            position.to_tuple() not in self.survivors_found
        )

    # ==================================================
    # CALCULATE NEXT POSITION
    # ==================================================

    def calculate_next_position(self, action):
        """
        Calculate the position after performing an action.
        """

        x = self.position.x
        y = self.position.y
        z = self.position.z

        if action == Action3D.FORWARD:
            y += 1

        elif action == Action3D.BACKWARD:
            y -= 1

        elif action == Action3D.LEFT:
            x -= 1

        elif action == Action3D.RIGHT:
            x += 1

        elif action == Action3D.ASCEND:
            z += 1

        elif action == Action3D.DESCEND:
            z -= 1

        else:
            return self.position

        return Position3D(x, y, z)

    # ==================================================
    # STEP
    # ==================================================

    def step(self, action):
        """
        Execute one action.

        Returns:

            next_state
            reward
            done
            info
        """

        if self.done:
            return self.get_state(), 0, True, self.get_info()

        self.steps += 1

        # Battery decreases for every movement
        self.battery -= 1

        # Calculate destination
        next_position = self.calculate_next_position(action)

        # ----------------------------------------------
        # Boundary collision
        # ----------------------------------------------

        if not self.is_valid_position(next_position):

            reward = -10

            print(
                "Boundary collision:",
                next_position.to_tuple()
            )

            return (
                self.get_state(),
                reward,
                False,
                self.get_info()
            )

        # ----------------------------------------------
        # Obstacle collision
        # ----------------------------------------------

        if self.is_obstacle(next_position):

            reward = -10

            print(
                "Obstacle detected at:",
                next_position.to_tuple()
            )

            return (
                self.get_state(),
                reward,
                False,
                self.get_info()
            )

        # ----------------------------------------------
        # Move drone
        # ----------------------------------------------

        self.position = next_position

        # Normal movement penalty
        reward = -1

        # ----------------------------------------------
        # Survivor detection
        # ----------------------------------------------

        if self.is_survivor(next_position):

            survivor_position = next_position.to_tuple()

            self.survivors_found.add(survivor_position)

            reward = 100

            print(
                "SURVIVOR FOUND at:",
                survivor_position
            )

        # ----------------------------------------------
        # All survivors found
        # ----------------------------------------------

        if len(self.survivors_found) == len(self.survivors):

            self.done = True

            reward += 100

            print("ALL SURVIVORS FOUND!")

        # ----------------------------------------------
        # Maximum steps
        # ----------------------------------------------

        elif self.steps >= self.max_steps:

            self.done = True

            print("Maximum steps reached.")

        # ----------------------------------------------
        # Battery empty
        # ----------------------------------------------

        elif self.battery <= 0:

            self.done = True

            print("Drone battery depleted.")

        return (
            self.get_state(),
            reward,
            self.done,
            self.get_info()
        )

    # ==================================================
    # DISPLAY 3D ENVIRONMENT
    # ==================================================

    def display(self):
        """
        Display every Z layer of the 3D environment
        in the terminal.
        """

        print("\n")
        print("=" * 60)
        print("        3D DISASTER RESPONSE ENVIRONMENT")
        print("=" * 60)

        for z in range(self.grid_z):

            print(f"\n--- ALTITUDE Z = {z} ---")

            for y in range(self.grid_y):

                row = []

                for x in range(self.grid_x):

                    position = Position3D(x, y, z)

                    # Drone
                    if position == self.position:
                        row.append("D")

                    # Survivor
                    elif self.is_survivor(position):
                        row.append("S")

                    # Already found survivor
                    elif position.to_tuple() in self.survivors_found:
                        row.append("F")

                    # Obstacle
                    elif self.is_obstacle(position):
                        row.append("X")

                    # Empty
                    else:
                        row.append(".")

                print(" ".join(row))

        print("\nDrone Position:", self.position.to_tuple())
        print("Battery:", self.battery)
        print("Steps:", self.steps)
        print(
            "Survivors:",
            len(self.survivors_found),
            "/",
            len(self.survivors)
        )

    # ==================================================
    # INFORMATION
    # ==================================================

    def get_info(self):
        """
        Return useful environment information.
        """

        return {
            "drone_position": self.position.to_tuple(),
            "battery": self.battery,
            "steps": self.steps,
            "survivors_found": len(self.survivors_found),
            "total_survivors": len(self.survivors),
            "done": self.done
        }


# ======================================================
# TEST 3D ENVIRONMENT
# ======================================================

if __name__ == "__main__":

    print("=" * 60)
    print("      3D DISASTER RESPONSE ENVIRONMENT TEST")
    print("=" * 60)

    # Create environment
    env = DisasterEnvironment(
        grid_x=20,
        grid_y=20,
        grid_z=5,
        max_steps=100
    )

    # Display initial environment
    env.display()

    # Initial state
    state = env.get_state()

    print("\nInitial State:")
    print(state)

    # --------------------------------------------------
    # Test 3D movements
    # --------------------------------------------------

    actions = [
        Action3D.RIGHT,
        Action3D.FORWARD,
        Action3D.FORWARD,
        Action3D.ASCEND,
        Action3D.RIGHT,
        Action3D.DESCEND,
        Action3D.LEFT
    ]

    print("\nRunning 3D test actions...")

    for action in actions:

        next_state, reward, done, info = env.step(action)

        print(
            f"\nAction   : {action.name}"
        )

        print(
            f"Position : {next_state.position.to_tuple()}"
        )

        print(
            f"Reward   : {reward}"
        )

        print(
            f"Battery  : {next_state.battery}"
        )

        print(
            f"Done     : {done}"
        )

        if done:
            break

    # --------------------------------------------------
    # Final information
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("             ENVIRONMENT SUMMARY")
    print("=" * 60)

    print(env.get_info())

    print("=" * 60)