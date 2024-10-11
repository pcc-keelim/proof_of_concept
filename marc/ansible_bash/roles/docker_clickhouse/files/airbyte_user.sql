CREATE USER IF NOT EXISTS airbyte_user IDENTIFIED WITH plaintext_password BY 'airbyte_password';
GRANT CREATE ON * TO airbyte_user;
GRANT CREATE DATABASE ON *.* TO airbyte_user;
GRANT SELECT ON *.* TO airbyte_user;
GRANT INSERT, CREATE TABLE ON *.* TO airbyte_user;
GRANT DROP DATABASE ON *.* TO airbyte_user;
GRANT ALTER DELETE ON *.* TO airbyte_user;
GRANT TRUNCATE ON *.* TO airbyte_user;
GRANT DROP TABLE ON *.* to 'airbyte_user';