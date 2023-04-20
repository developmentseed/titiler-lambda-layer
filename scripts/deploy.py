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
@click.argument("runtime", type=str)
@click.argument("version", type=str)
def main(runtime, version):
    """Build and Deploy Layers."""
    version_nodot = version.replace(".", "")

    session = boto3_session()

    click.echo("Deploying titiler layer", err=True)
    for region in AWS_REGIONS:
        click.echo(f"AWS Region: {region}", err=True)


        # upload the package to s3
        s3_client = session.client("s3", region_name=region)

        s3_bucket = f"titiler-layers-{region}"
        s3_key = f"titiler{version_nodot}.zip"

        click.echo(f"Uploading package to S3 s3://{s3_bucket}/{s3_key}", err=True)

        try:
            s3_client.head_bucket(Bucket=s3_bucket)
        except s3_client.exceptions.ClientError:
            ops = {}
            if region != "us-east-1":
                ops["CreateBucketConfiguration"] = {"LocationConstraint": region}

            s3_client.create_bucket(Bucket=s3_bucket, **ops)

        with open("package.zip", "rb") as data:
            s3_client.upload_fileobj(data, s3_bucket, s3_key)

        click.echo("Publishing new version", err=True)

        # Increase connection timeout to work around timeout errors
        config = Config(connect_timeout=6000, retries={"max_attempts": 5})
        lambda_client = session.client("lambda", region_name=region, config=config)

        res = lambda_client.publish_layer_version(
            LayerName="titiler",
            Content={"S3Bucket": s3_bucket, "S3Key": s3_key},
            CompatibleRuntimes=[f"python{runtime}"],
            Description=f"TiTiler Lambda Layer ({version})",
            LicenseInfo="MIT",
        )

        click.echo("Adding permission", err=True)
        lambda_client.add_layer_version_permission(
            LayerName="titiler",
            VersionNumber=res["Version"],
            StatementId="make_public",
            Action="lambda:GetLayerVersion",
            Principal="*",
        )


if __name__ == "__main__":
    main()
