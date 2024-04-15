#!/bin/bash

set -e
echo "TEST@@@!!!"


# Load environment variables from the .env file
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

# Check that all required environment variables are set
if [ -z "$POSTGRES_PASSWORD" ] || [ -z "$POSTGRES_DB" ] || [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PORT" ]; then
  echo "Some required environment variables are not set. Exiting..."
  exit 1
fi

# Check connection and if ok continue if not try after 1 sec
until PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -p "$POSTGRES_PORT" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up -executing command"


if [ "$ENV_TYPE" = "dev" ]; then
  exec uvicorn main:app --reload --host 0.0.0.0
else
  exec uvicorn main:app --host 0.0.0.0
fi

