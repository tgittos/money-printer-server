#!/bin/bash

docker exec --tty $(docker compose ps -q api) /bin/bash -c "MP_ENVIRONMENT=test PYTHONPATH=src pytest --cov-config=.coveragerc --cov=src --cov-report term:skip-covered src/"