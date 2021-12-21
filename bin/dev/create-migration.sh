#!/bin/bash

if [ -z "$1" ]; then
    echo "Migration name required"
    exit 1
fi

docker exec --tty $(docker compose ps -q api) /bin/bash -c "cd src && MP_ENVIRONMENT=development alembic revision --autogenerate -m \"$1\""