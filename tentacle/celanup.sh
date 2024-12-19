#!/bin/bash

# Check if an image name is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <image_name>"
    exit 1
fi

IMAGE_NAME=$1

# Get and stop all containers using the specified image
CONTAINERS=$(docker ps -q --filter "ancestor=$IMAGE_NAME")

if [ -z "$CONTAINERS" ]; then
    echo "No running containers found using image: $IMAGE_NAME"
else
    echo "Stopping and removing the following containers using image: $IMAGE_NAME"
    docker stop $CONTAINERS
    docker rm $CONTAINERS
fi