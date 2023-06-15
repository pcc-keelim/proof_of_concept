SET allow_introspection_functions=1;
CREATE USER IF NOT EXISTS admin_marc IDENTIFIED BY 'analyst_password_01';
GRANT ALL ON *.* TO admin_marc WITH GRANT OPTION;
SET allow_introspection_functions=0;

CREATE USER IF NOT EXISTS jdoe IDENTIFIED BY 'analyst_password_01';
CREATE DATABASE IF NOT EXISTS dev_jdoe; 
-- CREATE TABLE IF NOT EXISTS dev_jdoe.home (
--     home_id String
-- ) 
-- ENGINE = MergeTree AS SELECT 1;
GRANT SELECT, INSERT, ALTER, CREATE ON dev_jdoe.* TO fred;