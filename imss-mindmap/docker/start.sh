#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR

# if command -v chcon &> /dev/null
# then
#     chcon -R -u unconfined_u -r object_r -t container_file_t .
# fi

if command -v podman-compose &> /dev/null; then
    export DOCKER_COMPOSE=podman-compose
else
    export DOCKER_COMPOSE=docker-compose
fi

${DOCKER_COMPOSE} --project-name activity-visualisation-imss-mindmap \
                  -f docker-compose.yml \
                  up -d
exit 0
