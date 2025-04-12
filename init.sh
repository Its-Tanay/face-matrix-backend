#!/bin/bash
set -e

# Start the DB in the background so we can run commands
docker-entrypoint.sh postgres &

# Wait for the server to start
until pg_isready -U "$POSTGRES_USER"; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

# Enable the vector extension
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Bring foreground process back
wait
