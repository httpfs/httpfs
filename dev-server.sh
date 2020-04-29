#!/bin/bash

#sudo PATH="$PATH" bash -c 'python -m httpfs.server 8080 /mnt/httpfs/server/ --cred-store test-creds.json'
#sudo PATH="$PATH" bash -c 'python -m httpfs.server 8080 /mnt/httpfs/server/'
sudo PATH="$PATH" bash -c 'python -m httpfs.server 8080 /mnt/httpfs/server/ --tls-key server.key --tls-cert server.crt'
