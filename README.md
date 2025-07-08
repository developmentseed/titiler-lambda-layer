# TiTiler AWS Lambda Layers

<a href="https://github.com/developmentseed/titiler-lambda-layer/actions?query=workflow%3ACI" target="_blank">
    <img src="https://github.com/developmentseed/titiler-lambda-layer/workflows/CI/badge.svg" alt="Test">
</a>

## Layers

| Layer Version  | TiTiler Version | Python Version |
|              --|               --|              --|
|             17 |          0.22.4 |           3.12 |

**Older version**

| Layer Version  | TiTiler Version | Python Version |
|              --|               --|              --|
|             15 |          0.19.1 |           3.11 |
|             14 |          0.18.5 |           3.11 |
|             13 |          0.18.1 |           3.11 |
|             12 |          0.17.3 |           3.11 |
|             11 |          0.15.6 |           3.11 |
|             10 |          0.15.0 |           3.11 |
|              9 |          0.15.0 |           3.10 |
|              8 |          0.14.0 |           3.10 |
|              7 |          0.13.3 |           3.10 |
|              6 |          0.13.1 |           3.10 |
|              5 |          0.13.0 |           3.10 |
|              4 |          0.12.0 |           3.10 |
|              3 |          0.11.6 |           3.10 |
|              2 |          0.11.6 |           3.10 |
|              1 |          0.11.6 |           3.10 |



#### Arns format

- `arn:aws:lambda:${region}:552819999234:layer:titiler:${version}`

#### Regions
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

## SAM application

<p><a href="https://console.aws.amazon.com/lambda/home?#/create/app?applicationId=arn:aws:serverlessrepo:us-east-1:552819999234:applications/TiTiler" rel="noreferrer"><img src="https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg" alt="Launch Stack"></a></p>

Link: https://serverlessrepo.aws.amazon.com/applications/us-east-1/552819999234/TiTiler

> **Note**
> You can change the `TiTiler` version by changing the Lambda Layer version `LayerVersion` parameter before deploying.

see: [SAM Application template](/sam.yml)
