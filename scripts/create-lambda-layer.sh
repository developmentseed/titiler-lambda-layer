#!/bin/bash
echo "-----------------------"
echo "Creating lambda layer"
echo "-----------------------"

yum makecache fast
yum install -y zip binutils

echo "Remove lambda python packages"
rm -rdf $PREFIX/python/boto3* \
&& rm -rdf $PREFIX/python/botocore* \
&& rm -rdf $PREFIX/python/docutils* \
&& rm -rdf $PREFIX/python/dateutil* \
&& rm -rdf $PREFIX/python/jmespath* \
&& rm -rdf $PREFIX/python/s3transfer* \
&& rm -rdf $PREFIX/python/numpy/doc/

find $PREFIX/python -type d -a -name 'tests' -print0 | xargs -0 rm -rf

echo "Remove uncompiled python scripts"
find $PREFIX/python -type f -name '*.pyc' | while read f; do n=$(echo $f | sed 's/__pycache__\///' | sed 's/.cpython-[0-9]*//'); cp $f $n; done;
find $PREFIX/python -type d -a -name '__pycache__' -print0 | xargs -0 rm -rf
find $PREFIX/python -type f -a -name '*.py' -print0 | xargs -0 rm -f

echo "Create archives"
cd $PREFIX && zip -r9q /tmp/package.zip python

cp /tmp/package.zip /local/package.zip
