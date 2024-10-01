FROM python:3.11-slim
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    git-all \
    gnupg \
    curl \
    telnetd



# Register the Microsoft Ubuntu repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
# Update the list of products
RUN apt-get update -y
# Install MS SQL ODBC Driver
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
# Verify if the MS SQL ODBC Driver is installed
RUN odbcinst -q -d -n "ODBC Driver 17 for SQL Server"

# # Add non-root user
# ARG USERNAME=nonroot
# RUN groupadd --gid 1000 $USERNAME && useradd --uid 1000 --gid 1000 -m $USERNAME
# ## Make sure to reflect new user in PATH
# ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
# USER $USERNAME

# # Add dbt profiles
# COPY ~/.dbt/profiles.yml /root/.dbt/profiles.yml


# # Add dbt credentials
# ARG SERVER_INSTANCE
# ARG DBT_USER
# ARG DBT_PASSWORD
# ARG DBT_DATASCIENCE_TARGET
# ENV SERVER_INSTANCE=$SERVER_INSTANCE
# ENV DBT_USER=$DBT_USER
# ENV DBT_PASSWORD=$DBT_PASSWORD
# ENV DBT_DATASCIENCE_TARGET=$DBT_DATASCIENCE_TARGET

# # pre-compile dbt models
# WORKDIR /opt/ds-reporting-logic/src/dbt_datascience/
# RUN dbt debug
# RUN dbt deps
# RUN dbt compile

# # install ds-reporting-scheduling
# COPY ./ds-reporting-scheduling/ /opt/ds-reporting-scheduling
# WORKDIR /opt/ds-reporting-scheduling
# RUN pip install .

# COPY ./ds-infrastructure/deploy_dagster_dbt/entry_files/ /opt/ds-reporting-logic/src/dbt_datascience/

# # Clean up dbt credentials
# RUN unset DBT_USER
# RUN unset DBT_PASSWORD
# RUN unset DBT_DATASCIENCE_TARGET

# RUN pip install --no-cache-dir protobuf==4.25.3