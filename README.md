# TiTiler Lambda Layers

<a href="https://github.com/lambgeo/titiler-layer/actions?query=workflow%3ACI" target="_blank">
    <img src="https://github.com/lambgeo/titiler-layer/workflows/CI/badge.svg" alt="Test">
</a>

### TiTiler Version

| TiTiler Version | Layer Version |
|               --|             --|
|           0.7.1 |             2 |
|           0.8.1 |             3 |
|          0.10.2 |             4 |

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

see: [SAM Application template](/sam.yml)
