#!/bin/bash

PYTHON_VERSION=$1
TITILER_VERSION=$2

# Base Image
docker build \
    --platform linux/amd64 \
    --build-arg PYTHON_VERSION=${PYTHON_VERSION} \
    --build-arg TITILER_VERSION=${TITILER_VERSION} \
    -t lambgeo/titiler:${TITILER_VERSION} .
