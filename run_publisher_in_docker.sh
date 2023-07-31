#!/usr/bin/env sh
set -e
set -x

cd /app

DIRECTORY="$PWD"

export PYTHONPATH="$DIRECTORY/service:$DIRECTORY"
echo "$PYTHONPATH"

cd "$DIRECTORY"

# run project
python ./publisher/main.py
