# module_2/drone.py

"""
3D Autonomous Drone for Disaster Response System.

The drone moves in:
    X-axis -> LEFT / RIGHT
    Y-axis -> FORWARD / BACKWARD
    Z-axis -> ASCEND / DESCEND
"""

from interfaces import Action3D, Position3D


class Drone:
    """
    Represents an autonomous drone in a 3D disaster area.
    """

    def __init__(self, x=0, y=0, z=0, drone_id=1):
        self.drone_id = drone_id

        # 3D position
        self.x = x
        self.y = y
        self.z = z

        # Statistics
        self.survivors_found = 0
        self.steps = 0

    # --------------------------------------------------
    # GET POSITION
    # --------------------------------------------------

    def get_position(self):
        """
        Return the current 3D position.
        """
        return Position3D(
            self.x,
            self.y,
            self.z
        )

    # --------------------------------------------------
    # MOVE DRONE
    # --------------------------------------------------

    def move(self, action, grid):
        """
        Move the drone according to the selected 3D action.

        Returns:
            True  -> movement successful
            False -> movement blocked
        """

        # Current position
        new_x = self.x
        new_y = self.y
        new_z = self.z

        # --------------------------------------------------
        # Calculate new position
        # --------------------------------------------------

        if action == Action3D.FORWARD:
            new_y += 1

        elif action == Action3D.BACKWARD:
            new_y -= 1

        elif action == Action3D.LEFT:
            new_x -= 1

        elif action == Action3D.RIGHT:
            new_x += 1

        elif action == Action3D.ASCEND:
            new_z += 1

        elif action == Action3D.DESCEND:
            new_z -= 1

        else:
            print("Invalid 3D action")
            return False

        # --------------------------------------------------
        # Check boundary
        # --------------------------------------------------

        if not grid.is_valid_position(new_x, new_y, new_z):

            print(
                f"Drone {self.drone_id}: "
                f"Move blocked - outside 3D grid "
                f"at ({new_x}, {new_y}, {new_z})"
            )

            return False

        # --------------------------------------------------
        # Check obstacle
        # --------------------------------------------------

        if grid.is_obstacle(new_x, new_y, new_z):

            print(
                f"Drone {self.drone_id}: "
                f"Move blocked - obstacle at "
                f"({new_x}, {new_y}, {new_z})"
            )

            return False

        # --------------------------------------------------
        # Move drone
        # --------------------------------------------------

        self.x = new_x
        self.y = new_y
        self.z = new_z

        self.steps += 1

        print(
            f"Drone {self.drone_id} moved to "
            f"({self.x}, {self.y}, {self.z})"
        )

        # --------------------------------------------------
        # Check survivor
        # --------------------------------------------------

        if grid.is_survivor(
            self.x,
            self.y,
            self.z
        ):

            self.survivors_found += 1

            print(
                f"Survivor detected at "
                f"({self.x}, {self.y}, {self.z})!"
            )

            return True

        return True

    # --------------------------------------------------
    # GET STEPS
    # --------------------------------------------------

    def get_steps(self):
        """
        Return number of successful movements.
        """
        return self.steps

    # --------------------------------------------------
    # GET SURVIVORS
    # --------------------------------------------------

    def get_survivors_found(self):
        """
        Return number of survivors found.
        """
        return self.survivors_found

    # --------------------------------------------------
    # RESET DRONE
    # --------------------------------------------------

    def reset(self, x=0, y=0, z=0):
        """
        Reset drone to starting position.
        """

        self.x = x
        self.y = y
        self.z = z

        self.steps = 0
        self.survivors_found = 0


# ======================================================
# TEST 3D DRONE
# ======================================================

if __name__ == "__main__":

    print("========================================")
    print("       3D DRONE MOVEMENT TEST")
    print("========================================")

    print("\nNote:")
    print("This test requires a 3D grid object")
    print("with the following methods:")
    print("is_valid_position(x, y, z)")
    print("is_obstacle(x, y, z)")
    print("is_survivor(x, y, z)")

    # --------------------------------------------------
    # Create a simple test grid
    # --------------------------------------------------

    class TestGrid:

        def __init__(self):
            self.size_x = 10
            self.size_y = 10
            self.size_z = 5

            self.obstacles = {
                (2, 2, 0),
                (3, 2, 0),
                (3, 3, 1)
            }

            self.survivors = {
                (1, 2, 0),
                (4, 4, 2)
            }

        def is_valid_position(self, x, y, z):

            return (
                0 <= x < self.size_x
                and
                0 <= y < self.size_y
                and
                0 <= z < self.size_z
            )

        def is_obstacle(self, x, y, z):

            return (x, y, z) in self.obstacles

        def is_survivor(self, x, y, z):

            return (x, y, z) in self.survivors

    # Create grid
    grid = TestGrid()

    # Create drone
    drone = Drone(
        x=0,
        y=0,
        z=0,
        drone_id=1
    )

    print(
        "\nInitial position:",
        drone.get_position().to_tuple()
    )

    # --------------------------------------------------
    # Test 1: RIGHT
    # --------------------------------------------------

    print("\n1. Moving RIGHT")

    drone.move(
        Action3D.RIGHT,
        grid
    )

    # --------------------------------------------------
    # Test 2: FORWARD
    # --------------------------------------------------

    print("\n2. Moving FORWARD")

    drone.move(
        Action3D.FORWARD,
        grid
    )

    # --------------------------------------------------
    # Test 3: ASCEND
    # --------------------------------------------------

    print("\n3. Moving ASCEND")

    drone.move(
        Action3D.ASCEND,
        grid
    )

    # --------------------------------------------------
    # Test 4: RIGHT
    # --------------------------------------------------

    print("\n4. Moving RIGHT")

    drone.move(
        Action3D.RIGHT,
        grid
    )

    # --------------------------------------------------
    # Test 5: FORWARD
    # --------------------------------------------------

    print("\n5. Moving FORWARD")

    drone.move(
        Action3D.FORWARD,
        grid
    )

    # --------------------------------------------------
    # Final summary
    # --------------------------------------------------

    print("\n========================================")
    print("           DRONE SUMMARY")
    print("========================================")

    print(
        "Drone ID:",
        drone.drone_id
    )

    print(
        "Final Position:",
        drone.get_position().to_tuple()
    )

    print(
        "Steps:",
        drone.get_steps()
    )

    print(
        "Survivors Found:",
        drone.get_survivors_found()
    )

    print("========================================")