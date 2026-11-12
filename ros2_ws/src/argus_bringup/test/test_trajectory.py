"""Tests for ARGUS trajectory calculations."""

import pytest

from argus_bringup.trajectory import (
    calculate_duration,
    interpolate_joints,
    smoothstep,
    trajectory_at_time,
    trajectory_complete,
)


def test_interpolation_endpoints():
    """Interpolation reaches both endpoints."""
    start = (0.0, 0.0)
    target = (1.0, -1.0)

    assert interpolate_joints(start, target, 0.0) == start
    assert interpolate_joints(start, target, 1.0) == target


def test_interpolation_midpoint():
    """Interpolation calculates the midpoint."""
    result = interpolate_joints(
        (0.0, 0.0),
        (1.0, -1.0),
        0.5,
    )

    assert result == pytest.approx((0.5, -0.5))


def test_duration():
    """Duration respects the slowest joint."""
    duration = calculate_duration(
        (0.0, 0.0),
        (1.0, 0.5),
        (0.5, 0.5),
    )

    assert duration == pytest.approx(2.0)


def test_smoothstep_endpoints():
    """Smoothstep preserves trajectory endpoints."""
    assert smoothstep(0.0) == 0.0
    assert smoothstep(1.0) == 1.0


def test_smoothstep_midpoint():
    """Smoothstep reaches halfway at alpha 0.5."""
    assert smoothstep(0.5) == pytest.approx(0.5)


def test_trajectory_endpoints():
    """Trajectory begins and ends correctly."""
    start = (0.0, 0.0)
    target = (1.0, -1.0)

    assert trajectory_at_time(
        start, target, 0.0, 3.0
    ) == pytest.approx(start)

    assert trajectory_at_time(
        start, target, 3.0, 3.0
    ) == pytest.approx(target)


def test_trajectory_does_not_overshoot():
    """Trajectory remains at target after completion."""
    result = trajectory_at_time(
        (0.0,),
        (1.0,),
        10.0,
        3.0,
    )

    assert result == pytest.approx((1.0,))


def test_smoothstep_velocity_limit():
    """Smoothstep peak velocity respects the configured limit."""
    displacement = 1.0
    max_velocity = 0.5

    duration = 1.5 * calculate_duration(
        (0.0,),
        (displacement,),
        (max_velocity,),
    )

    peak_velocity = 1.5 * displacement / duration

    assert peak_velocity <= max_velocity + 1e-9


@pytest.mark.parametrize(
    'alpha',
    [-0.1, 1.1],
)
def test_invalid_alpha(alpha):
    """Invalid interpolation progress is rejected."""
    with pytest.raises(ValueError):
        smoothstep(alpha)


def test_invalid_duration():
    """Negative trajectory durations are rejected."""
    with pytest.raises(ValueError):
        trajectory_at_time(
            (0.0,), (1.0,), 0.0, -1.0
        )


def test_invalid_velocity():
    """Nonpositive velocity limits are rejected."""
    with pytest.raises(ValueError):
        calculate_duration(
            (0.0,), (1.0,), (0.0,)
        )
def test_trajectory_complete_before_duration():
    assert trajectory_complete(0.0, 2.0) is False
    assert trajectory_complete(1.0, 2.0) is False


def test_trajectory_complete_at_and_after_duration():
    assert trajectory_complete(2.0, 2.0) is True
    assert trajectory_complete(3.0, 2.0) is True


def test_trajectory_complete_zero_duration():
    assert trajectory_complete(0.0, 0.0) is True


def test_trajectory_complete_rejects_negative_time():
    with pytest.raises(ValueError):
        trajectory_complete(-1.0, 2.0)

    with pytest.raises(ValueError):
        trajectory_complete(1.0, -2.0)