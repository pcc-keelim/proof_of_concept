Repo Located Here:
    https://github.com/ClickHouse/ClickHouse/tree/master/docker/server
Releases Described Here:
    https://github.com/ClickHouse/ClickHouse/releases 
Registery Located Here:
    https://registry.hub.docker.com/r/clickhouse/clickhouse-server/tags
To get images on to the machine: 
1. docker save -o clickhouse-server_23.5.3.24.tar clickhouse/clickhouse-server:23.5.3.24
2. scp .\clickhouse-server_23.5.3.24.tar dc2-ds-db-01.int.collectivemedicaltech.com:~/
3. docker load -i ./clickhouse-server_23.5.3.24.tar


the way to get this up and running is to
1. execute `docker-compose up` and wait for it to fail
2. Then `sudo chown -R clickhouse:clickhouse ./clickhouse_database/`
3. Then `sudo chown -R clickhouse:clickhouse ./clickhouse_logs/`
4. You should then be able to start up the server without any issue. 
