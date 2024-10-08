## To be run within the docker container when first built

# simply run 'bash setup.sh' in the terminal to execute this script

# modify the contents of windows_shared/.dbt/profiles.yml
# replace any value following "ca_cert:" with "/windows_shared/.ssl/CMT-CA-CHAIN.crt"
sed -i 's/ca_cert: .*/ca_cert: \/root\/.ssl\/CMT-CA-CHAIN.crt/' /windows_shared/.dbt/profiles.yml

# modify the contents of windows_shared/secrets/secrets.yaml
# replace any value following "ca_cert:" with "/windows_shared/.ssl/CMT-CA-CHAIN.crt"
sed -i 's/ca_cert: .*/ca_cert: \/root\/.ssl\/CMT-CA-CHAIN.crt/' /windows_shared/secrets/secrets.yaml

# copy the contents of /windows_shared to /root
mkdir /root/.ssh
cp -r /windows_shared/.ssh/* /root/.ssh
mkdir /root/.dbt
cp -r /windows_shared/.dbt/* /root/.dbt
mkdir /root/.ssl
cp -r /windows_shared/.ssl/* /root/.ssl
mkdir /root/secrets
cp -r /windows_shared/secrets/* /root/secrets

chmod -R 700 /root/.ssh

# copy pem file to etc/ssl/certs
cp /root/.ssl/CMT_Root_CA.pem /etc/ssl/certs

# prompt git config email and name
echo "Enter your git user name (ie john.doe):"
read git_name
git config --global user.name $git_name

echo "Enter your git email (ie doej@pointclickcare.com):"
read git_email
git config --global user.email $git_email

# trust git repos in /code
git config --global --add safe.directory /code/ds-reporting-logic
git config --global --add safe.directory /code/ds-reporting-scheduling

# git fetch, checkout master and pull on both repos
cd /code/ds-reporting-logic
git fetch
git checkout master
git pull

cd /code/ds-reporting-scheduling
git fetch
git checkout master
git pull


# run dbt setup
cd  /code/ds-reporting-logic/src/dbt_datascience
echo "running dbt debug"
dbt debug 
echo "running dbt compile"
dbt compile