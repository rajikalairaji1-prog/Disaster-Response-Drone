from grid import Grid


class Drone:
    """
    Represents an autonomous drone in the disaster area.
    """

    # Movement actions
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __init__(self, row=0, col=0, drone_id=1):
        self.drone_id = drone_id
        self.row = row
        self.col = col
        self.survivors_found = 0
        self.steps = 0

    def get_position(self):
        """Return current drone position."""
        return self.row, self.col

    def move(self, action, grid):
        """
        Move the drone in the selected direction.

        Returns:
            True  - movement successful
            False - movement blocked
        """

        new_row = self.row
        new_col = self.col

        # Calculate new position
        if action == self.UP:
            new_row -= 1

        elif action == self.DOWN:
            new_row += 1

        elif action == self.LEFT:
            new_col -= 1

        elif action == self.RIGHT:
            new_col += 1

        else:
            print("Invalid action")
            return False

        # Check whether position is inside the grid
        if not grid.is_valid_position(new_row, new_col):
            print(
                f"Drone {self.drone_id}: "
                f"Move blocked - outside grid"
            )
            return False

        # Check for obstacle
        if grid.is_obstacle(new_row, new_col):
            print(
                f"Drone {self.drone_id}: "
                f"Move blocked - obstacle at "
                f"({new_row}, {new_col})"
            )
            return False

        # Move drone
        self.row = new_row
        self.col = new_col
        self.steps += 1

        print(
            f"Drone {self.drone_id} moved to "
            f"({self.row}, {self.col})"
        )

        # Check for survivor
        if grid.is_survivor(self.row, self.col):
            self.survivors_found += 1

            print(
                f"Survivor detected at "
                f"({self.row}, {self.col})!"
            )

        return True

    def get_steps(self):
        """Return number of successful movements."""
        return self.steps

    def get_survivors_found(self):
        """Return number of survivors found."""
        return self.survivors_found


# --------------------------------------------------
# TEST DRONE
# --------------------------------------------------

if __name__ == "__main__":

    print("================================")
    print("   DRONE MOVEMENT TEST")
    print("================================")

    # Create 20 x 20 disaster grid
    grid = Grid(20)

    # Add obstacles
    grid.add_obstacle(1, 2)
    grid.add_obstacle(2, 2)
    grid.add_obstacle(3, 3)

    # Add survivor
    grid.add_survivor(2, 1)

    # Create drone at (0, 0)
    drone = Drone(
        row=0,
        col=0,
        drone_id=1
    )

    print(
        "\nInitial position:",
        drone.get_position()
    )

    # ------------------------------------------
    # Test 1: Move RIGHT
    # ------------------------------------------

    print("\n1. Moving RIGHT")

    drone.move(Drone.RIGHT, grid)

    # ------------------------------------------
    # Test 2: Move DOWN
    # ------------------------------------------

    print("\n2. Moving DOWN")

    drone.move(Drone.DOWN, grid)

    # ------------------------------------------
    # Test 3: Move DOWN
    # ------------------------------------------

    print("\n3. Moving DOWN")

    drone.move(Drone.DOWN, grid)

    # ------------------------------------------
    # Test 4: Move RIGHT
    # ------------------------------------------

    print("\n4. Moving RIGHT")

    drone.move(Drone.RIGHT, grid)

    # ------------------------------------------
    # Test 5: Move DOWN
    # ------------------------------------------

    print("\n5. Moving DOWN")

    drone.move(Drone.DOWN, grid)

    # ------------------------------------------
    # Test 6: Try obstacle
    # ------------------------------------------

    print("\n6. Testing obstacle collision")

    drone.move(Drone.UP, grid)

    # ------------------------------------------
    # Final information
    # ------------------------------------------

    print("\n================================")
    print("        DRONE SUMMARY")
    print("================================")

    print(
        "Drone ID:",
        drone.drone_id
    )

    print(
        "Final position:",
        drone.get_position()
    )

    print(
        "Steps:",
        drone.get_steps()
    )

    print(
        "Survivors found:",
        drone.get_survivors_found()
    )

    print("================================")