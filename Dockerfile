ARG PYTHON_VERSION
FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}

ENV PREFIX /opt
RUN mkdir ${PREFIX}/python

ENV \
  LANG=en_US.UTF-8 \
  LC_ALL=en_US.UTF-8

RUN yum update -y

RUN python -m pip install pip -U

COPY requirements.txt requirements.txt
RUN python -m pip install \
    -r requirements.txt \
    --no-binary pydantic \
    -t $PREFIX/python

ENV PYTHONPATH=$PYTHONPATH:$PREFIX/python
ENV PATH=$PREFIX/python/bin:$PATH

ENTRYPOINT bash
