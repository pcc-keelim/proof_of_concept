### `docker-compose.yml`

```yaml
version: '3.8'

services:
  control-node:
    image: ubuntu:latest
    container_name: control-node
    networks:
      internal_network:
        ipv4_address: 10.0.0.2
    hostname: control-node
    environment:
      - ANSIBLE_HOST_KEY_CHECKING=False
    volumes:
      - ./control_node_ansible:/root/.ssh
    command: >
      /bin/bash -c "
      apt-get update && 
      apt-get install -y software-properties-common &&
      apt-add-repository --yes --update ppa:ansible/ansible &&
      apt-get update && 
      apt-get install -y ansible ssh &&
      apt-get clean &&
      echo '[servers]' > /etc/ansible/hosts &&
      echo 'server1 ansible_host=10.0.0.3' >> /etc/ansible/hosts &&
      echo 'server2 ansible_host=10.0.0.4' >> /etc/ansible/hosts &&
      echo 'server3 ansible_host=10.0.0.5' >> /etc/ansible/hosts &&
      sleep infinity
      "
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1GB

  server1:
    image: ubuntu:latest
    container_name: server1
    networks:
      internal_network:
        ipv4_address: 10.0.0.3
    hostname: server1
    command: >
      /bin/bash -c "
      apt-get update &&
      apt-get install -y ssh &&
      apt-get clean &&
      sleep infinity
      "
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1GB

  server2:
    image: ubuntu:latest
    container_name: server2
    networks:
      internal_network:
        ipv4_address: 10.0.0.4
    hostname: server2
    command: >
      /bin/bash -c "
      apt-get update &&
      apt-get install -y ssh &&
      apt-get clean &&
      sleep infinity
      "
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1GB

  server3:
    image: ubuntu:latest
    container_name: server3
    networks:
      internal_network:
        ipv4_address: 10.0.0.5
    hostname: server3
    command: >
      /bin/bash -c "
      apt-get update &&
      apt-get install -y ssh &&
      apt-get clean &&
      sleep infinity
      "
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1GB

networks:
  internal_network:
    driver: bridge
    ipam:
      config:
        - subnet: 10.0.0.0/24
```

### Explanation:

1. **Network**: A custom bridge network named `internal_network` with a subnet starting from `10.0.0.0/24` is created, ensuring all the containers are connected and can communicate with each other using internal IP addresses.

2. **Control Node**:
   - Named `control-node`.
   - Ansible is installed using the latest PPA (Personal Package Archive).
   - SSH is installed and configured, and Ansible host entries are set up to recognize `server1`, `server2`, and `server3`.
   - The environment variable `ANSIBLE_HOST_KEY_CHECKING=False` is set to disable SSH host key checking, which can be helpful in a practice environment.
   - An initial setup command is provided to configure the control node.

3. **Server Containers** (`server1`, `server2`, `server3`):
   - Each is a basic Ubuntu container configured with SSH.
   - They are assigned specific IPs within the `internal_network`.

4. **Resource Allocation**: Each container is limited to `1GB` of RAM and `1 CPU` to simulate realistic server constraints.

5. **Persistence**: The control node uses a volume (`./control_node_ansible`) to store SSH configurations, facilitating easy key management.

### Usage Instructions

1. **Start the Environment**: Run `docker-compose up -d` to start all containers in the background.
2. **Access Control Node**: Use `docker exec -it control-node /bin/bash` to access the control node and manage the servers using Ansible.
3. **Ansible Configuration**: Ansible's inventory is pre-configured. You can start running Ansible commands from the control node to manage the other servers.

This setup provides a practical environment for installing and configuring a Kubernetes cluster from scratch using Ansible on Ubuntu servers.


