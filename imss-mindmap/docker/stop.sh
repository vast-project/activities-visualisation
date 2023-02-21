#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

if command -v podman-compose &> /dev/null; then
    export DOCKER_COMPOSE=podman-compose
else
    export DOCKER_COMPOSE=docker-compose
fi

${DOCKER_COMPOSE} --project-name activity-visualisation-imss-mindmap \
                  -f docker-compose.yml \
                  down

exit 0
