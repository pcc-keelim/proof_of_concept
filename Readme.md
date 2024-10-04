# Setup ssh (only for WSL, skip if not)

### Install needed linux packages
```bash
sudo apt-get install keychain openssh-client
```

### Configure ~/.ssh folder

Can simply copy an existing .ssh folder from windows or linux

### Configure ~/.profile

Add the following to your ~/.profile at the bottom:

```bash
# load keychain
eval $(keychain --quiet --eval --agents ssh id_rsa)

# start ssh-agent
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval $(ssh-agent -s)
    ssh-add ~/.ssh/id_rsa
fi
```

At this point, whenever a wsl session is opened, the ssh-agent should be started and your key should be loaded

# Setup credentials

Create a folder named "secrets" at the top level of this repository, at the same level as this readme.

Copy "~/secrets/secrets.yaml", "~/.dbt/profiles.yaml", and CMT_Root_CA.pem into this folder

# Setup ds-reporting-logic and ds-reporting-scheduling


# Create the dev container, and attach vscode to it

Press F1, and select "Dev Containers: Reopen in container"

This will create the container, and also do the following:
* installs customizable vscode settings such as extensions, found in devcontainer.json
* run setup.sh, which installs the repos as python packages, runs dbt compile, and configures git for use
* run startup.sh, which starts dagster dev on port 3000


