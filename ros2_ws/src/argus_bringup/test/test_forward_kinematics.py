
import math

from argus_bringup.forward_kinematics import forward_kinematics


def test_zero_angles():
    x, y, z = forward_kinematics(0, 0, 0, 0)

    assert math.isclose(x, 0.0, abs_tol=1e-9)
    assert math.isclose(y, 0.0, abs_tol=1e-9)
    assert math.isclose(z, 0.57, abs_tol=1e-9)


def test_shoulder_90_degrees():
    x, y, z = forward_kinematics(
        0, math.pi / 2, 0, 0
    )

    assert math.isclose(x, 0.46, abs_tol=1e-9)
    assert math.isclose(y, 0.0, abs_tol=1e-9)
    assert math.isclose(z, 0.11, abs_tol=1e-9)


def test_bent_elbow():
    x, y, z = forward_kinematics(
        0, math.pi / 2, -math.pi / 2, 0
    )

    assert math.isclose(x, 0.20, abs_tol=1e-9)
    assert math.isclose(y, 0.0, abs_tol=1e-9)
    assert math.isclose(z, 0.37, abs_tol=1e-9)


def test_base_rotation():
    x, y, z = forward_kinematics(
        math.pi / 2, math.pi / 2, 0, 0
    )

    assert math.isclose(x, 0.0, abs_tol=1e-9)
    assert math.isclose(y, 0.46, abs_tol=1e-9)
    assert math.isclose(z, 0.11, abs_tol=1e-9)
