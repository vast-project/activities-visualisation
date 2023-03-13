#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd $SCRIPT_DIR

echo "Working directory is:" `pwd`

PROJECT_NAME="vast-imss-vis-app-httpreq"
PROJECT_VERSION="v0.0.1"

IMAGE_NAME=${PROJECT_NAME}
IMAGE_VERSION=${PROJECT_VERSION}
DOCKER_HUB_NAME=docker.io/chdamdesinger/${IMAGE_NAME}

set -e

## Generate docker image...
docker build \
  -t ${DOCKER_HUB_NAME}:${IMAGE_VERSION} \
  -t ${DOCKER_HUB_NAME}:latest \
  .

## Push image to docker.io
docker login docker.io

docker push ${DOCKER_HUB_NAME}:${IMAGE_VERSION}
docker push ${DOCKER_HUB_NAME}:latest
