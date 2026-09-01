import os
import logging


DEFAULT_PROFILE_NAME = "inventory"
DEFAULT_ROLE_NAME = "AWSInventoryReadOnly"
DEFAULT_REGION_NAME = "us-east-1"
DEFAULT_LOG_LEVEL = "INFO"

logger = logging.getLogger(__name__)


def get_log_level() -> str:
    """Return the configured application logging level."""

    log_level = os.getenv("AWS_INVENTORY_LOG_LEVEL", DEFAULT_LOG_LEVEL).upper()

    if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        return DEFAULT_LOG_LEVEL

    return log_level


def get_profile_name() -> str:
    """Return the AWS CLI profile used by the application."""

    return os.getenv("AWS_INVENTORY_PROFILE", DEFAULT_PROFILE_NAME)


def get_role_name() -> str:
    """Return the IAM role used by the application."""

    return os.getenv("AWS_INVENTORY_ROLE", DEFAULT_ROLE_NAME)


def get_region_name() -> str:
    """Return the AWS region used by the application."""

    return os.getenv("AWS_INVENTORY_REGION", DEFAULT_REGION_NAME)
