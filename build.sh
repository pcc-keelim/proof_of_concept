# to be run on your local machine to build the image after a new deployment (if necessary)
git clone 
git clone

docker build -t ds_dev_image .
docker save -o ds_dev_image.tar ds_dev_image:latest