class Grid:
    def __init__(self, size=20):
        self.size = size

        # Cell meanings:
        # 0 = Empty
        # 1 = Obstacle
        # 2 = Survivor
        self.grid = [[0 for _ in range(size)] for _ in range(size)]

    def add_obstacle(self, row, col):
        if self.is_valid_position(row, col):
            self.grid[row][col] = 1

    def add_survivor(self, row, col):
        if self.is_valid_position(row, col):
            self.grid[row][col] = 2

    def is_valid_position(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def is_obstacle(self, row, col):
        return self.grid[row][col] == 1

    def is_survivor(self, row, col):
        return self.grid[row][col] == 2

    def display(self):
        for row in self.grid:
            print(row)


# Test the Grid
if __name__ == "__main__":
    grid = Grid()

    # Add obstacles
    grid.add_obstacle(5, 5)
    grid.add_obstacle(5, 6)
    grid.add_obstacle(6, 5)

    # Add survivor
    grid.add_survivor(10, 10)

    print("Disaster Grid:")
    grid.display()
    print("\nTesting functions:")

print("Position (5,5) is obstacle:",
      grid.is_obstacle(5, 5))

print("Position (10,10) is survivor:",
      grid.is_survivor(10, 10))

print("Position (25,25) is valid:",
      grid.is_valid_position(25, 25))