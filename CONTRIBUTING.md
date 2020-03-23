# Contributing
Welcome to HttpFs!

## Table of Contents
1. [Main README](./README.md)
2. [Docs](./docs/)
3. [Bugs](https://github.com/httpfs/httpfs/issues)
4. [Discord Chat](https://discord.gg/4eYv8Wg)

## Testing
Unit tests should be developed for each class and added to the [tests](./tests/)
directory.

## Installing the development environment
Make sure python3 and pip are installed

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html), make sure it's in your PATH
2. Create the project environment: `conda env create -f environment.yml`
3. Activate the project environment: `conda activate httpfs`

To update an the existing environment, run `conda env update` from the root of
this repository.

To add dependencies to the project, edit [environment.yml](./environment.yml)
and run `conda env update` from the root of this repository.

## Running the server for development
The client and server are packaged as executable python modules. The following
commands will run the server on port 8080
```shell script
$ conda activate httpfs
$ pip install -e .
$ python -m httpfs.server 8080
```

## Running the client for development
The following command will run the client, configured to talk to a server on
the same machine, port 8080, and a mountpoint of /mnt/other
```shell script
$ conda activate httpfs
$ pip install -e .
$ sudo -E PATH="$PATH" bash -c 'python -m httpfs.client 127.0.0.1:8080 /mnt/other'
```

## Using Docker for development
This will run both the server and client on the docker host. It will mount
/mnt/httpfs/client as the client's mount directory and /mnt/httpfs/server
as the server's exported directory. Any changes made to either directory
on the host should be mirrored within the other. Good for testing/development.
**Currently this compose file has only been tested on Linux**.
```shell script
$ docker-compose -f docker-compose-dev.yml up
```

## Submitting changes
To submit changes, open a pull request to the master branch of [HttpFs](https://github.com/httpfs/httpfs)

## Bug Reporting
Submit the following template as a [GitHub issue](https://github.com/httpfs/httpfs/issues)
```
Problem Description:

Steps to Reproduce:

Proposed Changes:
```

## HttFs API Format
 
#### Request Schema
```json
{
  "$id": "https://raw.githubusercontent.com/httpfs/httpfs/master/HttpFsResponse.schema.json",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "HttpFsRequest",
  "type": "object",
  "properties": {
    "type": {
      "type": "integer",
      "description": "The type of filesystem operation being executed"
    },
    "args": {
      "type": "object",
      "description": "Key-value arguments corresponding to operation type"
    },
    "auth": {
      "type": "string",
      "description": "API key for authentication with the server"
    }
  }
}
```

Example (type zero is [HttpFsOp.OP_ACCESS](httpfs/common/HttpFsRequest.py), Mode 448 is "rwx------"):
```json
{
  "type": 0,
  "auth": "1941a3af-8256-4e63-a5c0-2d88782b7e2c",
  "args": {
    "path": "/path/to/some/file",
    "mode": 448
  }
}
```

#### Response Schema
```json
{
  "$id": "https://raw.githubusercontent.com/httpfs/httpfs/master/HttpFsResponse.schema.json",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "HttpFsResponse",
  "type": "object",
  "properties": {
    "error_no": {
      "type": "integer",
      "description": "0 on success, a system error code on failure (see https://python.readthedocs.io/en/latest/library/errno.html)"
    },
    "response_data": {
      "type": "object",
      "description": "The return value from the command, or error message if any"
    }
  }
}
```

Example Response (success):
```json
{
  "error_no": 0,
  "response_data": {}
}
```
```json
{
  "error_no": 5,
  "response_data": {
    "message": "Input/output error"
  }
}
```

