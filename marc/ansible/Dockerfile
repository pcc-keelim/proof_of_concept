# Use Ubuntu as base image    
FROM ubuntu:latest
    
# Avoid warnings by switching to noninteractive  
ENV DEBIAN_FRONTEND=noninteractive  
  
# Update the system and install necessary packages  
RUN apt-get update -y && \  
    apt-get upgrade -y && \  
    apt-get install -y git software-properties-common ssh ansible sudo && \  
    rm -rf /var/lib/apt/lists/*  
  
# Set the default user name      
ARG myusername=default_user 

# Create a new user
RUN useradd -m ${myusername}

# Add the user to the sudo group
RUN usermod -aG sudo ${myusername}

# Copy .ssh directory from host to the docker container    
COPY ./.ssh /home/${myusername}/.ssh/

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
