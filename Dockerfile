ARG PYTHON_VERSION
FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}

ARG TITILER_VERSION

ENV PREFIX /opt
RUN mkdir ${PREFIX}/python

ENV \
  LANG=en_US.UTF-8 \
  LC_ALL=en_US.UTF-8

RUN yum update -y

RUN pip install pip -U

RUN pip install \
    titiler.core==${TITILER_VERSION} \
    titiler.extensions["stac,cogeo"]==${TITILER_VERSION} \
    titiler.mosaic==${TITILER_VERSION} \
    titiler.application==${TITILER_VERSION} \
    mangum \
    requests \
    pyyaml \
    jinja2 \
    --no-binary pydantic \
    -t $PREFIX/python

ENV PYTHONPATH=$PYTHONPATH:$PREFIX/python
ENV PATH=$PREFIX/python/bin:$PATH

ENTRYPOINT bash
