# ARGUS Project State

**Last updated:** 2026-11-03
**Project:** ARGUS v1  
**Current phase:** Software-first development, Phase 4 complete at current
scope — inverse kinematics

## Current checkpoint

The repository contains the initial ROS 2 workspace, the `argus_bringup`
Python package, and the `argus_description` resource package. The bringup
package source is located at `ros2_ws/src/argus_bringup/` and includes
publisher/subscriber nodes for the `/argus/status` topic, a pure
forward-kinematics implementation, and an FK ROS 2 node. The description
package contains a generic simulated 4-DOF arm, a visualization launch file,
an RViz configuration, and a `tool_tip` URDF frame.

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
- `forward_kinematics.py` implements the four-joint tool-position calculation
  in metres relative to `base_link`.
- `fk_node.py` subscribes to `/joint_states`, validates the four required joint
  names, and publishes the calculated position as a `PointStamped` on
  `/argus/tool_position` with `base_link` as its frame.
- The URDF includes a fixed `tool_tip` frame attached to `wrist_link`.
- `cd ros2_ws && python3 -m pytest
  src/argus_bringup/test/test_forward_kinematics.py -q` passes independently
  with 4 tests passed.
- `source /opt/ros/jazzy/setup.bash && cd ros2_ws && colcon build
  --symlink-install` succeeds with the FK implementation.
- An earlier bounded automated launch test confirmed that
  `robot_state_publisher`, `joint_state_publisher_gui`, and RViz2 started and
  exchanged the robot description. Its externally imposed timeout caused
  signal-based termination messages; those messages do not describe the later
  successful manual graphical launch.
- User-reported manual verification confirmed agreement between ROS TF and the
  Python FK node for zero-angle, shoulder-rotation, and bent-elbow
  configurations. This comparison was not independently repeated in this
  session.
- The IK suite independently passes 8 tests, and the combined FK and IK
  suites pass 12 tests total.
- The IK solver covers both base orientations, both elbow configurations,
  geometric reachability, joint limits, backward reach, and FK round trips.
- User-reported results also confirm all 8 IK tests passed.

## Not yet verified in this checkpoint

- Interactive joint manipulation beyond launch-time GUI initialization.
- End-to-end `/joint_states` to `/argus/tool_position` runtime behavior under
  all joint configurations.
- Independent ROS TF versus Python FK comparison for the reported
  zero-angle, shoulder-rotation, and bent-elbow configurations.
- ROS 2 inverse-kinematics integration.
- Motion planning and trajectory control.
- Physical hardware operation. Hardware remains deferred in favor of
  simulation.

## Known issues and risks

- Interactive movement of all four joints has not yet been explicitly tested.
- The earlier timeout-based launch test produced expected termination messages
  because it was externally interrupted; the manual graphical launch was
  successful.
- The IK solver keeps the wrist angle fixed at zero and does not solve wrist
  orientation.
- Collision checking is not implemented.
- Base-angle limits use approximately +/-3.14 radians; exact +/-pi values
  are rejected by the current edge-case tests.
- ROS 2 IK integration, motion planning, and trajectory control remain
  unimplemented.

## Next action

Integrate inverse kinematics with ROS 2 so Cartesian targets can produce
validated joint positions, without introducing hardware integration.

## Working protocol

Every session should update this file with the current milestone, verified
evidence, known problems, and one concrete next action. Claims about behavior
must be backed by a command, test, or direct inspection.
