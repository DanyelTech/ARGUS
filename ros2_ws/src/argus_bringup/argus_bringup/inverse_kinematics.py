import math
from argus_bringup.forward_kinematics import forward_kinematics

# ARGUS v1 dimensions (metres)
SHOULDER_HEIGHT = 0.11
UPPER_ARM_LENGTH = 0.20
FOREARM_LENGTH = 0.18
WRIST_LENGTH = 0.08


JOINT_LIMITS = [
    (-3.14, 3.14),  # Base
    (-1.57, 1.57),  # Shoulder
    (-2.35, 2.35),  # Elbow
    (-1.57, 1.57),  # Wrist
]


def within_joint_limits(angles):
    for angle, (minimum, maximum) in zip(angles, JOINT_LIMITS):
        if not minimum <= angle <= maximum:
            return False

    return True


def inverse_kinematics(x, y, z):
    """
    Calculate joint angles for a target tool-tip position.

    Coordinates are relative to base_link, in metres.
    Returns (theta1, theta2, theta3, theta4) in radians.
    Tries both base orientations and both elbow branches.
    Keeps the wrist aligned with the forearm (theta4 = 0).
    """

    # Horizontal distance and shoulder-relative height
    r = math.hypot(x, y)
    h = z - SHOULDER_HEIGHT

    # Effective two-link arm
    L1 = UPPER_ARM_LENGTH
    L2 = FOREARM_LENGTH + WRIST_LENGTH

    # Two base orientations: toward the target and opposite the target.
    base_angle = math.atan2(y, x)
    base_candidates = [
        (base_angle, r),
        (math.atan2(-y, -x), -r),
    ]

    for theta1, signed_r in base_candidates:
        # Law of cosines
        cos_theta3 = (
            (r**2 + h**2 - L1**2 - L2**2)
            / (2 * L1 * L2)
        )

        # Check whether the target is geometrically reachable.
        if not -1.0 <= cos_theta3 <= 1.0:
            raise ValueError("Target is outside the arm's reach")

        # Try both elbow configurations.
        elbow_angle = math.acos(cos_theta3)
        for theta3 in (elbow_angle, -elbow_angle):
            alpha = math.atan2(signed_r, h)
            beta = math.atan2(
                L2 * math.sin(theta3),
                L1 + L2 * math.cos(theta3)
            )
            theta2 = alpha - beta
            theta4 = 0.0
            angles = (theta1, theta2, theta3, theta4)

            if within_joint_limits(angles):
                return angles

    raise ValueError("No IK solution satisfies joint limits")

if __name__ == "__main__":
    targets = [
    (0.20, 0.20, 0.30),
    (0.30, 0.00, 0.11),
    (1.00, 0.00, 0.30),
    (0.30, 0.00, 0.00),
    (0.00, 0.00, 0.30),
    (-0.24211007679584348, 0.0, -0.111320380249788),
    ]

    for target in targets:
        print(f"\nTesting target: {target}")

        try:
            angles = inverse_kinematics(*target)
            result = forward_kinematics(*angles)
            error = math.dist(target, result)

            print("Joint angles (degrees):")
            print([round(math.degrees(a), 2) for a in angles])
            print(f"FK result: {result}")
            print(f"Position error: {error:.10f} m")

        except ValueError as exc:
            print(f"IK rejected target: {exc}")
