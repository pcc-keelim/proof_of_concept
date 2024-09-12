This folder is to set up a mock bare metal server and the set up k8s on that server using the ansible service

[Link to video](https://youtu.be/lvkpIoySt3U?si=JL0AErUN3QxRSDw0)

When inside the ansible container make sure to checkout a specific release branch of kubespray as the latest has un-tested changed.
I am going with `release-2.24` as it is not the latest but one previous and is most likely to be stable.

# environment setup
install requirements in venv and create some files

```bash
cd /home/ansible/kubespray
su ansible
bash
python3 -m venv venv
source ./venv/bin/activate
pip3 install ruamel.yaml
pip3 install -U -r requirements.txt
```

Now, for each server we need to create an ansible user and establish ssh connectivity. 
On the ansible container run this command to generate the ssh key

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -q -N ""
```
Explanation-
- `ssh-keygen` This is the command used to generate, manage, and convert authentication keys for SSH (Secure Shell).
- `-t ed25519` This option specifies the type of key to create. In this case, it’s using the Ed25519 algorithm, which is known for its high security and performance.
- `-f ~/.ssh/id_ed25519` This option specifies the file in which to save the generated key. Here, the key will be saved in the ~/.ssh directory with the filename id_ed25519.
- `-q` This option stands for “quiet” mode. It suppresses the output of the command, making it less verbose.
- `-N ""` This option sets the passphrase for the key. An empty string "" means no passphrase is set, allowing for passwordless authentication.

Next we need to create a password that we will use to automate the ssh password entry and copy the ssh public keys to the remote servers
```bash
touch password.txt
echo password > password.txt

```
shh into the servers with a password  and accept fingerprint then exit
```bash
sshpass -f password.txt ssh -o StrictHostKeyChecking=no ansible@control-node exit
sshpass -f password.txt ssh -o StrictHostKeyChecking=no ansible@server1 exit
sshpass -f password.txt ssh -o StrictHostKeyChecking=no ansible@server2 exit
sshpass -f password.txt ssh -o StrictHostKeyChecking=no ansible@server3 exit
```

then for each server we need to copy over the public key
```bash
sshpass -f password.txt ssh-copy-id -i ~/.ssh/id_ed25519.pub ansible@control-node
sshpass -f password.txt ssh-copy-id -i ~/.ssh/id_ed25519.pub ansible@server1
sshpass -f password.txt ssh-copy-id -i ~/.ssh/id_ed25519.pub ansible@server2
sshpass -f password.txt ssh-copy-id -i ~/.ssh/id_ed25519.pub ansible@server3
```

# cluster-variable.yaml
```bash
touch inventory/proxmos01/cluster-variable.yaml
```

```yaml
kube_version: v1.30.4
helm_enabled: true
kube_proxy_mode: iptables
# issues templating out for deployment so will do it later
# metallb_enabled: true
# metallb_speaker_enabled: true
# metallb_config:
#   address_pools:
#     primary:
#       ip_range:
#         - "10.0.0.1-10.0.0.128"
#       auto_assign: true
#     layer2:
#         - primary
```

# host.yaml
hosts.yaml has been modified to reflect something more similar to our production environment.
```yaml
all:
  hosts:
    control-node:
      ansible_host: 10.0.0.3
      ip: 10.0.0.3
      access_ip: 10.0.0.3
    server1:
      ansible_host: 10.0.0.4
      ip: 10.0.0.4
      access_ip: 10.0.0.4
    server2:
      ansible_host: 10.0.0.5
      ip: 10.0.0.5
      access_ip: 10.0.0.5
    server3:
      ansible_host: 10.0.0.6
      ip: 10.0.0.6
      access_ip: 10.0.0.6
  children:
    kube_control_plane:
      hosts:
        control-node:
    kube_node:
      hosts:
        server1:
        server2:
        server3:
    etcd:
      hosts:
        control-node:
        server1:
        server2:
    k8s_cluster:
      children:
        kube_control_plane:
        kube_node:
    calico_rr:
      hosts: {}
```

```bash
ansible-playbook -i inventory/mycluster/inventory -e @inventory/mycluster/cluster-variable.yaml --become --become-user=root -u ansible cluster.yml
ansible-playbook -i inventory/mycluster/inventory -b -v --private-key=/home/ansible/.ssh/id_ed25519
```

Creates this error:
```
TASK [kubespray-defaults : Create fallback_ips_base] **************************************************************************************************************************************************
fatal: [control-node -> localhost]: FAILED! => {"msg": "The task includes an option with an undefined variable. The error was: 'None' has no attribute 'get'. 'None' has no attribute 'get'\n\nThe error appears to be in '/home/ansible/kubespray/roles/kubespray-defaults/tasks/fallback_ips.yml': line 18, column 3, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n\n- name: Create fallback_ips_base\n  ^ here\n"}
```

from this task
```yaml
- name: Create fallback_ips_base
  set_fact:
    fallback_ips_base: |
      ---
      {% set search_hosts = (ansible_play_hosts_all + [groups['kube_control_plane'][0]]) | unique if ansible_limit is defined else (groups['k8s_cluster'] | default([]) + groups['etcd'] | default([]) + groups['calico_rr'] | default([])) | unique %}
      {% for item in search_hosts %}
      {% set found = hostvars[item].get('ansible_default_ipv4') %}
      {{ item }}: "{{ found.get('address', '127.0.0.1') }}"
      {% endfor %}
  delegate_to: localhost
  connection: local
  delegate_facts: true
  become: false
  run_once: true
```