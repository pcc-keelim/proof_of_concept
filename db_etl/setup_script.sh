sudo rm -rf ./clickhouse_logs
# Remove for productsion
sudo rm -rf /data/ch_db
# Remove for productsion
sudo mkdir /data/ch_db

# Create flags file if not exists
file=flags.yml
if [ ! -e "$file" ] ; then
    touch "$file"
fi

sudo chown clickhouse:clickhouse /data/ch_db/
sudo chmod -R 770 /data/ch_db/
sudo chown clickhouse:clickhouse clickhouse-server/
sudo chmod -R 770 ./clickhouse-server/
docker compose -f docker-compose-db-etl.yml up -d
