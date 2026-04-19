#!/bin/bash
set -e
mkdir -p bin
echo "Downloading database migration tool..."
curl -fsSL \
    https://github.com/pressly/goose/releases/download/v3.15.0/goose_linux_x86_64 \
    -o bin/goose
chmod +x bin/goose
echo "Running migrations..."
./bin/goose sqlite3 instance/taskmanager.db up
