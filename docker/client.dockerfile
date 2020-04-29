# vim: set ft=dockerfile:

FROM continuumio/miniconda3

ENV SERVER_HOST 127.0.0.1
ENV SERVER_PORT 8080
ENV MNT_DIR /mnt/httpfs

ADD . /httpfs
WORKDIR /httpfs

RUN apt-get update && \
    apt-get install fuse -y && \
    rm -rf /var/cache/apt/* /var/lib/apt/lists/*

RUN conda env update -n base -f environment.yml && \
    pip install -e .

VOLUME $MNT_DIR
ENTRYPOINT ["bash", "-lc", "python -m httpfs.client $SERVER_HOST:$SERVER_PORT $MNT_DIR"]
