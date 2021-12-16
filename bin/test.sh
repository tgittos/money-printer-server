#!/bin/bash

docker exec --tty $(docker-compose -f docker-compose.dev.yml ps -q api) /bin/bash -c "MP_ENVIRONMENT=test PYTHONPATH=src pytest src/"