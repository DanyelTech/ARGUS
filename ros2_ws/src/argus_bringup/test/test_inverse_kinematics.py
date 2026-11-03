
import math

import pytest

from argus_bringup.forward_kinematics import forward_kinematics
from argus_bringup.inverse_kinematics import (
    JOINT_LIMITS,
    inverse_kinematics,
    within_joint_limits,
)


POSITION_TOLERANCE = 1e-9


def assert_reaches_target(target):
    """Check that IK produces a valid FK round-trip."""
    angles = inverse_kinematics(*target)

    assert len(angles) == 4
    assert within_joint_limits(angles)

    for angle, (lower, upper) in zip(angles, JOINT_LIMITS):
        assert lower <= angle <= upper

    result = forward_kinematics(*angles)
    assert math.dist(result, target) < POSITION_TOLERANCE

    return angles


def test_normal_target():
    assert_reaches_target((0.20, 0.20, 0.30))


def test_horizontal_target():
    assert_reaches_target((0.30, 0.00, 0.11))


def test_target_below_base():
    assert_reaches_target((0.30, 0.00, 0.00))


def test_backward_negative_elbow():
    """Regression test for backward signed reach."""
    known_angles = tuple(
        math.radians(a) for a in (0, -80, -90, 0)
    )

    target = forward_kinematics(*known_angles)
    solved_angles = assert_reaches_target(target)

    # This target requires the backward-reach branch
    assert solved_angles[2] < 0


def test_target_on_base_axis():
    assert_reaches_target((0.00, 0.00, 0.30))


def test_unreachable_target():
    with pytest.raises(ValueError, match="outside the arm's reach"):
        inverse_kinematics(1.00, 0.00, 0.30)


def test_joint_limit_checker():
    assert within_joint_limits((0.0, 0.0, 0.0, 0.0))
    assert not within_joint_limits((0.0, 2.0, 0.0, 0.0))
    assert not within_joint_limits((0.0, 0.0, 3.0, 0.0))


def test_base_limit_checker():
    assert within_joint_limits((3.14, 0.0, 0.0, 0.0))
    assert within_joint_limits((-3.14, 0.0, 0.0, 0.0))

    assert not within_joint_limits((math.pi, 0.0, 0.0, 0.0))
    assert not within_joint_limits((-math.pi, 0.0, 0.0, 0.0))
