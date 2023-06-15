the way to get this up and running is to
1. execute `docker-compose up` and wait for it to fail
2. Then `sudo chown -R clickhouse:clickhouse ./clickhouse_database/`
3. Then `sudo chown -R clickhouse:clickhouse ./clickhouse_logs/`
4. You should then be able to start up the server without any issue. 
