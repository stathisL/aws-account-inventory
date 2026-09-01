import logging

import boto3

from src.aws_clients import (
    get_ec2_client,
    get_rds_client,
    get_s3_client,
    get_vpc_client
)
from .data_transformations import (
    transform_ec2_response,
    transform_s3_response,
    transform_rds_response,
    transform_vpc_response
)
from .custom_types import InventoryResult


logger = logging.getLogger(__name__)


def collect_ec2_inventory(session: boto3.Session) -> InventoryResult:
    """Collect EC2 instance information from the configured AWS region."""

    logger.debug("Requesting EC2 instance inventory")

    ec2 = get_ec2_client(session)
    response = ec2.describe_instances()

    logger.info("EC2 inventory retrieved successfully")

    return {
        "service": "EC2",
        "resources": transform_ec2_response(response)
    }


def collect_s3_inventory(session: boto3.Session) -> InventoryResult:
    """Collect S3 bucket information for the AWS account."""

    logger.debug("Requesting S3 bucket inventory")

    s3 = get_s3_client(session)
    response = s3.list_buckets()

    logger.info("S3 inventory retrieved successfully")

    return {
        "service": "S3",
        "resources": transform_s3_response(response)
    }


def collect_rds_inventory(session: boto3.Session) -> InventoryResult:
    """Collect RDS DB instance information from the configured AWS region."""

    logger.debug("Requesting RDS instance inventory")

    rds = get_rds_client(session)
    response = rds.describe_db_instances()

    logger.info("RDS inventory retrieved successfully")

    return {
        "service": "RDS",
        "resources": transform_rds_response(response)
    }


def collect_vpc_inventory(session: boto3.Session) -> InventoryResult:
    """Collect VPC information from the configured AWS region."""

    logger.debug("Requesting VPC inventory")

    ec2 = get_vpc_client(session)
    response = ec2.describe_vpcs()

    logger.info("VPC inventory retrieved successfully")

    return {
        "service": "VPC",
        "resources": transform_vpc_response(response)
    }
