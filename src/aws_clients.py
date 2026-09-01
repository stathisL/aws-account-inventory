import logging
import boto3

from botocore.client import BaseClient


logger = logging.getLogger(__name__)


def get_ec2_client(session: boto3.Session) -> BaseClient:
    """Return an EC2 client for the configured AWS region."""

    logger.debug("Creating EC2 client")

    return session.client("ec2")


def get_s3_client(session: boto3.Session) -> BaseClient:
    """Return an S3 client."""

    logger.debug("Creating S3 client")

    return session.client("s3")


def get_rds_client(session: boto3.Session) -> BaseClient:
    """Return an RDS client for the configured AWS region."""

    logger.debug("Creating RDS client")

    return session.client("rds")


def get_vpc_client(session: boto3.Session) -> BaseClient:
    """Return an EC2 client for VPC operations."""

    logger.debug("Creating VPC client")

    return session.client("ec2")
