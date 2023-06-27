sudo rm -rf ./clickhouse_logs
# Remove for productsion
sudo rm -rf ./clickhouse_database
# Remove for productsion
mkdir ./clickhouse_database

# Create flags file if not exists
file=flags.yml
if [ ! -e "$file" ] ; then
    touch "$file"
fi

sudo chown clickhouse:clickhouse clickhouse_database/
sudo chown clickhouse:clickhouse clickhouse-server/
sudo chmod -R 775 ./clickhouse-server/
docker compose up --force-recreate --no-cache
