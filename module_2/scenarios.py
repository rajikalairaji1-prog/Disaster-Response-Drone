from grid import Grid


class DisasterScenario:
    """
    Creates different 3D disaster scenarios
    for testing drone search algorithms.

    Coordinate system:
        X = Left / Right
        Y = Forward / Backward
        Z = Altitude

    Cell values:
        0 = Empty
        1 = Obstacle
        2 = Survivor
    """

    def __init__(self, grid_size=20, height=10):
        self.grid_size = grid_size
        self.height = height

    # --------------------------------------------------
    # SCENARIO 1: SIMPLE
    # --------------------------------------------------

    def simple_scenario(self):
        """
        Small number of obstacles and survivors.
        Useful for basic 3D testing.
        """

        grid = Grid(
            size=self.grid_size,
            height=self.height
        )

        # Obstacles: (x, y, z)
        obstacles = [
            (5, 5, 1),
            (5, 6, 1),
            (6, 5, 1),
            (8, 8, 2),
            (8, 9, 2)
        ]

        # Survivors: (x, y, z)
        survivors = [
            (2, 2, 0),
            (10, 10, 1),
            (15, 15, 2)
        ]

        self.add_obstacles(grid, obstacles)
        self.add_survivors(grid, survivors)

        return grid

    # --------------------------------------------------
    # SCENARIO 2: OBSTACLE HEAVY
    # --------------------------------------------------

    def obstacle_heavy_scenario(self):
        """
        Large number of obstacles distributed
        across different altitude levels.
        """

        grid = Grid(
            size=self.grid_size,
            height=self.height
        )

        obstacles = [

            # Ground-level wall
            (5, 3, 0),
            (5, 4, 0),
            (5, 5, 0),
            (5, 6, 0),
            (5, 7, 0),

            # Second-level wall
            (10, 10, 1),
            (10, 11, 1),
            (10, 12, 1),
            (10, 13, 1),
            (10, 14, 1),

            # Vertical structure
            (7, 12, 0),
            (8, 12, 0),
            (9, 12, 0),
            (10, 12, 0),
            (11, 12, 0),
            (12, 12, 0),

            # Higher altitude obstacles
            (14, 5, 2),
            (14, 6, 2),
            (15, 5, 2),
            (15, 6, 2),

            # High-level obstacles
            (16, 10, 3),
            (16, 11, 3),
            (17, 10, 3)
        ]

        survivors = [
            (3, 3, 0),
            (12, 15, 1),
            (17, 17, 2)
        ]

        self.add_obstacles(grid, obstacles)
        self.add_survivors(grid, survivors)

        return grid

    # --------------------------------------------------
    # SCENARIO 3: SURVIVOR DENSE
    # --------------------------------------------------

    def survivor_dense_scenario(self):
        """
        More survivors distributed across
        different 3D positions.
        """

        grid = Grid(
            size=self.grid_size,
            height=self.height
        )

        obstacles = [
            (7, 7, 0),
            (7, 8, 0),
            (8, 7, 0),

            (12, 12, 1),
            (12, 13, 1),

            (15, 15, 2),
            (15, 16, 2)
        ]

        survivors = [
            (2, 2, 0),
            (3, 8, 0),
            (5, 15, 1),
            (8, 3, 1),
            (10, 10, 1),
            (12, 17, 2),
            (15, 5, 2),
            (16, 12, 3),
            (18, 18, 3)
        ]

        self.add_obstacles(grid, obstacles)
        self.add_survivors(grid, survivors)

        return grid

    # --------------------------------------------------
    # SCENARIO 4: 3D MAZE
    # --------------------------------------------------

    def maze_scenario(self):
        """
        3D maze-like obstacle arrangement.
        Tests path planning and obstacle avoidance.
        """

        grid = Grid(
            size=self.grid_size,
            height=self.height
        )

        obstacles = []

        # X-Y walls at different Z levels

        # Wall at altitude 0
        for y in range(2, 8):
            obstacles.append((4, y, 0))

        # Wall at altitude 1
        for y in range(10, 17):
            obstacles.append((8, y, 1))

        # Wall at altitude 2
        for y in range(3, 10):
            obstacles.append((13, y, 2))

        # Horizontal wall at altitude 0
        for x in range(4, 10):
            obstacles.append((x, 8, 0))

        # Horizontal wall at altitude 1
        for x in range(10, 17):
            obstacles.append((x, 17, 1))

        # Additional upper-level wall
        for x in range(5, 12):
            obstacles.append((x, 12, 3))

        survivors = [
            (3, 2, 0),
            (9, 10, 1),
            (15, 15, 2),
            (18, 18, 3)
        ]

        self.add_obstacles(grid, obstacles)
        self.add_survivors(grid, survivors)

        return grid

    # --------------------------------------------------
    # SCENARIO 5: RANDOM-LIKE
    # --------------------------------------------------

    def random_scenario(self):
        """
        Creates a mixed 3D disaster environment.
        """

        grid = Grid(
            size=self.grid_size,
            height=self.height
        )

        obstacles = [
            (2, 5, 0),
            (2, 6, 0),
            (3, 5, 0),

            (6, 10, 1),
            (7, 10, 1),
            (8, 10, 1),

            (10, 4, 2),
            (10, 5, 2),
            (11, 5, 2),

            (13, 14, 1),
            (14, 14, 1),
            (15, 14, 1),

            (16, 7, 3),
            (16, 8, 3),
            (17, 8, 3)
        ]

        survivors = [
            (1, 15, 0),
            (6, 3, 1),
            (9, 17, 2),
            (13, 5, 2),
            (18, 18, 3)
        ]

        self.add_obstacles(grid, obstacles)
        self.add_survivors(grid, survivors)

        return grid

    # --------------------------------------------------
    # ADD OBSTACLES
    # --------------------------------------------------

    def add_obstacles(self, grid, obstacles):
        """
        Add 3D obstacles to the grid.
        """

        for x, y, z in obstacles:

            if grid.is_valid_position(x, y, z):
                grid.add_obstacle(x, y, z)

    # --------------------------------------------------
    # ADD SURVIVORS
    # --------------------------------------------------

    def add_survivors(self, grid, survivors):
        """
        Add survivors to the 3D grid.
        """

        for x, y, z in survivors:

            if grid.is_valid_position(x, y, z):

                # Do not place survivor on obstacle
                if not grid.is_obstacle(x, y, z):
                    grid.add_survivor(x, y, z)

    # --------------------------------------------------
    # DISPLAY SCENARIO
    # --------------------------------------------------

    def display(self, grid, name):
        """
        Display each altitude layer of the 3D scenario.
        """

        print("\n========================================")
        print("3D SCENARIO:", name)
        print("========================================")

        for z in range(self.height):

            print(f"\n--- ALTITUDE Z = {z} ---")

            for y in range(self.grid_size):

                row_data = []

                for x in range(self.grid_size):

                    if grid.is_obstacle(x, y, z):
                        row_data.append("X")

                    elif grid.is_survivor(x, y, z):
                        row_data.append("S")

                    else:
                        row_data.append(".")

                print(" ".join(row_data))


# ======================================================
# TEST SCENARIOS
# ======================================================

if __name__ == "__main__":

    print("========================================")
    print("     3D DISASTER SCENARIO TEST")
    print("========================================")

    scenarios = DisasterScenario(
        grid_size=20,
        height=5
    )

    # ------------------------------------------
    # Simple Scenario
    # ------------------------------------------

    grid = scenarios.simple_scenario()

    scenarios.display(
        grid,
        "Simple 3D Disaster Scenario"
    )

    # ------------------------------------------
    # Obstacle Heavy Scenario
    # ------------------------------------------

    grid = scenarios.obstacle_heavy_scenario()

    scenarios.display(
        grid,
        "3D Obstacle Heavy Scenario"
    )

    # ------------------------------------------
    # Survivor Dense Scenario
    # ------------------------------------------

    grid = scenarios.survivor_dense_scenario()

    scenarios.display(
        grid,
        "3D Survivor Dense Scenario"
    )

    print("\nAll 3D scenarios created successfully!")