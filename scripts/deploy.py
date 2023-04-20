

import os
import click

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
@click.option('--deploy', is_flag=True)
def main(runtime, deploy):
    """Build and Deploy Layers."""
    description = "TiTiler Lambda Layer"

    if deploy:
        session = boto3_session()

        # Increase connection timeout to work around timeout errors
        config = Config(connect_timeout=6000, retries={'max_attempts': 5})

        click.echo(f"Deploying titiler layer", err=True)
        for region in AWS_REGIONS:
            click.echo(f"AWS Region: {region}", err=True)
            client = session.client("lambda", region_name=region, config=config)

            with open("package.zip", "rb") as package:
                click.echo("Publishing new version", err=True)
                res = client.publish_layer_version(
                    LayerName="titiler",
                    Content={
                        "ZipFile": package.read(),
                    },
                    CompatibleRuntimes=[f"python{runtime}"],
                    Description=description,
                    LicenseInfo="MIT"
                )

            click.echo("Adding permission", err=True)
            client.add_layer_version_permission(
                LayerName="titiler",
                VersionNumber=res["Version"],
                StatementId='make_public',
                Action='lambda:GetLayerVersion',
                Principal='*',
            )


if __name__ == '__main__':
    main()
