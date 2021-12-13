#!/bin/sh

set -e

host="$1"
shift

until mysql --user=$MYSQL_USER --password=$MYSQL_PASSWORD --database=$MYSQL_DATABASE --host=$MYSQL_HOST --execute="show databases;"; do
  >&2 echo "db is unavailable - sleeping"
  sleep 1
done

>&2 echo "db is up - executing command"
exec "$@"