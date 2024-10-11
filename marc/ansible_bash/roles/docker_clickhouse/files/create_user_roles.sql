-- DE Pod
CREATE ROLE IF NOT EXISTS data_engineers;
GRANT SELECT, INSERT, ALTER, CREATE, DROP TABLE, TRUNCATE, OPTIMIZE, DROP VIEW ON shared_ds.* TO data_engineers;
GRANT SELECT, INSERT, ALTER, CREATE, DROP TABLE, TRUNCATE, OPTIMIZE, DROP VIEW ON stage.* TO data_engineers;
GRANT SELECT ON *.* TO data_engineers;
-- AE Pod
CREATE ROLE IF NOT EXISTS analytics_engineers;
GRANT SELECT ON raw_gdb.* TO analytics_engineers;
GRANT SELECT ON raw_criteria.* TO analytics_engineers;
GRANT SELECT ON raw_insights.* TO analytics_engineers;
GRANT SELECT ON raw_report.* TO analytics_engineers;
GRANT SELECT ON raw_encounters.* TO analytics_engineers;
GRANT SELECT ON prod.* TO analytics_engineers;
GRANT SELECT ON stage.* TO analytics_engineers;
GRANT SELECT ON system.processes TO analytics_engineers;
GRANT SELECT ON learning.* TO analytics_engineers;
GRANT SELECT ON raw_sf.* TO analytics_engineers;
GRANT SELECT, INSERT, ALTER, CREATE, DROP TABLE, TRUNCATE, OPTIMIZE, DROP VIEW ON shared_ds.* TO analytics_engineers;
-- Analysts
CREATE ROLE IF NOT EXISTS data_analyst;
GRANT SELECT ON prod.* TO data_analyst;
GRANT SELECT ON stage.* TO data_analyst;
GRANT SELECT ON learning.* TO data_analyst;
GRANT SELECT, INSERT, ALTER, CREATE, DROP TABLE, TRUNCATE, OPTIMIZE, DROP VIEW ON shared_ds.* TO data_analyst;