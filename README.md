# TiTiler Lambda Layers

<a href="https://github.com/lambgeo/titiler-layer/actions?query=workflow%3ACI" target="_blank">
    <img src="https://github.com/lambgeo/titiler-layer/workflows/CI/badge.svg" alt="Test">
</a>

### TiTiler Version

| TiTiler Version | Layer Version |
|               --|             --|
|           0.7.1 |             2 |
|           0.8.1 |             3 |

### Arns format

- `arn:aws:lambda:${region}:524387336408:layer:titiler:${version}`

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


### SAM application

<p><a href="https://console.aws.amazon.com/lambda/home?#/create/app?applicationId=arn:aws:serverlessrepo:us-east-1:552819999234:applications/TiTiler" rel="noreferrer"><img src="https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg" alt="Launch Stack"></a></p>

Link: https://serverlessrepo.aws.amazon.com/applications/us-east-1/552819999234/TiTiler

> **Note**
> You can change the TiTiler version by changing the Lambda Layer version `LambdaLayerVersion` parameter before deploying.

SAM Application template
```yml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Parameters:
  Bucket:
    Type: CommaDelimitedList
    Default: "*"

  DisableCOG:
    Type: String
    Default: "false"
    AllowedValues:
      - "true"
      - "false"

  DisableMosaic:
    Type: String
    Default: "true"
    AllowedValues:
      - "true"
      - "false"

  DisableSTAC:
    Type: String
    Default: "true"
    AllowedValues:
      - "true"
      - "false"

  LambdaLayerVersion:
    Type: String
    Default: 3

Resources:
  TiTiler:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.9
      Handler: index.handler
      Description: 'Titiler: Dynamic tiler'
      Layers:
        - !Sub arn:aws:lambda:${AWS::Region}:524387336408:layer:titiler:${LambdaLayerVersion}

      InlineCode: |
        import logging
        from mangum import Mangum
        from titiler.application.main import app

        logging.getLogger("mangum.lifespan").setLevel(logging.ERROR)
        logging.getLogger("mangum.http").setLevel(logging.ERROR)

        handler = Mangum(app, lifespan="auto")

      MemorySize: 1024
      Timeout: 10
      Policies:
        - AWSLambdaExecute # Managed Policy
        - Version: '2012-10-17' # Policy Document
          Statement:
            - Effect: Allow
              Action:
                - s3:GetObject
                - s3:HeadObject
              Resource:
                !Split
                  - ','
                  - !Join
                      - ''
                      - - 'arn:aws:s3:::'
                        - !Join
                            - '/*,arn:aws:s3:::'
                            - !Ref Bucket
                        - '/*'

      Environment:
        Variables:
          CPL_VSIL_CURL_ALLOWED_EXTENSIONS: '.tif,.TIF,.tiff'
          GDAL_CACHEMAX: 200
          GDAL_DISABLE_READDIR_ON_OPEN: EMPTY_DIR
          GDAL_HTTP_MERGE_CONSECUTIVE_RANGES: YES
          GDAL_HTTP_MULTIPLEX: YES
          GDAL_HTTP_VERSION: 2
          VSI_CACHE: TRUE
          VSI_CACHE_SIZE: 536870912
          CPL_VSIL_CURL_CACHE_SIZE: 200000000
          GDAL_INGESTED_BYTES_AT_OPEN: 32768
          TITILER_API_DISABLE_COG: !Ref DisableCOG
          TITILER_API_DISABLE_STAC: !Ref DisableSTAC
          TITILER_API_DISABLE_MOSAIC: !Ref DisableMosaic

      Events:
        API:
          Type: HttpApi

Outputs:
  LambdaFunc:
    Description: Lambda Fucntion ARN
    Value: !GetAtt TiTiler.Arn

  Api:
    Description: "Endpoint URL"
    Value: !Sub "https://${ServerlessHttpApi}.execute-api.${AWS::Region}.amazonaws.com/"
```
