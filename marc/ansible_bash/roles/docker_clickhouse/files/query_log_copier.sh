interval=60 #defines how often the query is run 10 is every 10 seconds
filename="/var/log/clickhouse-server/query_log.json"
directory="/var/log/clickhouse-server/"
# we get all of the los before beginning if the file doesn't exist **
start_query="
SELECT
	user,
	query,
	query_kind ,
	databases ,
	tables ,
	exception ,
	stack_trace ,
	columns ,
	type,
	event_time,
	query_duration_ms,
	query_id ,
	address ,
	port ,
	is_initial_query ,
	initial_user ,
	initial_address ,
	initial_port ,
	initial_query_id ,
	read_rows,
	read_bytes ,
	written_rows ,
	written_bytes ,
	result_rows ,
	result_bytes ,
	memory_usage ,
	current_database
FROM system.query_log
WHERE
	user not like '%prod_dbt_user%'
	AND user not like '%stage_dbt_user%'
	AND user not like '%airbyte_user%'
	AND user not like '%prod_dagster%'
	AND user not like '%default%'
" 
start_datetime=""  
start_datetime_formatted=""  
end_datetime=""
end_datetime_formatted=""  
sleep 120 # allow server to boot up

echo "Begin Query Logging..."
while true; do  
	if [ ! -d "$directory" ]; then  
		echo "Directory does not exist. Creating directory..."  
		mkdir -p "$directory"  
	fi  
    if [ ! -f "$filename" ]; then 
		echo "Log file does not exist. Creating file..."  
        touch "$filename"
        clickhouse-client -q "$start_query" -f JSON >> "$filename" # **
    fi 

    if [ -z "$start_datetime" ]; then  
        start_datetime=$(date)  
    fi

    end_datetime=$(date -d "$start_datetime +$((interval - 1)) seconds")

    #ensures query begins at appropriate time
	current_epoch=$(date +%s)
	target_epoch=$(date -d "$end_datetime +1 seconds" +%s)
	sleep_seconds=$(( $target_epoch - $current_epoch ))
    if [[ $sleep_seconds -lt 0 ]]; then  
        sleep_seconds=0
        echo "WARNING query log is falling behind, consider raising interval"
    fi  
	sleep $sleep_seconds

    start_datetime_formatted=$(date -d "$start_datetime" +"%Y-%m-%d %T")
    end_datetime_formatted=$(date -d "$end_datetime" +"%Y-%m-%d %T")

    query="
SELECT
	user,
	query,
	query_kind ,
	databases ,
	tables ,
	exception ,
	stack_trace ,
	columns ,
	type,
	event_time,
	query_duration_ms,
	query_id ,
	address ,
	port ,
	is_initial_query ,
	initial_user ,
	initial_address ,
	initial_port ,
	initial_query_id ,
	read_rows,
	read_bytes ,
	written_rows ,
	written_bytes ,
	result_rows ,
	result_bytes ,
	memory_usage ,
	current_database ,
FROM system.query_log
WHERE
	user not like '%prod_dbt_user%'
	AND user not like '%stage_dbt_user%'
	AND user not like '%airbyte_user%'
	AND user not like '%prod_dagster%'
	AND user not like '%default%'
	AND event_time < '$end_datetime_formatted'
	AND event_time >'$start_datetime_formatted'
"
    clickhouse-client -q "$query" -f JSON >> "$filename"
    echo "Query logs run succesfully $start_datetime_formatted through $end_datetime_formatted"

    start_datetime=$(date -d "$end_datetime +1 seconds")
done  