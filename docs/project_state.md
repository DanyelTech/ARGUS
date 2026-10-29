# ARGUS Project State

**Last updated:** 2026-10-29  
**Project:** ARGUS v1  
**Current phase:** Software-first development, Phase 1 — ROS 2 foundation

## Current checkpoint

The repository contains the initial ROS 2 workspace and an `argus_bringup`
Python package. The package source is located at
`ros2_ws/src/argus_bringup/` and includes publisher/subscriber nodes for the
`/argus/status` topic.

## Verified in the repository

- The dev container is based on `ros:jazzy-ros-base-noble`.
- The container configuration installs ROS 2 development tools, RViz2,
  `robot_state_publisher`, `joint_state_publisher_gui`, and Xacro.
- `argus_bringup` has `status_publisher` and `status_subscriber` console
  entry points.
- The publisher sends `std_msgs/msg/String` messages on `/argus/status` once
  per second.
- The subscriber listens on `/argus/status` and logs received messages.
- Publisher shutdown checks `rclpy.ok()` before calling `rclpy.shutdown()`.
- The latest repository commit is
  `8d67b8b` (`Initial ARGUS ROS 2 setup with publisher-subscriber
  communication`).
- The local `main` branch is tracking `origin/main`, configured as
  `https://github.com/DanyelTech/ARGUS.git`. Before this documentation
  change, the local branch matched `origin/main` with no Git status
  differences.

## Previous successful tests

The following results were reported from earlier development sessions. They
are preserved as historical evidence, but have not been independently
repeated during this checkpoint:

- The publisher and subscriber ran concurrently.
- The publisher transmitted status messages once per second.
- The subscriber received and logged those messages.
- `ros2 topic info /argus/status` reported one publisher and one subscriber.

## Not yet verified in this checkpoint

- A fresh end-to-end publisher/subscriber runtime test in the current
  container.
- ROS 2 topic discovery during a live run.
- RViz2, Xacro, and `robot_state_publisher` behavior.
- The subscriber's `Ctrl+C` shutdown path. Its source contains the intended
  conditional shutdown guard, but that behavior needs to be retested.
- Physical hardware operation. Hardware remains deferred in favor of
  simulation.

## Known issues and risks

- Generated `ros2_ws/build/`, `ros2_ws/install/`, and `ros2_ws/log/`
  directories are excluded from Git and should not be treated as source
  evidence.

## Next action

Run a fresh package build and live publisher/subscriber test, then verify
`/argus/status` with ROS 2 topic tools. After that, verify the installed
RViz2, Xacro, and `robot_state_publisher` tools before creating a generic
4-DOF virtual arm.

## Working protocol

Every session should update this file with the current milestone, verified
evidence, known problems, and one concrete next action. Claims about behavior
must be backed by a command, test, or direct inspection.
