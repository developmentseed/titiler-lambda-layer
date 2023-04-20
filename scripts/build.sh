#!/bin/bash

PYTHON_VERSION=$1

# Base Image
docker build \
    --platform linux/amd64 \
    --build-arg PYTHON_VERSION=${PYTHON_VERSION} \
    -t devseed/titiler-layer:latest .
