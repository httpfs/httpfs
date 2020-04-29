#!/bin/bash

#sudo PATH="$PATH" bash -c 'python -m httpfs.client 127.0.0.1:8080 /mnt/httpfs/client --api-key b7615991121777b03088c03720d665ca'
#sudo PATH="$PATH" bash -c 'python -m httpfs.client 127.0.0.1:8080 /mnt/httpfs/client'
HOSTNAME=$(python -c 'import socket; print(socket.getfqdn())')
sudo PATH="$PATH" bash -c "python -m httpfs.client ${HOSTNAME}:8080 /mnt/httpfs/client --ca-file ca.crt --api-key 24a051469df2bb8579ad4416ec3cb9bd"
