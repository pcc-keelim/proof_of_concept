Repo [Located Here](https://github.com/ClickHouse/ClickHouse/tree/master/docker/server)

Releases [Described Here](https://github.com/ClickHouse/ClickHouse/releases)

Registery [Located Here](https://registry.hub.docker.com/r/clickhouse/clickhouse-server/tags)

How to lock down Clickhouse
- [Video](https://www.youtube.com/watch?v=O5JWXLv_1ZQ&t=1458s)
- [GitHub Repo](https://github.com/Altinity/clickhouse-sql-examples/tree/main/fortress-clickhouse)
    
To get images on to the machine: 
1. docker save -o clickhouse-server_23.5.3.24.tar clickhouse/clickhouse-server:23.5.3.24
2. scp .\clickhouse-server_23.5.3.24.tar dc2-ds-db-01.int.collectivemedicaltech.com:~/
3. docker load -i ./clickhouse-server_23.5.3.24.tar


the way to get this up and running is execute the following script
- `setup_script.sh`

<br><br>

Airbyte user needs the following permissions in ClickHouse
CREATE USER 'airbyte_user'@'%' IDENTIFIED BY 'your_password_here';

GRANT SELECT ON raw_*.* TO 'airbyte_user'@'%';
GRANT SELECT ON prod_*.* TO 'airbyte_user'@'%';
GRANT SELECT ON stage_*.* TO 'airbyte_user'@'%';
GRANT SELECT ON INFORMATION_SCHEMA.* TO 'airbyte_user'@'%';

GRANT CREATE ON *.* TO 'airbyte_user';

GRANT CREATE DATABASE ON *.* to 'airbyte_user';
GRANT DROP TABLE ON *.* to 'airbyte_user';



Modifications to server
Use ufw tool to modify ports
allow port forwarding by configuring it to forward traffic from an external port to an internal port. Before you configure UFW to allow port forwarding, you must enable packet forwarding. You can do this by editing the UFW configuration file located at /etc/default/ufw and changing the value of DEFAULT_FORWARD_POLICY from DROP to ACCEPT.

https://hub.docker.com/r/clickhouse/clickhouse-server/

CREATE DATABASE dev_butler;
GRANT SELECT, UPDATE ...... to butler;

https://www.youtube.com/watch?v=pilKEtyf9fk
https://docs.altinity.com/operationsguide/security/clickhouse-hardening-guide/


Deployemnt process best practice
<!-- This is supposed to work better -->
https://github.com/gongbell/ContractFuzzer/issues/5 
1: Export Image (will need image name)
  - Example: `docker save -o altinity/clickhouse-server clickhouse-server.tar`
2: scp clickhouse-server.tar to the server
  - Example: `scp C:\Users\keelim\Documents\dev\clickhouse\clickhouse-server.tar dc2-ds-db-01.int.collectivemedicaltech.com:~/`
3: docker import the file
  - Example: `docker load -i clickhouse-server.tar`
4: Build the container with the docker-compose file
  - Example: ``

  

  Make sure that the docker demon network is modified so that it does not use the incorrect subnet and lock up the server communication. [see this article](https://medium.com/@jacob.swanson.n/making-docker-use-different-ip-ranges-on-ubuntu-27ba6cbb825d)
  
  Create the following file 
  `/etc/docker/daemon.json`
  ``` json
  {
  "bip": "10.10.0.5/24",
  "default-address-pools": [
    {
      "base": "10.11.0.0/16",
      "size": 24
    }
  ]
}
```