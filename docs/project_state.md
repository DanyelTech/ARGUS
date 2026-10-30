# ARGUS Project State

**Last updated:** 2026-10-30
**Project:** ARGUS v1  
**Current phase:** Software-first development, Phase 2 complete — visualization
and robot description

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
- The model contains all five links and four revolute joints:
  `base_rotation_joint`, `shoulder_joint`, `elbow_joint`, and `wrist_joint`.
- The Dev Container was rebuilt successfully after updating
  `.devcontainer/devcontainer.json` to provide WSLg/X11 graphical access.
- `cd ros2_ws && colcon build --symlink-install` succeeds for both packages
  after adding the robot description resources.
- `cd ros2_ws && colcon test` reports 11 tests, 0 failures, 0 errors, and 1
  skipped test.
- During the successful manual graphical launch, RViz2 and
  `joint_state_publisher_gui` both opened, and the ARGUS arm was visible in
  RViz2 with RobotModel status OK.
- The RViz configuration was saved to
  `ros2_ws/src/argus_description/rviz/argus.rviz`.
- `display.launch.py` successfully loads the saved RViz configuration
  automatically when launching `argus_description`.
- An earlier bounded automated launch test confirmed that
  `robot_state_publisher`, `joint_state_publisher_gui`, and RViz2 started and
  exchanged the robot description. Its externally imposed timeout caused
  signal-based termination messages; those messages do not describe the later
  successful manual graphical launch.

## Not yet verified in this checkpoint

- Interactive joint manipulation beyond launch-time GUI initialization.
- Forward-kinematics calculations for the four joints.
- Physical hardware operation. Hardware remains deferred in favor of
  simulation.

## Known issues and risks

- Interactive movement of all four joints has not yet been explicitly tested.
- The earlier timeout-based launch test produced expected termination messages
  because it was externally interrupted; the manual graphical launch was
  successful.

## Next action

Implement and validate forward kinematics for the simulated 4-DOF arm,
without introducing hardware integration.

## Working protocol

Every session should update this file with the current milestone, verified
evidence, known problems, and one concrete next action. Claims about behavior
must be backed by a command, test, or direct inspection.
