from grid import Grid
from drone import Drone


class DisasterEnvironment:
    """
    Disaster Response Environment for Reinforcement Learning.

    Grid:
        0 = Empty
        1 = Obstacle
        2 = Survivor

    Actions:
        0 = UP
        1 = DOWN
        2 = LEFT
        3 = RIGHT
    """

    def __init__(self, grid_size=20):
        self.grid_size = grid_size

        # Create disaster grid
        self.grid = Grid(grid_size)

        # Create drone
        self.drone = Drone(
            row=0,
            col=0,
            drone_id=1
        )

        # Environment settings
        self.max_steps = grid_size * grid_size
        self.steps = 0

        # Number of survivors
        self.total_survivors = 0
        self.survivors_found = 0

        # Episode status
        self.done = False

        # Create default disaster scenario
        self.create_scenario()

    # --------------------------------------------------
    # CREATE DISASTER SCENARIO
    # --------------------------------------------------

    def create_scenario(self):
        """
        Create obstacles and survivors in the disaster area.
        """

        # Obstacles
        obstacles = [
            (5, 5),
            (5, 6),
            (6, 5),
            (8, 10),
            (8, 11),
            (9, 10),
            (12, 14),
            (13, 14),
            (14, 14)
        ]

        for row, col in obstacles:
            self.grid.add_obstacle(row, col)

        # Survivors
        survivors = [
            (2, 1),
            (10, 10),
            (15, 15)
        ]

        for row, col in survivors:
            self.grid.add_survivor(row, col)

        self.total_survivors = len(survivors)

    # --------------------------------------------------
    # GET STATE
    # --------------------------------------------------

    def get_state(self):
        """
        Return the current state of the drone.

        State:
            (drone_row, drone_col)
        """

        return (
            self.drone.row,
            self.drone.col
        )

    # --------------------------------------------------
    # RESET ENVIRONMENT
    # --------------------------------------------------

    def reset(self):
        """
        Reset the environment for a new episode.
        """

        self.grid = Grid(self.grid_size)

        self.drone = Drone(
            row=0,
            col=0,
            drone_id=1
        )

        self.steps = 0
        self.survivors_found = 0
        self.done = False

        # Recreate disaster scenario
        self.create_scenario()

        return self.get_state()

    # --------------------------------------------------
    # STEP
    # --------------------------------------------------

    def step(self, action):
        """
        Execute one action in the environment.

        Returns:
            next_state
            reward
            done
        """

        if self.done:
            return self.get_state(), 0, True

        self.steps += 1

        # Store old position
        old_position = self.drone.get_position()

        # Check whether destination contains survivor
        new_row = self.drone.row
        new_col = self.drone.col

        if action == Drone.UP:
            new_row -= 1

        elif action == Drone.DOWN:
            new_row += 1

        elif action == Drone.LEFT:
            new_col -= 1

        elif action == Drone.RIGHT:
            new_col += 1

        else:
            return self.get_state(), -10, False

        # --------------------------------------------------
        # Boundary collision
        # --------------------------------------------------

        if not self.grid.is_valid_position(new_row, new_col):

            reward = -10

            print("Boundary reached.")

            return self.get_state(), reward, False

        # --------------------------------------------------
        # Obstacle collision
        # --------------------------------------------------

        if self.grid.is_obstacle(new_row, new_col):

            reward = -10

            print(
                f"Obstacle detected at "
                f"({new_row}, {new_col})"
            )

            return self.get_state(), reward, False

        # --------------------------------------------------
        # Move drone
        # --------------------------------------------------

        self.drone.row = new_row
        self.drone.col = new_col

        # Normal movement reward
        reward = -1

        # --------------------------------------------------
        # Survivor detection
        # --------------------------------------------------

        if self.grid.is_survivor(new_row, new_col):

            reward = 100

            self.survivors_found += 1

            # Remove survivor after finding it
            self.grid.grid[new_row][new_col] = 0

            print(
                f"Survivor found at "
                f"({new_row}, {new_col})!"
            )

        # --------------------------------------------------
        # Check termination
        # --------------------------------------------------

        if self.survivors_found == self.total_survivors:

            self.done = True

            reward += 100

            print("All survivors found!")

        elif self.steps >= self.max_steps:

            self.done = True

            print("Maximum steps reached.")

        # Get new state
        next_state = self.get_state()

        return next_state, reward, self.done

    # --------------------------------------------------
    # DISPLAY ENVIRONMENT
    # --------------------------------------------------

    def display(self):
        """
        Display the disaster grid and drone position.
        """

        print("\nDisaster Environment:")

        for row in range(self.grid_size):

            row_data = []

            for col in range(self.grid_size):

                # Drone
                if (
                    row == self.drone.row
                    and col == self.drone.col
                ):
                    row_data.append("D")

                # Obstacle
                elif self.grid.is_obstacle(row, col):
                    row_data.append("X")

                # Survivor
                elif self.grid.is_survivor(row, col):
                    row_data.append("S")

                # Empty
                else:
                    row_data.append(".")

            print(" ".join(row_data))

        print("\nDrone position:", self.drone.get_position())
        print("Steps:", self.steps)
        print(
            "Survivors found:",
            self.survivors_found,
            "/",
            self.total_survivors
        )

    # --------------------------------------------------
    # INFORMATION
    # --------------------------------------------------

    def get_info(self):
        """
        Return useful environment information.
        """

        return {
            "drone_position": self.drone.get_position(),
            "steps": self.steps,
            "survivors_found": self.survivors_found,
            "total_survivors": self.total_survivors,
            "done": self.done
        }


# ======================================================
# TEST DISASTER ENVIRONMENT
# ======================================================

if __name__ == "__main__":

    print("========================================")
    print("   DISASTER RESPONSE ENVIRONMENT TEST")
    print("========================================")

    # Create environment
    env = DisasterEnvironment(grid_size=20)

    # Display initial environment
    env.display()

    # Get initial state
    state = env.get_state()

    print("\nInitial State:", state)

    # --------------------------------------------------
    # Test actions
    # --------------------------------------------------

    actions = [
        Drone.RIGHT,
        Drone.DOWN,
        Drone.DOWN,
        Drone.RIGHT,
        Drone.DOWN
    ]

    print("\nRunning test actions...")

    for action in actions:

        next_state, reward, done = env.step(action)

        print(
            "Action:",
            action,
            "| State:",
            next_state,
            "| Reward:",
            reward,
            "| Done:",
            done
        )

        if done:
            break

    # Final information
    print("\n========================================")
    print("           ENVIRONMENT SUMMARY")
    print("========================================")

    print(env.get_info())

    print("========================================")