# httpfs

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
$ wget https://raw.githubusercontent.com/httpfs/httpfs/httpfs/docker-compose.yml
$ docker-compose up httpfs-server
```

### Running the client using docker
See [docker-compose.yml](./docker-compose.yml) and the [docker directory](./docker/).
By default the client will attempt to connected to a server called 
httpfs-server on port 8080. Make sure Docker and docker-compose are installed.
The below commands download the HttpFs docker-compose file and start the client.
```shell script
$ wget https://raw.githubusercontent.com/httpfs/httpfs/httpfs/docker-compose.yml
$ docker-compose up httpfs-client
```

---
Organization Icon: File Server by I Putu Kharismayadi from the Noun Project
