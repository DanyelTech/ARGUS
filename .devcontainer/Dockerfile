FROM ros:jazzy-ros-base-noble

ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=1000

# Install development tools and RViz
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-pip \
    git \
    build-essential \
    ros-jazzy-rviz2 \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-xacro \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-c"]

RUN if ! getent group "${USERNAME}" >/dev/null; then \
      groupadd --gid "${USER_GID}" "${USERNAME}"; \
    fi \
    && if ! id --user "${USERNAME}" >/dev/null 2>&1; then \
      useradd --uid "${USER_UID}" --gid "${USERNAME}" --create-home --shell /bin/bash "${USERNAME}"; \
    fi \
    && mkdir -p "/home/${USERNAME}" \
    && chown "${USERNAME}:${USERNAME}" "/home/${USERNAME}" \
    && echo "source /opt/ros/jazzy/setup.bash" >> "/home/${USERNAME}/.bashrc" \
    && chown "${USERNAME}:${USERNAME}" "/home/${USERNAME}/.bashrc"
