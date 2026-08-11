from grid import Grid


class DisasterScenario:
    """
    Creates different disaster scenarios for testing
    drone search algorithms.

    Grid values:
        0 = Empty
        1 = Obstacle
        2 = Survivor
    """

    def __init__(self, grid_size=20):
        self.grid_size = grid_size

    # --------------------------------------------------
    # SCENARIO 1: SIMPLE
    # --------------------------------------------------

    def simple_scenario(self):
        """
        Small number of obstacles and survivors.
        Useful for basic testing.
        """

        grid = Grid(self.grid_size)

        obstacles = [
            (5, 5),
            (5, 6),
            (6, 5)
        ]

        survivors = [
            (2, 2),
            (10, 10),
            (15, 15)
        ]

        self.add_obstacles(grid, obstacles)
        self.add_survivors(grid, survivors)

        return grid

    # --------------------------------------------------
    # SCENARIO 2: OBSTACLE HEAVY
    # --------------------------------------------------

    def obstacle_heavy_scenario(self):
        """
        Large number of obstacles.
        Tests the drone's ability to avoid obstacles.
        """

        grid = Grid(self.grid_size)

        obstacles = [
            # Horizontal wall
            (5, 3),
            (5, 4),
            (5, 5),
            (5, 6),
            (5, 7),

            # Second wall
            (10, 10),
            (10, 11),
            (10, 12),
            (10, 13),
            (10, 14),

            # Vertical wall
            (7, 12),
            (8, 12),
            (9, 12),
            (10, 12),
            (11, 12),
            (12, 12),

            # Additional obstacles
            (14, 5),
            (14, 6),
            (15, 5),
            (15, 6)
        ]

        survivors = [
            (3, 3),
            (12, 15),
            (17, 17)
        ]

        self.add_obstacles(grid, obstacles)
        self.add_survivors(grid, survivors)

        return grid

    # --------------------------------------------------
    # SCENARIO 3: SURVIVOR DENSE
    # --------------------------------------------------

    def survivor_dense_scenario(self):
        """
        More survivors with fewer obstacles.
        Tests survivor detection efficiency.
        """

        grid = Grid(self.grid_size)

        obstacles = [
            (7, 7),
            (7, 8),
            (8, 7),
            (12, 12),
            (12, 13)
        ]

        survivors = [
            (2, 2),
            (3, 8),
            (5, 15),
            (8, 3),
            (10, 10),
            (12, 17),
            (15, 5),
            (16, 12),
            (18, 18)
        ]

        self.add_obstacles(grid, obstacles)
        self.add_survivors(grid, survivors)

        return grid

    # --------------------------------------------------
    # SCENARIO 4: MAZE
    # --------------------------------------------------

    def maze_scenario(self):
        """
        Maze-like obstacle arrangement.
        Tests path planning and obstacle avoidance.
        """

        grid = Grid(self.grid_size)

        obstacles = []

        # Vertical walls
        for row in range(2, 8):
            obstacles.append((row, 4))

        for row in range(10, 17):
            obstacles.append((row, 8))

        for row in range(3, 10):
            obstacles.append((row, 13))

        # Horizontal walls
        for col in range(4, 10):
            obstacles.append((8, col))

        for col in range(10, 17):
            obstacles.append((17, col))

        survivors = [
            (3, 2),
            (9, 10),
            (15, 15)
        ]

        self.add_obstacles(grid, obstacles)
        self.add_survivors(grid, survivors)

        return grid

    # --------------------------------------------------
    # RANDOM-LIKE SCENARIO
    # --------------------------------------------------

    def random_scenario(self):
        """
        Creates a larger mixed disaster environment.
        """

        grid = Grid(self.grid_size)

        obstacles = [
            (2, 5),
            (2, 6),
            (3, 5),
            (6, 10),
            (7, 10),
            (8, 10),
            (10, 4),
            (10, 5),
            (11, 5),
            (13, 14),
            (14, 14),
            (15, 14),
            (16, 7),
            (16, 8),
            (17, 8)
        ]

        survivors = [
            (1, 15),
            (6, 3),
            (9, 17),
            (13, 5),
            (18, 18)
        ]

        self.add_obstacles(grid, obstacles)
        self.add_survivors(grid, survivors)

        return grid

    # --------------------------------------------------
    # ADD OBSTACLES
    # --------------------------------------------------

    def add_obstacles(self, grid, obstacles):
        """
        Add obstacles to the grid.
        """

        for row, col in obstacles:

            if grid.is_valid_position(row, col):
                grid.add_obstacle(row, col)

    # --------------------------------------------------
    # ADD SURVIVORS
    # --------------------------------------------------

    def add_survivors(self, grid, survivors):
        """
        Add survivors to the grid.
        """

        for row, col in survivors:

            if grid.is_valid_position(row, col):

                # Do not place survivor on obstacle
                if not grid.is_obstacle(row, col):
                    grid.add_survivor(row, col)

    # --------------------------------------------------
    # DISPLAY SCENARIO
    # --------------------------------------------------

    def display(self, grid, name):
        """
        Display a scenario.
        """

        print("\n========================================")
        print("SCENARIO:", name)
        print("========================================")

        for row in range(self.grid_size):

            row_data = []

            for col in range(self.grid_size):

                if grid.is_obstacle(row, col):
                    row_data.append("X")

                elif grid.is_survivor(row, col):
                    row_data.append("S")

                else:
                    row_data.append(".")

            print(" ".join(row_data))


# ======================================================
# TEST SCENARIOS
# ======================================================

if __name__ == "__main__":

    print("========================================")
    print("     DISASTER SCENARIO TEST")
    print("========================================")

    scenarios = DisasterScenario(20)

    # ------------------------------------------
    # Test Simple Scenario
    # ------------------------------------------

    grid = scenarios.simple_scenario()

    scenarios.display(
        grid,
        "Simple Disaster Scenario"
    )

    # ------------------------------------------
    # Test Obstacle Heavy Scenario
    # ------------------------------------------

    grid = scenarios.obstacle_heavy_scenario()

    scenarios.display(
        grid,
        "Obstacle Heavy Scenario"
    )

    # ------------------------------------------
    # Test Survivor Dense Scenario
    # ------------------------------------------

    grid = scenarios.survivor_dense_scenario()

    scenarios.display(
        grid,
        "Survivor Dense Scenario"
    )

    print("\nAll scenarios created successfully!")