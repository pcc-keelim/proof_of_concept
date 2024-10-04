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
    openssh-client 

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
RUN curl -fsSL https://code-server.dev/install.sh | sh

# # Install the extensions
RUN code-server --install-extension ms-python.python
RUN code-server --install-extension ms-toolsai.jupyter
# RUN code-server --install-extension github.copilot

# Expose the port
EXPOSE 8080
EXPOSE 3000

# Copy setup.sh over to the container
COPY ./setup.sh /setup.sh
RUN dos2unix /setup.sh

# Start dagster dev server

WORKDIR /code/ds-reporting-scheduling
COPY .env /code/ds-reporting-scheduling/.env
# CMD ["dagster", "dev"]
CMD ["tail", "-f", "/dev/null"]