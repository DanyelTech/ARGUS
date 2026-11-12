# ARGUS Project State

**Last updated:** 2026-11-12
**Project:** ARGUS v1  
**Current phase:** Phase 6 — Simulated motion control (in progress)

## Current checkpoint

ARGUS has a functioning ROS 2 Jazzy simulation of a 4-DOF robotic arm,
including a Xacro robot description, RViz visualization, forward and inverse
kinematics, and smooth joint-space trajectory execution.

The `argus_bringup` package provides Cartesian target handling, joint
trajectory generation, and trajectory completion status. The
`argus_description` package provides the robot model and visualization launch
files.

The current motion-control pipeline is:

1. `/argus/target_position` receives a Cartesian target in `base_link`.
2. The IK node calculates a valid joint configuration.
3. `/argus/joint_commands` delivers the joint target.
4. The trajectory node interpolates joint positions using cubic smoothstep
   easing.
5. `/joint_states` drives the simulated robot visualization.
6. `/argus/trajectory_complete` reports whether the planned movement duration
   has elapsed.

The trajectory node publishes joint states at approximately 30 Hz. Motion
duration is calculated using per-joint velocity limits of 0.5 rad/s, with a
factor of 1.5 to account for smoothstep's peak velocity.

The current launch command is:

```bash
cd /workspaces/argus/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch argus_description trajectory_display.launch.py
```

Physical actuator control has not yet been implemented.

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
- `source /opt/ros/jazzy/setup.bash && cd ros2_ws && colcon build
  --symlink-install` succeeds for both packages with the ROS 2 IK integration.
- Pylance reports no syntax errors in `ik_node.py`.
- On launch, the IK node logs `ARGUS initialized in upright configuration`.
  A synchronized `ros2 topic echo --once /joint_states
  sensor_msgs/msg/JointState` captured `base_link` and the four expected joint
  names with positions `[0.0, 0.0, 0.0, 0.0]`.
- The focused FK, IK, and IK-node regression tests pass: 13 passed.
- An isolated ROS runtime check confirmed startup zero angles, a reachable
  target publishing the solver's joint positions, and an unreachable target
  producing no further joint-state command.
- After stopping a duplicate launch instance, the active `/joint_states`
  graph had one publisher (`ik_node`) and one subscriber
  (`robot_state_publisher`).
- User-reported manual verification confirms RViz displays the upright arm,
  reachable Cartesian targets update its configuration, and unreachable
  targets warn while preserving the previous configuration.
- Targeted `flake8` passes for the Phase 5 node, launch file, and regression
  test.

## Phase 6 — Verified motion-control progress

- Joint-space interpolation is implemented in `trajectory.py`.
- Trajectory duration is calculated from joint displacement and maximum joint
  velocity.
- Cubic smoothstep easing provides zero velocity at the start and end of each
  planned movement.
- The trajectory node publishes interpolated joint positions to
  `/joint_states` at approximately 30 Hz.
- `trajectory_display.launch.py` launches the IK node, trajectory node, robot
  state publisher, and RViz.
- User-reported RViz verification confirms smooth movement between reachable
  Cartesian targets.
- The trajectory node validates joint names, joint counts, and finite target
  angles.
- New targets received during motion begin from the current interpolated
  position.
- `/argus/trajectory_complete` publishes `std_msgs/msg/Bool`.
- `false` indicates the planned trajectory is active.
- `true` indicates its planned duration has elapsed.
- User-reported runtime verification confirmed the status transitions from
  `true` to `false` during movement and back to `true` afterward.
- The trajectory completion helper passed six manual assertions.
- User-reported: the complete trajectory unit-test file passed all 16 tests
  on 2026-11-12.
- User-reported: the trajectory completion implementation and tests were
  committed and pushed to GitHub.

### Current limitations

- Completion is determined by elapsed trajectory time, not physical actuator
  feedback.
- The completion boolean does not identify individual commands.
- The completion status is published continuously, including while idle.
- Automated multi-waypoint execution has not been implemented.
- Trajectory-node joint-limit validation and collision checking are not
  implemented.
- New commands during active movement can introduce velocity discontinuities.
- No ESP32 communications or physical actuator control is implemented.

## Not yet verified in this checkpoint

- Interactive joint manipulation beyond launch-time GUI initialization.
- End-to-end `/joint_states` to `/argus/tool_position` runtime behavior under
  all joint configurations.
- Independent ROS TF versus Python FK comparison for the reported
  zero-angle, shoulder-rotation, and bent-elbow configurations.
- A persistent automated ROS integration test for target success and
  unreachable-target preservation.
- Automated multi-waypoint execution.
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
- Running multiple visualization launch descriptions can create multiple
  `/joint_states` publishers and duplicate robot-state/RViz nodes:
  `display.launch.py` starts `joint_state_publisher_gui`, while
  `ik_display.launch.py` remaps the IK publisher to that same topic. Run only
  one of these launch descriptions at a time.
- The complete bringup pytest run still fails its repository-wide
  `flake8`/`pep257` checks because of existing style violations and a stale,
  missing installed launch-file path. The Phase 5 Python files pass targeted
  `flake8`.
- Physical hardware operation is not implemented.

## Next action

Implement reliable waypoint execution, starting with command-specific
trajectory completion acknowledgement to prevent the controller from
mistaking the initial idle state for completion of a newly submitted waypoint.

Then implement and test a sequential waypoint queue before proceeding to
safety validation and ESP32 communication.

## Working protocol

Every session should update this file with the current milestone, verified
evidence, known problems, and one concrete next action. Claims about behavior
must be backed by a command, test, or direct inspection.
