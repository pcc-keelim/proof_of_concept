# To be run on your local machine to start the docker container
# this assumes you already have the latest image from data engineering

# this also assumes you have:
# your ssh info in the .ssh folder in your user directory
# your dbt profiles.yml in the .dbt folder in your user directory
# your ssl certs in the .ssl folder in your user directory

# If you do not, please ensure you do before running.

# to run open a bash (git bash or WSL) terminal in whichever directory this file is in and run the following command
# check if the image is loaded
docker images | grep ds_dev_image
# if the image is loaded, prompt the user if they want to overwrite it
if [ $? -eq 0 ]; then
    echo "Do you want to overwrite the image? (y/n)"
    read overwrite
    if [ $overwrite == "y" ]; then
        echo "Loading image..."
        docker load -i ds_dev_image.tar
    fi
else
    echo "Image not found. Loading image..."
    docker load -i ds_dev_image.tar
fi

# bash startup.sh
mkdir ${USERPROFILE}/dockershare
# copy the contents of the .ssh, .dbt and .ssl folder to dockershare
cp -r ${USERPROFILE}/.ssh ${USERPROFILE}/dockershare/.ssh
cp -r ${USERPROFILE}/.dbt ${USERPROFILE}/dockershare/.dbt
cp -r ${USERPROFILE}/.ssl ${USERPROFILE}/dockershare/.ssl
cp -r ${USERPROFILE}/secrets ${USERPROFILE}/dockershare/secrets

docker run -d -v ${USERPROFILE}/dockershare:/windows_shared -it ds_dev_image