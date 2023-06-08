SET allow_introspection_functions=1;
CREATE USER IF NOT EXISTS admin_marc IDENTIFIED BY 'analyst_password_01';
GRANT ALL ON *.* TO admin_marc WITH GRANT OPTION;
SET allow_introspection_functions=0;

CREATE USER IF NOT EXISTS fred IDENTIFIED BY 'analyst_password_01';
CREATE DATABASE IF NOT EXISTS dev_fred; 
CREATE TABLE IF NOT EXISTS dev_fred.home (
    home_id String
) 
ENGINE = MergeTree AS SELECT 1;
GRANT SELECT, INSERT, ALTER, CREATE ON dev_fred.* TO fred;