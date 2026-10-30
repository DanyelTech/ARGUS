# ARGUS Engineering Decisions

This document records decisions that affect the project structure or
development strategy.

## D001 — Use ROS 2 Jazzy in a dev container

**Date:** 2026-10-29  
**Status:** Accepted

ARGUS development uses a reproducible VS Code dev container based on ROS 2
Jazzy (`ros:jazzy-ros-base-noble`). ROS tooling and visualization dependencies
are installed in the container rather than assumed to exist on the host.

**Reason:** Keep the development environment consistent across machines and
make the ROS 2 dependency set explicit.

## D002 — Start with an `ament_python` bringup package

**Date:** 2026-10-29  
**Status:** Accepted

The first ROS 2 package is `argus_bringup`, an `ament_python` package under
`ros2_ws/src/`. Its Python nodes are packaged through `setup.py` console
entry points.

**Reason:** Python is sufficient for the initial software-first bringup and
allows the communication path to be tested before introducing robot models,
hardware drivers, or lower-level control code.

## D003 — Use a publisher/subscriber status topic as the first integration test

**Date:** 2026-10-29  
**Status:** Accepted

The initial communication contract is a `std_msgs/msg/String` topic named
`/argus/status`. The publisher emits `ARGUS system online`, and the subscriber
logs received messages.

**Reason:** This provides a small, observable ROS 2 integration boundary
before adding motion, kinematics, coordinate frames, or hardware.

## D004 — Develop in simulation before purchasing or assembling hardware

**Date:** 2026-10-29  
**Status:** Accepted

Physical arm purchases and assembly are deferred. The next hardware-adjacent
work will use a generic simulated 4-DOF arm.

**Reason:** Validate software architecture, ROS 2 interfaces, visualization,
and motion concepts before committing to a physical design.

## D005 — Treat verified code and test evidence as authoritative

**Date:** 2026-10-29  
**Status:** Accepted

Implemented behavior is distinguished from planned design. A successful build
does not by itself establish runtime correctness. Session records must include
the commands used, their results, and any remaining unverified behavior.

**Reason:** Robotics failures can occur in runtime behavior, kinematics,
coordinate frames, and motion even when code compiles successfully.

## D006 — Configure WSLg/X11 access for container visualization

**Date:** 2026-10-30
**Status:** Accepted

The dev container mounts WSLg's X11 socket at `/tmp/.X11-unix`, sets
`DISPLAY` to `:0`, and selects the XCB Qt platform. This configuration is used
for RViz2 and the joint-state publisher GUI when running the visualization
launch file from the container.

**Reason:** Keep graphical ROS tools reproducible in the WSLg-backed VS Code
container instead of depending on a host-specific `DISPLAY` value or manual
socket setup.
