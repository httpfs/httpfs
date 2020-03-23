# vim: set ft=dockerfile:

FROM continuumio/miniconda3

ENV PORT 8080
ENV SRV_DIR /srv/httpfs

ADD . /httpfs
WORKDIR /httpfs

RUN conda env update -n base -f environment.yml && \
    pip install -e .

EXPOSE $PORT
VOLUME $SRV_DIR
CMD ["bash", "-lc", "python -m httpfs.server $PORT $SRV_DIR"]
