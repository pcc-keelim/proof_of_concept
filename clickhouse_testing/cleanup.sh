sudo rm -rf ./clickhouse_logs
sudo rm -rf ./clickhouse_database
mkdir ./clickhouse_database
sudo chown clickhouse:clickhouse clickhouse_database/
sudo chown clickhouse:clickhouse clickhouse-server/
sudo chmod -R 775 ./clickhouse-server/
docker-compose up --force-recreate 