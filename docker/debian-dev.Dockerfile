ARG NAME=wildcatter
ARG TAG=dev
ARG PORT="8888"
ARG VIRTUAL_ENV=/opt/venv
ARG SOURCE_DIR=/opt/wildcatter

FROM python:3.9-slim-bullseye as builder
ARG VIRTUAL_ENV
ARG SOURCE_DIR
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update
RUN apt-get install -y  \
    swig \
    build-essential

RUN python -m venv $VIRTUAL_ENV
RUN pip -q install pip --upgrade
RUN pip install \
    numpy \
    matplotlib \
    jupyterlab

COPY . $SOURCE_DIR
RUN pip install --editable $SOURCE_DIR

FROM python:3.9-slim-bullseye
ARG PORT
ARG VIRTUAL_ENV
ARG SOURCE_DIR

ENV PORT=$PORT
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
COPY --from=builder $SOURCE_DIR $SOURCE_DIR

EXPOSE $PORT
ENTRYPOINT jupyter lab --port=$PORT --ip=0.0.0.0 --allow-root --no-browser
