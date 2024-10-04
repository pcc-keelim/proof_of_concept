# To be run on your local machine to start the docker container
# this assumes you already have the latest image from data engineering

# this also assumes you have:
# your ssh info in the .ssh folder in your user directory
# your dbt profiles.yml in the .dbt folder in your user directory
# your ssl certs in the .ssl folder in your user directory

# If you do not, please ensure you do before running.

# to run open a bash (or WSL) terminal in whichever directory this file is in and run the following command
# bash startup.sh
mkdir ${USERPROFILE}/dockershare
# copy the contents of the .ssh, .dbt and .ssl folder to dockershare
cp -r ${USERPROFILE}/.ssh ${USERPROFILE}/dockershare/.ssh
cp -r ${USERPROFILE}/.dbt ${USERPROFILE}/dockershare/.dbt
cp -r ${USERPROFILE}/.ssl ${USERPROFILE}/dockershare/.ssl

 docker run -v ${USERPROFILE}/dockershare:/windows_shared -it test