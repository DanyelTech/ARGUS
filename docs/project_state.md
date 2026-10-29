# ARGUS Project State

**Last updated:** 2026-10-29  
**Project:** ARGUS v1  
**Current phase:** Software-first development, Phase 1 — ROS 2 foundation

## Current checkpoint

The repository contains the initial ROS 2 workspace, the `argus_bringup`
Python package, and an empty `argus_description` resource package. The
bringup package source is located at `ros2_ws/src/argus_bringup/` and includes
publisher/subscriber nodes for the `/argus/status` topic. Robot description
files have not yet been implemented.

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
- `argus_description` is an `ament_cmake` package with clone-safe placeholder
  directories for future URDF, launch, and RViz resources.
- Root-level ROS build artifact directories are ignored; ROS commands are run
  from `ros2_ws/`.

## Verified tests in this checkpoint

- `cd ros2_ws && colcon build --symlink-install` succeeds for both packages.
- `cd ros2_ws && colcon test` reports 7 tests, 0 failures, 0 errors, and 1
  skipped test.
- Both packages are discoverable after sourcing `ros2_ws/install/setup.bash`.
- A bounded concurrent runtime test confirmed publisher output and subscriber
  receipt on `/argus/status`.
- ROS 2 Jazzy packages for RViz2, Xacro, `robot_state_publisher`, and
  `joint_state_publisher_gui` are installed.
- A timeout-based termination can raise `ExternalShutdownException`; this is
  specific to externally terminating a spinning ROS node and is not a normal
  Ctrl+C behavior.

## Not yet verified in this checkpoint

- Interactive RViz2, Xacro, and `robot_state_publisher` behavior; no model
  exists yet to exercise them.
- Physical hardware operation. Hardware remains deferred in favor of
  simulation.

## Known issues and risks

- The `argus_description` package contains no robot model, launch file, or RViz
  configuration yet.
- A fresh Dev Container build is required to validate the explicit `ubuntu`
  user creation fallback in the Dockerfile.

## Next action

Create and validate `argus_arm.urdf.xacro` with its launch and RViz resources,
without introducing hardware integration.

## Working protocol

Every session should update this file with the current milestone, verified
evidence, known problems, and one concrete next action. Claims about behavior
must be backed by a command, test, or direct inspection.
