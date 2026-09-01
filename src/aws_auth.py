import logging

import boto3


logger = logging.getLogger(__name__)


def assume_role(
    session: boto3.Session,
    account_id: str,
    role_name: str
) -> boto3.Session:
    """Assume an IAM role and return a boto3 session using temporary credentials.

    Args:
        session: Authenticated boto3 session used to call AWS STS.
        account_id: AWS account ID containing the IAM role.
        role_name: Name of the IAM role to assume.

    Returns:
        A boto3 session authenticated with temporary credentials
        for the assumed IAM role.
    """

    logger.info("Starting IAM role assumption")

    sts = session.client("sts")

    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"

    response = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName="aws-account-inventory"
    )

    logger.info("IAM role assumed successfully")

    credentials = response["Credentials"]

    logger.debug("Creating boto3 session with temporary credentials")

    return boto3.Session(
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
        region_name=session.region_name
    )
