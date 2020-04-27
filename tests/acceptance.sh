#!/bin/bash
set -e

SERVER_DIR=/tmp/httpfs/server
CLIENT_DIR=/tmp/httpfs/client
ENV_DIR=./.env

mkdir -p $SERVER_DIR $CLIENT_DIR

# Create environment
echo "Creating environment..."
conda env create --prefix ./.env -f environment.yml > /dev/null 2>&1
export PATH="$ENV_DIR/bin:$PATH"
pip install -e .

# Run server
python -m httpfs.server 8080 /tmp/httpfs/server > /dev/null 2>&1 &
SERVER_PID="$!"

# Add API key for server
./bin/httpfs-cli add-api-key $(hostname) test-user > ./client-creds

# Add API key for client
cat << EOF >> config.yaml
User: test-user
CredFile: ./client-creds
EOF

# Run client
python -m httpfs.client $(hostname):8080 /tmp/httpfs/client > /dev/null 2>&1 &
CLIENT_PID="$!"
sleep 1

# Write file
dd status=progress if=/dev/zero of=$CLIENT_DIR/test-file bs=1K count=5120

# Kill client/server
kill -9 $SERVER_PID > /dev/null 2>&1
kill -9 $CLIENT_PID > /dev/null 2>&1
umount $CLIENT_DIR > /dev/null 2>&1
sleep 3 > /dev/null 2>&1

# Clean up
rm -rf /tmp/httpfs
rm -rf ./.env
rm -f creds client-creds config.yaml
