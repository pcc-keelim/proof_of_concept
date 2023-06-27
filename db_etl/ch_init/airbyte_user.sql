CREATE USER airbyte_user IDENTIFIED WITH plaintext_password BY 'airbyte_password';
GRANT CREATE ON * TO airbyte_user;
CREATE DATABASE raw_gdb;
GRANT CREATE DATABASE ON *.* TO airbyte_user;
GRANT CREATE TABLE ON raw_gdb.* TO airbyte_user;
GRANT DROP TABLE ON raw_gdb.* TO airbyte_user;
GRANT TRUNCATE ON raw_gdb.* TO airbyte_user;
GRANT SELECT ON raw_gdb.* TO airbyte_user;
GRANT INSERT ON raw_gdb.* TO airbyte_user;