"""Storage utilities for OWASP app."""

from django.conf import settings
from django.core.files.storage import default_storage


def get_evidence_storage():
    """Return custom storage for evidence if EVIDENCE_S3_BUCKET is configured.

    Falls back to the default storage (local memory/filesystem).
    """
    bucket_name = getattr(settings, "EVIDENCE_S3_BUCKET", None)
    if bucket_name:
        from storages.backends.s3boto3 import S3Boto3Storage  # noqa: PLC0415

        return S3Boto3Storage(bucket_name=bucket_name)
    return default_storage
