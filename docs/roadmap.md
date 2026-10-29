# ARGUS Roadmap

This roadmap tracks planned work and completion criteria. A phase is not
complete until its criteria are verified and recorded in
[`project_state.md`](./project_state.md).

## Phase 1 — ROS 2 foundation

**Status:** In progress

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

**Status:** Planned

### Scope

- Verify RViz2, Xacro, and `robot_state_publisher` in the dev container.
- Create a generic simulated 4-DOF arm description.
- Define and verify links, joints, coordinate frames, and joint limits.
- Launch the model in RViz2.

### Completion criteria

- Xacro expands successfully.
- `robot_state_publisher` publishes the expected transforms.
- RViz2 displays the arm with the expected frame tree.
- Joint limits and frame names are documented and tested.

## Phase 3 — Kinematics and motion control

**Status:** Planned

### Scope

- Implement forward kinematics for the virtual arm.
- Define and validate inverse kinematics goals and solutions.
- Add joint control and motion planning interfaces.
- Connect planned trajectories to the simulated robot.
- Add basic deterministic motion demonstrations.

### Completion criteria

- Forward-kinematics results are validated against known configurations.
- Inverse-kinematics solutions are checked against position and orientation
  tolerances.
- Planned commands produce the intended simulated joint changes.
- Motion is bounded by documented limits.
- Unreachable goals and planning failures are reported explicitly.
- Failures and invalid commands are visible to the operator.
- A repeatable test or demonstration command is documented.

## Phase 4 — Computer vision and coordinate transformations

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

## Phase 5 — Safety and failure handling

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

## Phase 6 — ESP32 firmware and serial communication

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

## Phase 7 — Physical arm integration

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
