#!/bin/bash

echo "Sourcing dev env from `pwd`/.env.dev"
source "`pwd`/.env.dev"

echo "Creating user $MP_DB__USERNAME in db mp_dev with pw $MYSQL_ROOT_PASSWORD"
docker exec --tty $(docker-compose -f docker-compose.dev.yml ps -q db) /bin/bash -c "mysql --user=root --password=$MYSQL_ROOT_PASSWORD --execute=\"CREATE USER '$MP_DB__USERNAME' IDENTIFIED BY '$MP_DB__PASSWORD'\""

echo "Creating db mp_dev"
docker exec --tty $(docker-compose -f docker-compose.dev.yml ps -q db) /bin/bash -c "mysql --user=root --password=$MYSQL_ROOT_PASSWORD --execute=\"CREATE SCHEMA mp_dev;\""
echo "Creating db mp_test"
docker exec --tty $(docker-compose -f docker-compose.dev.yml ps -q db) /bin/bash -c "mysql --user=root --password=$MYSQL_ROOT_PASSWORD --execute=\"CREATE SCHEMA mp_test;\""
echo "Creating db mp_matomo"
docker exec --tty $(docker-compose -f docker-compose.dev.yml ps -q db) /bin/bash -c "mysql --user=root --password=$MYSQL_ROOT_PASSWORD --execute=\"CREATE SCHEMA mp_matomo;\""
echo "Granting access to dbs to $MP_DB__USERNAME"
docker exec --tty $(docker-compose -f docker-compose.dev.yml ps -q db) /bin/bash -c "mysql --user=root --password=$MYSQL_ROOT_PASSWORD --database mp_dev --execute=\"GRANT ALL PRIVILEGES ON *.* TO '$MP_DB__USERNAME';\""
docker exec --tty $(docker-compose -f docker-compose.dev.yml ps -q db) /bin/bash -c "mysql --user=root --password=$MYSQL_ROOT_PASSWORD --database mp_test --execute=\"GRANT ALL PRIVILEGES ON *.* TO '$MP_DB__USERNAME';\""

echo "Migrating db"
docker exec --tty $(docker-compose -f docker-compose.dev.yml ps -q api) /bin/bash -c "cd /app/src && alembic upgrade head"

echo "Done"
