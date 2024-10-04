## To be run within the docker container when first built

# simply run 'bash setup.sh' in the terminal to execute this script

# modify the contents of windows_shared/.dbt/profiles.yml
# replace any value following "ca_cert:" with "/windows_shared/.ssl/CMT-CA-CHAIN.crt"
sed -i 's/ca_cert: .*/ca_cert: \/root\/.ssl\/CMT-CA-CHAIN.crt/' /windows_shared/.dbt/profiles.yml

# modify the contents of windows_shared/secrets/secrets.yaml
# replace any value following "ca_cert:" with "/windows_shared/.ssl/CMT-CA-CHAIN.crt"
sed -i 's/ca_cert: .*/ca_cert: \/root\/.ssl\/CMT-CA-CHAIN.crt/' /windows_shared/secrets/secrets.yaml

# copy the contents of /windows_shared to /root
cp -r /windows_shared/* /root
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

# run dbt setup
cd  /code/ds-reporting-logic/src/dbt_datascience
dbt debug 
dbt compile