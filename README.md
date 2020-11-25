# Containerizable service for testing service represented in "3net_mnist"

## Build
    docker build -t new_image_testing .

## Run
    docker run -it --rm -d -p 8090:80 --name 3net_mnist_testing new_image_testing