FROM python:3.11-slim
RUN pip install --upgrade pip
# get linux utilities
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    git-all \
    gnupg \
    curl \
    telnetd \
    dos2unix \
    openssh-client \
    tmux

# Register the Microsoft Ubuntu repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
# Update the list of products
RUN apt-get update -y
# Install MS SQL ODBC Driver
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
# Verify if the MS SQL ODBC Driver is installed
RUN odbcinst -q -d -n "ODBC Driver 17 for SQL Server"


# Create code directory
RUN mkdir -p /code
WORKDIR /code

# RUN ssh-keyscan bitbucket.collectivemedicaltech.com >> /root/.ssh/known_hosts
# # # Clone the repositories
COPY ./ds-reporting-logic /code/ds-reporting-logic
COPY ./ds-reporting-scheduling /code/ds-reporting-scheduling
RUN git config --global core.autocrlf input

# # # Install the requirements
WORKDIR /code/ds-reporting-logic
RUN pip install -e .
WORKDIR /code/ds-reporting-scheduling
RUN pip install -e .

# dbt setup
WORKDIR /code/ds-reporting-logic/src/dbt_datascience
RUN dbt deps
# RUN dbt compile
WORKDIR /code/ds-reporting-logic/src/dbt_etl
RUN dbt deps



# # Install vscode server
# RUN curl -fsSL https://code-server.dev/install.sh | sh
# RUN curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' --output vscode_cli.tar.gz
# RUN tar -xf vscode_cli.tar.gz

# RUN apt install software-properties-common apt-transport-https wget -y
# RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- |  apt-key add -
# RUN add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
# RUN apt update
# RUN apt install code -y

# # # Install the extensions
# # RUN code-server --install-extension github.copilot
# # RUN code-server --install-extension github.copilot-chat
# # RUN code-server --install-extension ms-python.vscode-pylance
# # RUN code-server --install-extension visualstudioexptteam.intellicode-api-usage-examples
# # RUN code-server --install-extension visualstudioexptteam.vscodeintellicode
# # RUN code-server --install-extension ms-vsliveshare.vsliveshare
# # RUN code-server --install-extension wisetime.branch-in-window-title
# RUN code-server --install-extension gruntfuggly.todo-tree
# RUN code-server --install-extension kevinrose.vsc-python-indent
# RUN code-server --install-extension mark-wiemer.vscode-autohotkey-plus-plus     
# RUN code-server --install-extension mechatroner.rainbow-csv
# RUN code-server --install-extension ms-python.debugpy
# RUN code-server --install-extension ms-python.isort
# RUN code-server --install-extension ms-python.python
# RUN code-server --install-extension ms-toolsai.jupyter
# RUN code-server --install-extension ms-toolsai.jupyter-keymap
# RUN code-server --install-extension ms-toolsai.vscode-jupyter-cell-tags
# RUN code-server --install-extension ms-toolsai.vscode-jupyter-slideshow
# RUN code-server --install-extension ms-vscode.makefile-tools
# RUN code-server --install-extension ms-vscode.notepadplusplus-keybindings       
# RUN code-server --install-extension redhat.vscode-yaml
# RUN code-server --install-extension streetsidesoftware.code-spell-checker
# RUN code-server --install-extension tamasfe.even-better-toml
# RUN code-server --install-extension vmware.vscode-manifest-yaml
# RUN code-server --install-extension vscjava.vscode-gradle
# RUN code-server --install-extension vscjava.vscode-maven


# Expose the port
EXPOSE 8080
EXPOSE 3000

# Copy setup.sh over to the container
COPY ./setup.sh /setup.sh
RUN dos2unix /setup.sh


WORKDIR /code/ds-reporting-scheduling
COPY .env /code/ds-reporting-scheduling/.env
# CMD ["dagster", "dev"]
CMD ["tail", "-f", "/dev/null"]