ARG VERSION
ARG RUNTIME

FROM lambgeo/lambda-gdal:${VERSION}-${RUNTIME}

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-binary numpy,rasterio,pygeos,pydantic -t $PREFIX/python
RUN rm requirements.txt

COPY handler.py $PREFIX/python/titiler/application/handler.py
RUN python3 -m py_compile $PREFIX/python/titiler/application/handler.py

ENV PYTHONPATH=$PYTHONPATH:$PREFIX/python
ENV PATH=$PREFIX/python/bin:$PATH
