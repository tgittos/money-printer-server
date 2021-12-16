#!/bin/bash

source .env.dev

echo "Creating user $MP_DB__USERNAME in db mp_dev"
docker compose -f docker-compose.dev.yml run --rm db mysql --user=root --password=$MYSQL_ROOT_PASSWORD --execute="CREATE USER '$MP_DB__USERNAME' IDENTIFIED BY '$MP_DB__PASSWORD'"

echo "Creating db mp_dev and granting access to $MP_DB__USERNAME"
docker compose -f docker-compose.dev.yml run --rm db mysql --user=root --password=$MYSQL_ROOT_PASSWORD --execute="CREATE SCHEMA mp_dev;"
docker compose -f docker-compose.dev.yml run --rm db mysql --user=root --password=$MYSQL_ROOT_PASSWORD --execute="CREATE SCHEMA mp_test;"
docker compose -f docker-compose.dev.yml run --rm db mysql --user=root --password=$MYSQL_ROOT_PASSWORD --database mp_dev --execute="GRANT ALL PRIVILEGES ON *.* TO '$MP_DB__USERNAME';"

echo "Migrating db"
docker exec --tty $(docker-compose -f docker-compose.dev.yml ps -q api) /bin/bash -c "cd /app/src && alembic upgrade head"

echo "Done"
