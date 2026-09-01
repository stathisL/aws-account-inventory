from datetime import datetime
from unittest.mock import MagicMock

from botocore.exceptions import ClientError

from src.aws_collectors import (
    collect_ec2_inventory,
    collect_s3_inventory,
    collect_rds_inventory,
    collect_vpc_inventory
)


def make_client_error(error_code: str, message: str) -> ClientError:
    """Create a simulated AWS ClientError for testing."""

    return ClientError(
        {
            "Error": {
                "Code": error_code,
                "Message": message,
            }
        },
        "test_operation"
    )


def test_collect_ec2_inventory():
    session = MagicMock()
    ec2 = session.client.return_value

    ec2.describe_instances.return_value = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-1234567890",
                        "InstanceType": "t3.micro",
                        "State": {"Name": "running"},
                        "Placement": {
                            "AvailabilityZone": "us-east-1a"
                        }
                    }
                ]
            }
        ]
    }

    result = collect_ec2_inventory(session)

    assert result == {
        "service": "EC2",
        "resources": [
            {
                "id": "i-1234567890",
                "type": "t3.micro",
                "state": "running",
                "availability_zone": "us-east-1a"
            }
        ]
    }

    ec2.describe_instances.assert_called_once_with()


def test_collect_s3_inventory():
    session = MagicMock()
    s3 = session.client.return_value

    s3.list_buckets.return_value = {
        "Buckets": [
            {
                "Name": "example-bucket",
                "CreationDate": datetime(2026, 1, 1)
            }
        ]
    }

    result = collect_s3_inventory(session)

    assert result == {
        "service": "S3",
        "resources": [
            {
                "id": "example-bucket",
                "created": "2026-01-01T00:00:00"
            }
        ]
    }

    s3.list_buckets.assert_called_once_with()


def test_collect_rds_inventory():
    session = MagicMock()
    rds = session.client.return_value

    rds.describe_db_instances.return_value = {
        "DBInstances": [
            {
                "DBInstanceIdentifier": "example-db",
                "Engine": "postgres",
                "DBInstanceStatus": "available",
                "DBInstanceClass": "db.t3.micro",
                "AvailabilityZone": "us-east-1a"
            }
        ]
    }

    result = collect_rds_inventory(session)

    assert result == {
        "service": "RDS",
        "resources": [
            {
                "id": "example-db",
                "engine": "postgres",
                "status": "available",
                "instance_class": "db.t3.micro",
                "availability_zone": "us-east-1a"
            }
        ]
    }

    rds.describe_db_instances.assert_called_once_with()


def test_collect_vpc_inventory():
    session = MagicMock()
    ec2 = session.client.return_value

    ec2.describe_vpcs.return_value = {
        "Vpcs": [
            {
                "VpcId": "vpc-1234567890",
                "CidrBlock": "10.0.0.0/16",
                "State": "available",
                "IsDefault": True
            }
        ]
    }

    result = collect_vpc_inventory(session)

    assert result == {
        "service": "VPC",
        "resources": [
            {
                "id": "vpc-1234567890",
                "cidr_block": "10.0.0.0/16",
                "state": "available",
                "is_default": True
            }
        ]
    }

    ec2.describe_vpcs.assert_called_once_with()


def test_collect_ec2_inventory_empty_response():
    session = MagicMock()
    ec2 = session.client.return_value

    ec2.describe_instances.return_value = {
        "Reservations": []
    }

    result = collect_ec2_inventory(session)

    assert result == {
        "service": "EC2",
        "resources": []
    }


def test_collect_s3_inventory_empty_response():
    session = MagicMock()
    s3 = session.client.return_value

    s3.list_buckets.return_value = {
        "Buckets": []
    }

    result = collect_s3_inventory(session)

    assert result == {
        "service": "S3",
        "resources": []
    }


def test_collect_rds_inventory_empty_response():
    session = MagicMock()
    rds = session.client.return_value

    rds.describe_db_instances.return_value = {
        "DBInstances": []
    }

    result = collect_rds_inventory(session)

    assert result == {
        "service": "RDS",
        "resources": []
    }


def test_collect_vpc_inventory_empty_response():
    session = MagicMock()
    ec2 = session.client.return_value

    ec2.describe_vpcs.return_value = {
        "Vpcs": []
    }

    result = collect_vpc_inventory(session)

    assert result == {
        "service": "VPC",
        "resources": []
    }


def test_collect_ec2_inventory_api_error():
    session = MagicMock()
    ec2 = session.client.return_value

    ec2.describe_instances.side_effect = make_client_error(
        "InternalError",
        "AWS service error"
    )

    try:
        collect_ec2_inventory(session)
    except ClientError as error:
        assert error.response["Error"]["Code"] == "InternalError"
    else:
        raise AssertionError("Expected ClientError")


def test_collect_s3_inventory_access_denied():
    session = MagicMock()
    s3 = session.client.return_value

    s3.list_buckets.side_effect = make_client_error(
        "AccessDenied",
        "User is not authorized to perform this operation"
    )

    try:
        collect_s3_inventory(session)
    except ClientError as error:
        assert error.response["Error"]["Code"] == "AccessDenied"
    else:
        raise AssertionError("Expected ClientError")
