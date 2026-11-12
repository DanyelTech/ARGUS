# ARGUS Roadmap

This roadmap tracks planned work and completion criteria. A phase is not
complete until its criteria are verified and recorded in
[`project_state.md`](./project_state.md).

## Phase 1 — ROS 2 foundation

**Status:** Complete at current scope

### Completed or implemented

- ROS 2 Jazzy dev container configuration.
- `ros2_ws/src/argus_bringup` package layout.
- Python package metadata and console entry points.
- Status publisher and subscriber source nodes.
- Initial Git repository and GitHub remote configuration.

### Completion criteria

- Fresh `colcon build` succeeds from `ros2_ws`.
- Publisher and subscriber run concurrently without errors.
- `/argus/status` is discoverable with ROS 2 CLI tools.
- Subscriber receives and logs publisher messages.
- Normal `Ctrl+C` shutdown is retested for both nodes.
- Results and exact commands are recorded in the project state and session
  log when that log is added.

## Phase 2 — Visualization and robot description

**Status:** Complete

### Scope

- Verified RViz2, Xacro, and `robot_state_publisher` in the dev container.
- Created a generic simulated 4-DOF arm description.
- Defined and verified links, joints, coordinate frames, and joint limits.
- Launched the model in RViz2 with the joint-state GUI.

### Completion criteria

- Xacro expands successfully and passes `check_urdf`.
- `robot_state_publisher` starts and initializes the expected five-link chain.
- RViz2 starts with the saved configuration and receives the robot description.
- Joint limits and frame names are defined in the Xacro and represented in the
  RViz configuration.

## Phase 3 — Forward kinematics

**Status:** Complete at current scope

### Scope

- Implement forward kinematics for the virtual arm.
- Publish calculated tool position from a ROS 2 node.
- Add and verify the `tool_tip` coordinate frame.

### Completion criteria

- Forward-kinematics results are validated by four unit tests.
- The FK node subscribes to `/joint_states` and publishes
  `/argus/tool_position`.
- The tool position is expressed relative to `base_link`, matching the
  `tool_tip` URDF frame.

The four Python unit tests pass independently. The user also manually
confirmed agreement between ROS TF and the Python FK node for zero-angle,
shoulder-rotation, and bent-elbow configurations; that manual comparison is
user-reported evidence.

## Phase 4 — Inverse kinematics

**Status:** Complete at current position-only IK scope

### Scope

- Define and validate inverse-kinematics goals and solutions across both base
  orientations and both elbow configurations.
- Enforce the base, shoulder, elbow, and wrist limits defined by the URDF.
- Check position tolerances through FK round trips; wrist orientation is
  outside the current scope.
- Report unreachable goals and joint-limit failures explicitly.

### Completion criteria

- Inverse-kinematics solutions are checked against position tolerances.
- Unreachable goals and joint-limit failures are reported explicitly.
- A repeatable test or demonstration command is documented.

The 8-test IK suite passes, including backward negative-elbow reach,
unreachable geometry, joint-limit checks, and base-angle edge cases. The
current scope keeps the wrist angle fixed at zero and does not include
collision checking or ROS 2 integration.

## Phase 5 — ROS 2 IK integration

**Status:** Complete at current simulation/visualization scope

### Scope

- Add a ROS 2 interface for Cartesian IK targets.
- Publish or command validated joint positions.
- Automatically publish the upright zero-angle configuration for
  visualization when `robot_state_publisher` is subscribed.
- Verify target handling and failure reporting through ROS 2.

### Completion criteria

- A ROS 2 node accepts a Cartesian target and invokes the IK solver.
- Valid solutions are exposed through a documented joint-position interface.
- Unreachable and joint-limit failures are visible to the operator.

The IK display launch now publishes the zero-angle joint state after
`robot_state_publisher` subscribes to `/joint_states`. A synchronized runtime
capture confirmed the four joint positions are all zero, and the node logged
successful upright initialization. An isolated ROS runtime check verified
reachable target publication and that an unreachable target does not publish
a replacement configuration. The user manually verified the same target
behavior and RViz display in the launch. The startup publication and target
commands are visualization-only and assume the IK node is the sole
`/joint_states` publisher. A persistent automated ROS integration test remains
the next validation improvement.

## Phase 6 — Motion control

**Status:** In progress — smooth trajectory execution and completion signaling verified

### Implemented and verified

- Joint-space interpolation between commanded configurations.
- Per-joint velocity-based trajectory duration calculation.
- Cubic smoothstep acceleration and deceleration profiles.
- ROS 2 trajectory node publishing simulated joint states at approximately
  30 Hz.
- Cartesian target → IK → joint trajectory → RViz execution.
- Valid joint-name, joint-count, and finite-angle checks.
- Trajectory completion publisher on `/argus/trajectory_complete`.
- User-reported manual verification of completion status during simulated
  motion.
- User-reported: 16 trajectory unit tests passed on 2026-11-12.

### Remaining work

- Implement command-specific trajectory completion acknowledgements.
- Implement sequential multi-waypoint execution.
- Add automated tests for waypoint ordering and completion handling.
- Validate joint limits and representative failure cases.
- Document repeatable motion demonstrations.

### Completion criteria

- Planned commands produce the intended simulated joint changes.
- Sequential waypoints execute in the correct order.
- Motion respects documented joint velocity and position limits.
- Invalid commands and failures are handled predictably.
- Automated tests and repeatable demonstration commands are documented.

### Limitations

The current controller uses simulated joint states. It does not provide
physical actuator feedback, collision avoidance, or hardware-level safety
guarantees.

## Phase 7 — Computer vision and coordinate transformations

**Status:** Planned

### Scope

- Add OpenCV-based object detection.
- Define camera calibration data and image-to-robot coordinate
  transformations.
- Represent detected objects in documented coordinate frames.
- Connect perception outputs to simulated motion goals.

### Completion criteria

- Camera calibration and transformation assumptions are documented.
- Detection results are reproducible on representative test inputs.
- Coordinate transformations are validated against known reference points.
- Perception failures and uncertain detections are visible to the operator.

## Phase 8 — Safety and failure handling

**Status:** Planned

### Scope

- Define software safety boundaries, joint limits, and command validation.
- Add emergency-stop and safe-shutdown interfaces appropriate to simulation.
- Define timeout, stale-data, communication-loss, and invalid-command
  behavior.
- Exercise failure cases before any hardware integration.

### Completion criteria

- Unsafe or invalid commands are rejected.
- Motion stops or enters a documented safe state on required failures.
- Safety behavior is tested and recorded for representative scenarios.
- Safety assumptions and limitations are explicit before hardware work begins.

## Phase 9 — ESP32 firmware and serial communication

**Status:** Planned; hardware-independent experimentation allowed

### Scope

- Experiment with ESP32 firmware without motors or a completed physical arm.
- Define the host-to-microcontroller serial protocol.
- Implement and test message framing, acknowledgements, telemetry, and
  communication-loss handling.
- Use simulated or mocked actuator data where practical.

### Completion criteria

- Firmware builds reproducibly.
- Serial messages have documented formats and error behavior.
- Host and ESP32 communication is tested without requiring motor hardware.
- Disconnects, malformed messages, and stale commands are handled safely.

## Phase 10 — Physical arm integration

**Status:** Deferred

Physical arm selection, purchasing, assembly, motor integration, and
hardware-specific drivers remain out of scope until the simulation, safety,
and ESP32 communication milestones provide sufficient evidence and explicit
authorization.

### Future scope

- Integrate verified hardware drivers and actuator interfaces.
- Calibrate the physical arm and camera system.
- Validate kinematics, coordinate frames, motion limits, and safety on the
  actual mechanism.
- Progress from controlled bench tests to broader physical operation.
