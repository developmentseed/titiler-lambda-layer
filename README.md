# TiTiler Lambda Layers

<p align="center">
  <em>TiTiler Layers.</em>
</p>
<p align="center">
  <a href="https://github.com/lambgeo/titiler-layer/actions?query=workflow%3ACI" target="_blank">
      <img src="https://github.com/lambgeo/titiler-layer/workflows/CI/badge.svg" alt="Test">
  </a>
</p>

## Python package

```
numpy
pygeos>=0.9,<0.10
rasterio~=1.2
titiler{core/mosaic/application}==0.3.1

# those package are in the docker image but not in the lambda env
requests
pyyaml
jinja2
```

### Arns format

- `arn:aws:lambda:${region}:524387336408:layer:titiler-gdal33:${version}`
- `arn:aws:lambda:${region}:524387336408:layer:titiler-gdal32:${version}` **archived**
- `arn:aws:lambda:${region}:524387336408:layer:titiler-gdal24:${version}`

### Regions
- ap-northeast-1
- ap-northeast-2
- ap-south-1
- ap-southeast-1
- ap-southeast-2
- ca-central-1
- eu-central-1
- eu-north-1
- eu-west-1
- eu-west-2
- eu-west-3
- sa-east-1
- us-east-1
- us-east-2
- us-west-1
- us-west-2

See [full list of ARN](/arns.json)

### Layer content

```
layer.zip
  |
  |___ lib/      # Shared libraries (GDAL, PROJ, GEOS...)
  |___ share/    # GDAL/PROJ data directories
  |___ python/   # Python modules
```

The layer content will be unzip in `/opt` directory in AWS Lambda. For the python libs to be able to use the C libraries you have to make sure to set 2 important environment variables:

- **GDAL_DATA:** /opt/share/gdal
- **PROJ_LIB:** /opt/share/proj
