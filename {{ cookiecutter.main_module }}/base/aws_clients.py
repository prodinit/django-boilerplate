from django.conf import settings

from .common_aws import get_boto_client


class S3Client:
    client = get_boto_client(
        "s3",
        settings.AWS_DEFAULT_REGION,
        settings.AWS_ACCESS_KEY_ID,
        settings.AWS_SECRET_ACCESS_KEY,
    )


class AthenaClient:
    client = get_boto_client(
        "athena",
        settings.AWS_DEFAULT_REGION,
        settings.AWS_ACCESS_KEY_ID,
        settings.AWS_SECRET_ACCESS_KEY,
    )
