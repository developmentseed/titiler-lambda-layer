ARG PYTHON_VERSION=3.12
FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}

ENV PREFIX /opt
RUN mkdir ${PREFIX}/python

RUN dnf install -y gcc-c++ && dnf clean all

RUN python -m pip install pip -U

COPY requirements.txt requirements.txt
RUN python -m pip install \
    -r requirements.txt \
    --no-binary pydantic \
    -t $PREFIX/python

ENV PYTHONPATH=$PYTHONPATH:$PREFIX/python
ENV PATH=$PREFIX/python/bin:$PATH

ENTRYPOINT bash
