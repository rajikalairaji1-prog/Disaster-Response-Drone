# module_2/grid.py

"""
3D Disaster Grid

Represents the disaster area as a 3D grid.

Cell values:
    0 = Empty
    1 = Obstacle
    2 = Survivor

Coordinates:
    X = Left / Right
    Y = Forward / Backward
    Z = Altitude
"""


class Grid:
    """
    Represents the disaster area as a 3D grid.
    """

    def __init__(self, size_x=20, size_y=20, size_z=5):

        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z

        # Create empty 3D grid
        self.grid = [
            [
                [0 for _ in range(size_z)]
                for _ in range(size_y)
            ]
            for _ in range(size_x)
        ]

    # --------------------------------------------------
    # VALID POSITION
    # --------------------------------------------------

    def is_valid_position(self, x, y, z):
        """
        Check whether a 3D position is inside the grid.
        """

        return (
            0 <= x < self.size_x
            and
            0 <= y < self.size_y
            and
            0 <= z < self.size_z
        )

    # --------------------------------------------------
    # ADD OBSTACLE
    # --------------------------------------------------

    def add_obstacle(self, x, y, z=0):
        """
        Add an obstacle at the given 3D position.
        """

        if self.is_valid_position(x, y, z):

            self.grid[x][y][z] = 1

            return True

        return False

    # --------------------------------------------------
    # ADD SURVIVOR
    # --------------------------------------------------

    def add_survivor(self, x, y, z=0):
        """
        Add a survivor at the given 3D position.
        """

        if self.is_valid_position(x, y, z):

            self.grid[x][y][z] = 2

            return True

        return False

    # --------------------------------------------------
    # OBSTACLE CHECK
    # --------------------------------------------------

    def is_obstacle(self, x, y, z=0):
        """
        Check whether a position contains an obstacle.
        """

        if not self.is_valid_position(x, y, z):
            return False

        return self.grid[x][y][z] == 1

    # --------------------------------------------------
    # SURVIVOR CHECK
    # --------------------------------------------------

    def is_survivor(self, x, y, z=0):
        """
        Check whether a position contains a survivor.
        """

        if not self.is_valid_position(x, y, z):
            return False

        return self.grid[x][y][z] == 2

    # --------------------------------------------------
    # REMOVE SURVIVOR
    # --------------------------------------------------

    def remove_survivor(self, x, y, z=0):
        """
        Remove a survivor after the drone finds them.
        """

        if self.is_survivor(x, y, z):

            self.grid[x][y][z] = 0

            return True

        return False

    # --------------------------------------------------
    # GET CELL
    # --------------------------------------------------

    def get_cell(self, x, y, z):
        """
        Return the value of a cell.
        """

        if not self.is_valid_position(x, y, z):
            return None

        return self.grid[x][y][z]

    # --------------------------------------------------
    # SET CELL
    # --------------------------------------------------

    def set_cell(self, x, y, z, value):
        """
        Set a cell value manually.

        0 = Empty
        1 = Obstacle
        2 = Survivor
        """

        if not self.is_valid_position(x, y, z):
            return False

        if value not in (0, 1, 2):
            return False

        self.grid[x][y][z] = value

        return True

    # --------------------------------------------------
    # DISPLAY 3D GRID
    # --------------------------------------------------

    def display(self):
        """
        Display the 3D grid layer by layer.

        Each Z level represents one altitude.
        """

        print("\n================================")
        print("       3D DISASTER GRID")
        print("================================")

        for z in range(self.size_z):

            print(f"\nAltitude Z = {z}")
            print("-" * 50)

            for y in range(self.size_y):

                row = []

                for x in range(self.size_x):

                    value = self.grid[x][y][z]

                    if value == 0:
                        row.append(".")

                    elif value == 1:
                        row.append("X")

                    elif value == 2:
                        row.append("S")

                print(" ".join(row))

    # --------------------------------------------------
    # DISPLAY SPECIFIC LEVEL
    # --------------------------------------------------

    def display_level(self, z):
        """
        Display only one altitude level.
        """

        if not (0 <= z < self.size_z):

            print(f"Invalid altitude: {z}")

            return

        print(f"\n3D Grid - Altitude Z = {z}")
        print("-" * 50)

        for y in range(self.size_y):

            row = []

            for x in range(self.size_x):

                value = self.grid[x][y][z]

                if value == 0:
                    row.append(".")

                elif value == 1:
                    row.append("X")

                elif value == 2:
                    row.append("S")

            print(" ".join(row))

    # --------------------------------------------------
    # COUNT SURVIVORS
    # --------------------------------------------------

    def count_survivors(self):
        """
        Count all survivors currently present.
        """

        count = 0

        for x in range(self.size_x):

            for y in range(self.size_y):

                for z in range(self.size_z):

                    if self.grid[x][y][z] == 2:

                        count += 1

        return count

    # --------------------------------------------------
    # COUNT OBSTACLES
    # --------------------------------------------------

    def count_obstacles(self):
        """
        Count all obstacles currently present.
        """

        count = 0

        for x in range(self.size_x):

            for y in range(self.size_y):

                for z in range(self.size_z):

                    if self.grid[x][y][z] == 1:

                        count += 1

        return count


# ======================================================
# GRID TEST
# ======================================================

if __name__ == "__main__":

    print("========================================")
    print("        3D DISASTER GRID TEST")
    print("========================================")

    # Create 3D grid
    grid = Grid(
        size_x=20,
        size_y=20,
        size_z=5
    )

    # --------------------------------------------------
    # Add 3D obstacles
    # --------------------------------------------------

    grid.add_obstacle(5, 5, 0)
    grid.add_obstacle(5, 6, 0)
    grid.add_obstacle(6, 5, 0)

    # Obstacle at higher altitude
    grid.add_obstacle(8, 8, 1)
    grid.add_obstacle(8, 9, 1)

    # --------------------------------------------------
    # Add survivors
    # --------------------------------------------------

    grid.add_survivor(2, 1, 0)
    grid.add_survivor(10, 10, 1)
    grid.add_survivor(15, 15, 2)

    # --------------------------------------------------
    # Display grid
    # --------------------------------------------------

    grid.display()

    # --------------------------------------------------
    # Test functions
    # --------------------------------------------------

    print("\n========================================")
    print("          TESTING FUNCTIONS")
    print("========================================")

    print(
        "\nPosition (5,5,0) is obstacle:",
        grid.is_obstacle(5, 5, 0)
    )

    print(
        "Position (10,10,1) is survivor:",
        grid.is_survivor(10, 10, 1)
    )

    print(
        "Position (15,15,2) is survivor:",
        grid.is_survivor(15, 15, 2)
    )

    print(
        "Position (25,25,5) is valid:",
        grid.is_valid_position(25, 25, 5)
    )

    print(
        "Position (5,5,0) is valid:",
        grid.is_valid_position(5, 5, 0)
    )

    print(
        "\nTotal survivors:",
        grid.count_survivors()
    )

    print(
        "Total obstacles:",
        grid.count_obstacles()
    )

    # --------------------------------------------------
    # Test survivor removal
    # --------------------------------------------------

    print("\nRemoving survivor at (2,1,0)...")

    grid.remove_survivor(2, 1, 0)

    print(
        "Is survivor still present:",
        grid.is_survivor(2, 1, 0)
    )

    print(
        "Survivors remaining:",
        grid.count_survivors()
    )

    # --------------------------------------------------
    # Display one level
    # --------------------------------------------------

    grid.display_level(1)

    print("\n========================================")
    print("             TEST COMPLETE")
    print("========================================")