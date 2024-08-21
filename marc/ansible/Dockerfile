# Use Ubuntu as base image
FROM ubuntu:latest

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]

# Update the system and install necessary packages
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y git software-properties-common ssh ansible sudo bash bash-completion curl && \
    apt-get clean

RUN apt-get update && apt-get install -y libreadline-dev

# Set the default shell for the root user to bash
RUN echo "root:$(openssl passwd -1 root)" | chpasswd && chsh -s /bin/bash root

# Set the default user name
ARG myusername=default_user

# Create a new user
RUN useradd -m ${myusername}

# Add the user to the sudo group
RUN usermod -aG sudo ${myusername}

# Set the default shell for the new user to bash by modifying /etc/passwd
RUN sed -i "s|${myusername}:.*|${myusername}:x:$(id -u ${myusername}):$(id -g ${myusername}):,,,:/home/${myusername}:/bin/bash|" /etc/passwd

# Copy .ssh directory from host to the docker container
COPY ./.ssh /home/${myusername}/.ssh/

# Copy .bashrc file from host to the docker container
COPY ./.bashrc /home/${myusername}/.bashrc

# Change the owner of the .bashrc file
RUN chown ${myusername}: /home/${myusername}/.bashrc

# Correct permissions of .ssh directory
RUN chown -R ${myusername}: /home/${myusername}/.ssh && \
    chmod 700 /home/${myusername}/.ssh && \
    chmod 600 /home/${myusername}/.ssh/*

# Switch to the new user
USER ${myusername}

# Set the work directory
WORKDIR /home/${myusername}

# Revert back to the normal user
ENV DEBIAN_FRONTEND=

# Keep container running
CMD tail -f /dev/null
