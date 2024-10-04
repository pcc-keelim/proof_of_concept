# Usage
## Regular usage

Come back to this if it's your first time.

Remember, docker desktop must be running for containers to work

No need to activate any python environments in the container, it is always active. If you have packages you want added, please create a ticker for DE

##      

### Starting and stopping the container

First you should note that you have two options, starting and stopping, or building and destroying

For starting and stopping, any changes you make should be saved in the container

- To stop the container
    - Open vscode and navigate to the docker extension tab on the far left
    - find the container under the containers dropdown, it should be called "ds_dev_image:latest" or something similar and have a green triangle indicating it is running
    - right click it and select stop
- To start the container
    - Open vscode and navigate to the docker extension tab on the far left
    - find the container under the containers dropdown, it should be called "ds_dev_image:latest" or something similar and have a red square indicating it is stopped
    - right click it and select start
    - wait for the green triangle to appear again, indicating it is running
    - then right click again and select "Attach Visual Studio Code"

If you destroy the container, everything will be gone. This may be useful if you break it
- To destroy the container
    - Open vscode and navigate to the docker extension tab on the far left
    - find the container under the containers dropdown, it should be called "ds_dev_image:latest" or something similar
    - right click it and select remove
- To rebuild the container Follow the steps under getting started below
##      
### Transferring files in and out of the container

There is a shared folder between your computer, and the container.
- On the container it is /windows_shared/
- On your computer it is in your home folder and called dockershare (ie "C:\Users\doej\dockershare")

Anything you put in one, will appear in the other. You cannot move the folders.

In the docker container, to move something from whatever folder the terminal is in, to the shared folder, use the following command:

`cp . /windows_shared/`

Or, if it is in another location

`cp /path/to/file /windows_shared/`

You can then find the file 
"C:\Users\doej\dockershare"

Reverse the process for moving something to the container.
## Getting started
1. Ensure docker desktop is running
    - Simply open the application and ensure in the bottom left it says 'Engine running'
2. Run the startup.sh script
    - open a bash terminal (either git bash or wsl) in the directory the script and .tar file are in
    - run `bash startup.sh`
    - this moves files and starts the container and creates a volume
    - the container is now running
3. Attach vscode to the container
    - Open vscode and navigate to the docker extension tab on the far left
    - find the container under the containers dropdown, it should be called "ds_dev_image:latest" or something similar and have a green triangle indicating it is running
    - right click it and select "Attach Visual Studio Code"
    - A new window of visual studio code will launch
4. Run the setup script
    - Press <cntrl + ~> to open a terminal
    - run `bash /setup.sh'
    - follow the prompts
    - this will set up dbt on reporting logic and move some files around, should take no more than 5 minutes
5. Open a folder
    - Either click the button that says open folder or find it under File > Open Folder
    - Generally you will want to open /code/ds-reporting-logic
    - If you need to see where other files are in the container, open /

 
##      
# Requirements

## Files
For this to work as intended, in your home folder (ie "C:\Users\doej") you must have the following directories and files

- directory
    - file
- .ssh
    - id_rsa
    - known_hosts
- .ssl
    - CMT_Root_CA.pem
    - CMT-CA-CHAIN.crt
- .dbt
    - profiles.yml
- secrets
    - secrets.yaml
it's ok if there are more files in those directories, they just need those at minimum
## Software
Additionally you will need the following:
- Docker Desktop, and an account
- Vscode 
    - With the docker extension
