def interpolate_joints(start, target, alpha):
    """Interpolate between two joint configurations."""

    if len(start) != len(target):
        raise ValueError("Joint configurations must have equal lengths")

    if not 0.0 <= alpha <= 1.0:
        raise ValueError("Alpha must be between 0 and 1")

    return tuple(
        start_angle + alpha * (target_angle - start_angle)
        for start_angle, target_angle in zip(start, target)
    )

def calculate_duration(start, target, max_velocities):
    """Calculate the minimum duration respecting joint velocity limits."""

    if not (len(start) == len(target) == len(max_velocities)):
        raise ValueError("Joint configurations must have equal lengths")

    if any(velocity <= 0 for velocity in max_velocities):
        raise ValueError("Maximum velocities must be positive")

    joint_durations = [
        abs(target_angle - start_angle) / max_velocity
        for start_angle, target_angle, max_velocity
        in zip(start, target, max_velocities)
    ]

    return max(joint_durations, default=0.0)

def trajectory_at_time(start, target, elapsed_time, duration):
    """Calculate joint positions at a given elapsed time."""

    if duration < 0:
        raise ValueError("Duration cannot be negative")

    if elapsed_time < 0:
        raise ValueError("Elapsed time cannot be negative")

    if duration == 0:
        return interpolate_joints(start, target, 1.0)

    alpha = min(1.0, elapsed_time / duration)

    return interpolate_joints(start, target, alpha)

