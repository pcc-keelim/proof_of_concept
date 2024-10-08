## Key Components:
1. scripts/: This folder will store all your Bash scripts.
    - Example: example_script.sh
2. `ansible/playbooks/copy_execute_script.yml`: The Ansible playbook responsible for copying and executing the Bash script on target hosts.
3. `ansible/inventory/hosts`: Inventory file listing your target hosts (e.g., [webservers]).
4. `ansible/roles/execute_script/tasks/main.yml`: This file defines the task to copy and execute the script on the remote host.
5. `ansible/roles/execute_script/files/scripts/`: This folder contains scripts that Ansible will copy to the target host.


## prepare_knowledge_base.py
Python script that will recursively gather all the files in a target folder and add their contents to a single file, which you can then upload into a custom ChatGPT instance to serve as the knowledge base. It will also add to the top of the output the file structure to better give context to the gpt. 
`python3 prepare_knowlege_base.py ./ ~/Downloads`