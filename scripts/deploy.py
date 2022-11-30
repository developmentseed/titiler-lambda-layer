

import os
import click

import docker

from boto3.session import Session as boto3_session
from botocore.client import Config

AWS_REGIONS = [
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-south-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ca-central-1",
    "eu-central-1",
    "eu-north-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
]


@click.command()
@click.argument('runtime', type=str)
@click.argument('version', type=str)
@click.option('--deploy', is_flag=True)
def main(runtime, version, deploy):
    """Build and Deploy Layers."""
    client = docker.from_env()

    docker_name = f"lambgeo/titiler-py{runtime}:{version}"
    click.echo(f"Building image: {docker_name}...")
    client.images.build(
        path="./",
        platform="linux/amd64",
        dockerfile="Dockerfile",
        tag=docker_name,
        buildargs={
            "PYTHON_VERSION": runtime,
            "TITILER_VERSION": version,
        },
        rm=True,
    )

    click.echo("Create Package")
    client.containers.run(
        platform="linux/amd64",
        image=docker_name,
        command="/local/scripts/create-lambda-layer.sh",
        entrypoint="bash",
        remove=True,
        volumes={os.path.abspath("./"): {"bind": "/local/", "mode": "rw"}},
        user=0,
    )

    version_nodot = version.replace(".", "")
    description = f"TiTiler Lambda Layer ({version})"

    if deploy:
        session = boto3_session()

        # Increase connection timeout to work around timeout errors
        config = Config(connect_timeout=6000, retries={'max_attempts': 5})

        click.echo(f"Deploying titiler layer", err=True)
        for region in AWS_REGIONS:
            click.echo(f"AWS Region: {region}", err=True)
            client = session.client("lambda", region_name=region, config=config)

            # upload the package to s3
            s3 = session.client("s3", region_name=region)

            try:
                s3.head_bucket(Bucket=f"lambgeo-{region}")
            except client.exceptions.ClientError:
                ops = {}
                if region != "us-east-1":
                    ops["CreateBucketConfiguration"] = {
                        "LocationConstraint": region
                    }

                s3.create_bucket(Bucket=f"lambgeo-{region}", **ops)

            with open("package.zip", "rb") as data:
                s3.upload_fileobj(
                    data,
                    f"lambgeo-{region}",
                    f"layers/titiler{version_nodot}.zip",
                )

            click.echo("Publishing new version", err=True)
            res = client.publish_layer_version(
                LayerName=layer_name,
                Content={
                    "S3Bucket": f"lambgeo-{region}",
                    "S3Key": f"layers/titiler{version_nodot}.zip",
                },
                CompatibleRuntimes=[f"python{runtime}"],
                Description=description,
                LicenseInfo="MIT"
            )

            click.echo("Adding permission", err=True)
            client.add_layer_version_permission(
                LayerName=layer_name,
                VersionNumber=res["Version"],
                StatementId='make_public',
                Action='lambda:GetLayerVersion',
                Principal='*',
            )


def head_bucket(name, client):
    try:
        return client.head_bucket(Bucket=name)
    except client.exceptions.ClientError:
        return False


if __name__ == '__main__':
    main()
