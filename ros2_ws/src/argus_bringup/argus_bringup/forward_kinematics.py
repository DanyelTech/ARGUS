
import math


# ARGUS v1 dimensions (metres)
BASE_HEIGHT = 0.08
SHOULDER_OFFSET = 0.03
UPPER_ARM_LENGTH = 0.20
FOREARM_LENGTH = 0.18
WRIST_LENGTH = 0.08


def forward_kinematics(theta1, theta2, theta3, theta4):
    """
    Calculate the tool-tip position relative to base_link.

    Joint angles must be supplied in radians.
    Returns (x, y, z) in metres.
    """

    # Cumulative pitch angles
    shoulder_angle = theta2
    elbow_angle = theta2 + theta3
    wrist_angle = theta2 + theta3 + theta4

    # Horizontal reach
    reach = (
        UPPER_ARM_LENGTH * math.sin(shoulder_angle)
        + FOREARM_LENGTH * math.sin(elbow_angle)
        + WRIST_LENGTH * math.sin(wrist_angle)
    )

    # Convert horizontal reach into X and Y
    x = reach * math.cos(theta1)
    y = reach * math.sin(theta1)

    # Calculate height
    z = (
        BASE_HEIGHT
        + SHOULDER_OFFSET
        + UPPER_ARM_LENGTH * math.cos(shoulder_angle)
        + FOREARM_LENGTH * math.cos(elbow_angle)
        + WRIST_LENGTH * math.cos(wrist_angle)
    )

    return x, y, z


if __name__ == "__main__":
    # Test configuration: all joints at zero
    angles = [0.0, 0.0, 0.0, 0.0]

    x, y, z = forward_kinematics(*angles)

    print("ARGUS Forward Kinematics")
    print(f"X: {x:.4f} m")
    print(f"Y: {y:.4f} m")
    print(f"Z: {z:.4f} m")
