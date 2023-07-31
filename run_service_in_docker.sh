#!/usr/bin/env sh
set -e
set -x

cd /app

DIRECTORY="$PWD"

export PYTHONPATH="$DIRECTORY"
echo "$PYTHONPATH"

# migrate DB
cd $DIRECTORY/migrations
alembic upgrade head

cd "$DIRECTORY"

# run project
python ./service/main.py
