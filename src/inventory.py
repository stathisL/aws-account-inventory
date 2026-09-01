import boto3
import logging

from botocore.exceptions import ClientError

from src.aws_auth import assume_role
from .aws_collectors import (
    collect_ec2_inventory,
    collect_s3_inventory,
    collect_rds_inventory,
    collect_vpc_inventory
)
from src.config import (
    get_profile_name,
    get_role_name,
    get_region_name,
    get_log_level
)
from src.presentation import print_inventory

logger = logging.getLogger(__name__)


class InventoryError(Exception):
    """Base exception for AWS inventory errors."""


def handle_aws_error(error: ClientError) -> InventoryError:
    """Convert an AWS ClientError into an application-level error."""

    error_code = error.response["Error"]["Code"]
    error_message = error.response["Error"]["Message"]

    if error_code in {"AccessDenied", "UnauthorizedOperation"}:
        return InventoryError(
            f"AWS permission error ({error_code}): {error_message}"
        )

    return InventoryError(
        f"AWS error ({error_code}): {error_message}"
    )


def main() -> None:
    """Run the AWS account inventory application."""

    logging.basicConfig(
        level=get_log_level(),
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    logger.info("Starting AWS account inventory")

    try:
        profile_name = get_profile_name()
        role_name = get_role_name()
        region_name = get_region_name()

        source_session = boto3.Session(
            profile_name=profile_name,
            region_name=region_name
        )

        source_sts = source_session.client("sts")
        source_identity = source_sts.get_caller_identity()

        read_only_session = assume_role(
            session=source_session,
            account_id=source_identity["Account"],
            role_name=role_name
        )

        ec2_inventory = collect_ec2_inventory(read_only_session)
        s3_inventory = collect_s3_inventory(read_only_session)
        rds_inventory = collect_rds_inventory(read_only_session)
        vpc_inventory = collect_vpc_inventory(read_only_session)

        inventory = [
            ec2_inventory,
            s3_inventory,
            rds_inventory,
            vpc_inventory
        ]

        print_inventory(inventory)

        logger.info("AWS account inventory application finished")
    except ClientError as error:
        raise handle_aws_error(error) from error


if __name__ == "__main__":
    main()
