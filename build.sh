# to be run on your local machine to build the image after a new deployment (if necessary)
git clone ssh://git@bitbucket.collectivemedicaltech.com:7999/dh/ds-reporting-scheduling.git
git clone ssh://git@bitbucket.collectivemedicaltech.com:7999/dh/ds-reporting-logic.git

docker build -t ds_dev_image .
docker save -o ds_dev_image.tar ds_dev_image:latest

remove -rf ds-reporting-scheduling
remove -rf ds-reporting-logic