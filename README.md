# httpfs
[![LINT](https://github.com/httpfs/httpfs/workflows/LINT/badge.svg?event=push)](https://github.com/httpfs/httpfs/actions?query=workflow%3ALINT)
[![TEST](https://github.com/httpfs/httpfs/workflows/TEST/badge.svg?event=push)](https://github.com/httpfs/httpfs/actions?query=workflow%3ATEST)

Network Filesystem over HTTP

# Table of Contents
1. [Contributing](./CONTRIBUTING.md)
2. [Code of Conduct](./CODE_OF_CONDUCT.md)
3. [License](./LICENSE)
4. [Design documentation](./docs/)

### Running the server using docker
See [docker-compose.yml](./docker-compose.yml) and the [docker directory](./docker/).
By default the server will run on 8080 and serve up /mnt/httpfs/server. Make sure
Docker and docker-compose are installed. The below commands download the HttpFs
docker-compose file and start the server.
```shell script
$ wget https://raw.githubusercontent.com/httpfs/httpfs/master/docker-compose.yml
$ docker-compose up httpfs-server
```

### Running the client using docker
See [docker-compose.yml](./docker-compose.yml) and the [docker directory](./docker/).
By default the client will attempt to connected to a server called 
httpfs-server on port 8080. Make sure Docker and docker-compose are installed.
The below commands download the HttpFs docker-compose file and start the client.
```shell script
$ wget https://raw.githubusercontent.com/httpfs/httpfs/master/docker-compose.yml
$ docker-compose up httpfs-client
```

### Running the server without docker
_Important Note:_ The `fuse` package must be installed for this to work

```shell script
$ conda env create -n httpfs_server -f environment.yml
$ conda activate httpfs_server
$ pip install -e .
# Generate an API key, see the next section
$ python -m httpfs.server server-port ~/httpfs-test/server
```
Where `server-port` is the port to run httpfs on, and `~/httpfs-test/server` is the directory to serve. See below for generating API keys and configuring TLS.

### Running the client without docker
As the root user
```shell script
$ conda env create -n httpfs_client -f environment.yml
$ conda activate httpfs_client
$ pip install -e .
# Configure API key(s), see the next section
$ python -m httpfs.client server-address:server-port ~/httpfs-test/client
```
Where `server-address` and `server-port` are a running HttpFS server's address and port and `~/httpfs-test/client` is the directory to mount the filesystem on to.
See below for generating API keys and configuring TLS.

### Generating API Keys
HttpFS clients require an API key in order to communicate with the server.
The keys can be generated as follows:

1. On the server, add a key to the keystore:
```shell script
$ ./bin/httpfs-cli add-api-key 192.168.1.96 test-user
192.168.1.96$test-user$4434aebd7e89b6900a49d4f0dcef706d6b6f287bd11f44b5943e984
b096909adbab431bfdf7cf91e5b98456a2e4a95ffcf3525fb2d8bb02e3eaaf976d706b687f6b1c
6ceb824f58d0a5eddfc12ced826863beced005f06c67782590ae41524eed91c3ff174c1c78a062
d4ab9d5b83d9aa8886fa5a875d6a76312937853b44afb69b26504193dc939d82056f7b4321f6cb
faa72063d46536a4ec3ae12bcfca89000771989a17291bb0f1c785e70c7d09cd37ca467866e23c
03d6814ce5c92b146020c60c3ab46deda939ae2f5a6e9df61fe1d1e557116b2b3ac0ec8037ec1f
02f846572eeebf18cafccd17bbacc09dd92a4ca530592f55f6953b9e56cfcc03712
```

2. The key above contains three fields: server, bearer (user), and api_key.
On the client, create config.yaml with the following contents:
```shell script
User: test-user
CredsFile: ./some-cred-file
```
And in `./some-cred-file` paste the output from step 1

3. Start the server and client, which should now be able to communicate with
each other

### Adding TLS Encryption
HttpFS provides a utility for create self-signed https certificates to encrypt
communication between and HttpFS client and server

1. Generate the certificates: `./bin/httpfs-cli gen-certs` will create `ca.key`,
`ca.crt`, `server.key`, and `server.crt` after prompting for some identifying
information:
```shell script
$ ./bin/httpfs-cli gen-certs
Country: US
State: AZ
City/Locality: Flagstaff
CA private key written to ca.key
CA certificate written to ca.crt
Server private key written to ca.key
Server certificate written to server.crt
```

2. Start the server with TLS:
```shell script
$ python -m httpfs.server 8080 /mnt/httpfs/server --tls-key server.key --tls-cert server.crt
```

3. Start the client, adding the generated CA as a trusted authority
```shell script
$ python -m httpfs.client 127.0.0.1:8080 /mnt/httpfs/client --ca-file ca.crt
```

---
Organization Icon: File Server by I Putu Kharismayadi from the Noun Project
