#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

ACTIVITIES_VISUALISATION_DIR=$( dirname  "$SCRIPT_DIR" )

ACTIVITIES=(`ls -d --hide=".*/systemd/" -- "$ACTIVITIES_VISUALISATION_DIR"/*/`)

SCRIPT="restart.sh"

for path in ${ACTIVITIES[@]}; do
  FILE="${path}docker/$SCRIPT"
  TOOL=$( basename "$path" )
  if [ -f "$FILE" ]; then
    echo "Starting Service: $TOOL"
    /bin/bash "$FILE"
  fi
done

