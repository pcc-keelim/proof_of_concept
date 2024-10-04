#!/bin/bash

# Install ds-reporting-logic
cd  /code/ds-reporting-logic
pip install -e .

# Install ds-reporting-scheduling
cd /code/ds-reporting-scheduling
pip install -e .

# Run dbt commands in the second repository
cd  /code/ds-reporting-logic/src/dbt_datascience
dbt debug
dbt deps
dbt compile

# Add repositories to safe directory
git config --global --add safe.directory  /code/ds-reporting-logic
git config --global --add safe.directory  /code/ds-reporting-scheduling