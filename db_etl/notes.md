Airbyte user needs the following permissions in ClickHouse
CREATE USER 'airbyte_user'@'%' IDENTIFIED BY 'your_password_here';

GRANT SELECT ON gdb.* TO 'airbyte_user'@'%';
GRANT SELECT ON INFORMATION_SCHEMA.* TO 'airbyte_user'@'%';

GRANT CREATE ON *.* TO 'airbyte_user';

<!-- GRANT CREATE DATABASE ON *.* to 'airbyte_user'; -->
GRANT DROP TABLE ON *.* to 'airbyte_user';

Command to build
docker-compose -f .\docker-compose-db-etl.yml build --no-cache

Command to stand up
docker-compose -f .\docker-compose-db-etl.yml up



Modifications to server
Use ufw tool to modify ports
allow port forwarding by configuring it to forward traffic from an external port to an internal port. Before you configure UFW to allow port forwarding, you must enable packet forwarding. You can do this by editing the UFW configuration file located at /etc/default/ufw and changing the value of DEFAULT_FORWARD_POLICY from DROP to ACCEPT.

https://hub.docker.com/r/clickhouse/clickhouse-server/

CREATE DATABASE dev_butler;
GRANT SELECT, UPDATE ...... to butler;