# ARGUS v1 Development Instructions

## Project authority and documentation

- Treat the repository's source code and documentation as the authoritative
  project state. Do not assume a feature exists based on previous
  conversations or unverified reports.
- Before beginning substantial work, read the relevant project
  documentation, including:
  - [`docs/project_state.md`](docs/project_state.md)
  - [`docs/decisions.md`](docs/decisions.md)
  - [`docs/roadmap.md`](docs/roadmap.md)
- Distinguish clearly between functionality that is implemented, tested,
  partially implemented, and planned.
- Do not claim that code has been tested unless the relevant commands were
  actually executed successfully.

## Architecture and development approach

- Preserve the simulation-first architecture. Physical arm assembly and
  purchasing remain deferred.
- Keep ROS 2 Jazzy and the existing Dev Container as the development
  environment.
- Prefer incremental, modular changes over large architectural rewrites.
- Before implementing substantial modifications, explain the proposed
  changes and their purpose.
- Follow existing repository conventions and use appropriate linting and
  testing tools.

## Project records

- After meaningful development work, update
  [`docs/project_state.md`](docs/project_state.md) with verified progress,
  known issues, and one concrete next action.
- Record significant architectural decisions in
  [`docs/decisions.md`](docs/decisions.md).
- Update [`docs/roadmap.md`](docs/roadmap.md) when milestones or phase status
  change.

## Repository safety

- Do not commit, push, delete, or substantially restructure files without
  explicit permission.
- Keep changes focused on the requested work and preserve existing behavior
  unless an intentional behavior change is documented and authorized.
