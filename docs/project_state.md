# ARGUS Project State

**Last updated:** 2026-10-30
**Project:** ARGUS v1  
**Current phase:** Software-first development, Phase 1 — ROS 2 foundation

## Current checkpoint

The repository contains the initial ROS 2 workspace, the `argus_bringup`
Python package, and the `argus_description` resource package. The bringup
package source is located at `ros2_ws/src/argus_bringup/` and includes
publisher/subscriber nodes for the `/argus/status` topic. The description
package now contains a generic simulated 4-DOF arm, a visualization launch
file, and an RViz configuration.

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
- `argus_description` is an `ament_cmake` package containing the 4-DOF Xacro
  model, visualization launch file, and RViz configuration.
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
- `xacro ros2_ws/src/argus_description/urdf/argus_arm.urdf.xacro |
  check_urdf /dev/stdin` succeeds and reports the expected five-link chain:
  `base_link`, `base_rotation_link`, `upper_arm_link`, `forearm_link`, and
  `wrist_link`.
- `cd ros2_ws && colcon build --symlink-install` succeeds for both packages
  after adding the robot description resources.
- `source ros2_ws/install/setup.bash && ros2 launch
  argus_description display.launch.py` starts `robot_state_publisher`,
  `joint_state_publisher_gui`, and RViz2; RViz2 initializes with OpenGL and
  the GUI receives the robot description before the bounded smoke test is
  interrupted.
- A timeout-based termination can raise `ExternalShutdownException`; this is
  specific to externally terminating a spinning ROS node and is not a normal
  Ctrl+C behavior.

## Not yet verified in this checkpoint

- Interactive joint manipulation beyond launch-time GUI initialization.
- Forward-kinematics calculations for the four joints.
- Physical hardware operation. Hardware remains deferred in favor of
  simulation.

## Known issues and risks

- The visualization smoke test was bounded with `timeout`; RViz2 and the joint
  state GUI therefore report signal-based termination when the test ends.
- A fresh Dev Container build is required to validate the explicit `ubuntu`
  user creation fallback in the Dockerfile.

## Next action

Implement and validate forward kinematics for the simulated 4-DOF arm,
without introducing hardware integration.

## Working protocol

Every session should update this file with the current milestone, verified
evidence, known problems, and one concrete next action. Claims about behavior
must be backed by a command, test, or direct inspection.
