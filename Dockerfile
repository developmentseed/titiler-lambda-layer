ARG PYTHON_VERSION=3.9
FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}

ARG TITILER_VERSION=0.7.1

RUN pip install \
    titiler.core==${TITILER_VERSION} \
    titiler.mosaic==${TITILER_VERSION} \
    titiler.application==${TITILER_VERSION} \
    requests \
    pyyaml \
    jinja2 \
    --no-binary pydantic -t $PREFIX/python

COPY handler.py $PREFIX/python/titiler/application/handler.py
RUN python3 -m py_compile $PREFIX/python/titiler/application/handler.py

ENV PYTHONPATH=$PYTHONPATH:$PREFIX/python
ENV PATH=$PREFIX/python/bin:$PATH

CMD ["echo", "hello world"]
