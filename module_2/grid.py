class Grid:
    """
    Represents the disaster area as a 2D grid.

    Cell values:
        0 = Empty
        1 = Obstacle
        2 = Survivor
    """

    def __init__(self, size=20):
        self.size = size

        # Create empty grid
        self.grid = [
            [0 for _ in range(size)]
            for _ in range(size)
        ]

    def is_valid_position(self, row, col):
        """Check whether a position is inside the grid."""

        return (
            0 <= row < self.size
            and
            0 <= col < self.size
        )

    def add_obstacle(self, row, col):
        """Add an obstacle to the grid."""

        if self.is_valid_position(row, col):
            self.grid[row][col] = 1

    def add_survivor(self, row, col):
        """Add a survivor to the grid."""

        if self.is_valid_position(row, col):
            self.grid[row][col] = 2

    def is_obstacle(self, row, col):
        """Check whether a position contains an obstacle."""

        if not self.is_valid_position(row, col):
            return False

        return self.grid[row][col] == 1

    def is_survivor(self, row, col):
        """Check whether a position contains a survivor."""

        if not self.is_valid_position(row, col):
            return False

        return self.grid[row][col] == 2

    def display(self):
        """Display the disaster grid."""

        print("Disaster Grid:")

        for row in self.grid:
            print(row)


# ==================================================
# GRID TEST
# ==================================================

if __name__ == "__main__":

    grid = Grid(20)

    # Add obstacles
    grid.add_obstacle(5, 5)
    grid.add_obstacle(5, 6)
    grid.add_obstacle(6, 5)

    # Add survivor
    grid.add_survivor(10, 10)

    # Display grid
    grid.display()

    # Test functions
    print("\nTesting functions:")

    print(
        "Position (5,5) is obstacle:",
        grid.is_obstacle(5, 5)
    )

    print(
        "Position (10,10) is survivor:",
        grid.is_survivor(10, 10)
    )

    print(
        "Position (25,25) is valid:",
        grid.is_valid_position(25, 25)
    )
if __name__ == "__main__":

    grid = Grid(20)

    grid.add_obstacle(5, 5)

    print(grid.is_obstacle(5, 5))