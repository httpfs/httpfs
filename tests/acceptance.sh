#!/bin/bash
set -e

SERVER_DIR=/tmp/httpfs/server
CLIENT_DIR=/tmp/httpfs/client
ENV_DIR=./.env

mkdir -p $SERVER_DIR $CLIENT_DIR

if [ -d $ENV_DIR ]; then
  rm -rf $ENV_DIR
fi

# Create environment
echo "Creating environment..."
conda env create --prefix $ENV_DIR -f environment.yml > /dev/null 2>&1
export PATH="$ENV_DIR/bin:$PATH"
pip install -e .

# Run server
python -m httpfs.server 8080 /tmp/httpfs/server > /dev/null 2>&1 &
SERVER_PID="$!"

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
