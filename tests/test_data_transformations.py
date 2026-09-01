from datetime import datetime

from src.data_transformations import (
    transform_ec2_response,
    transform_s3_response,
    transform_rds_response,
    transform_vpc_response
)


def test_transform_ec2_response():
    response = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-1234567890",
                        "InstanceType": "t3.micro",
                        "State": {
                            "Name": "running"
                        },
                        "Placement": {
                            "AvailabilityZone": "us-east-1a"
                        }
                    }
                ]
            }
        ]
    }

    result = transform_ec2_response(response)

    assert result == [
        {
            "id": "i-1234567890",
            "type": "t3.micro",
            "state": "running",
            "availability_zone": "us-east-1a"
        }
    ]


def test_transform_ec2_response_empty():
    response = {
        "Reservations": []
    }

    result = transform_ec2_response(response)

    assert result == []


def test_transform_s3_response():
    creation_date = datetime(2026, 8, 28, 12, 30, 0)

    response = {
        "Buckets": [
            {
                "Name": "example-bucket",
                "CreationDate": creation_date
            }
        ]
    }

    result = transform_s3_response(response)

    assert result == [
        {
            "id": "example-bucket",
            "created": "2026-08-28T12:30:00"
        }
    ]


def test_transform_s3_response_empty():
    response = {
        "Buckets": []
    }

    result = transform_s3_response(response)

    assert result == []


def test_transform_rds_response():
    response = {
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

    result = transform_rds_response(response)

    assert result == [
        {
            "id": "example-db",
            "engine": "postgres",
            "status": "available",
            "instance_class": "db.t3.micro",
            "availability_zone": "us-east-1a"
        }
    ]


def test_transform_rds_response_without_availability_zone():
    response = {
        "DBInstances": [
            {
                "DBInstanceIdentifier": "example-db",
                "Engine": "postgres",
                "DBInstanceStatus": "available",
                "DBInstanceClass": "db.t3.micro"
            }
        ]
    }

    result = transform_rds_response(response)

    assert result[0]["availability_zone"] is None


def test_transform_rds_response_empty():
    response = {
        "DBInstances": []
    }

    result = transform_rds_response(response)

    assert result == []


def test_transform_vpc_response():
    response = {
        "Vpcs": [
            {
                "VpcId": "vpc-123456",
                "CidrBlock": "10.0.0.0/16",
                "State": "available",
                "IsDefault": True
            }
        ]
    }

    result = transform_vpc_response(response)

    assert result == [
        {
            "id": "vpc-123456",
            "cidr_block": "10.0.0.0/16",
            "state": "available",
            "is_default": True
        }
    ]


def test_transform_vpc_response_empty():
    response = {
        "Vpcs": []
    }

    result = transform_vpc_response(response)

    assert result == []


def test_transform_ec2_response_multiple_instances():
    response = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-1111111111",
                        "InstanceType": "t3.micro",
                        "State": {
                            "Name": "running"
                        },
                        "Placement": {
                            "AvailabilityZone": "us-east-1a"
                        }
                    }
                ]
            },
            {
                "Instances": [
                    {
                        "InstanceId": "i-2222222222",
                        "InstanceType": "t3.small",
                        "State": {
                            "Name": "stopped"
                        },
                        "Placement": {
                            "AvailabilityZone": "us-east-1b"
                        }
                    }
                ]
            }
        ]
    }

    result = transform_ec2_response(response)

    assert result == [
        {
            "id": "i-1111111111",
            "type": "t3.micro",
            "state": "running",
            "availability_zone": "us-east-1a"
        },
        {
            "id": "i-2222222222",
            "type": "t3.small",
            "state": "stopped",
            "availability_zone": "us-east-1b"
        }
    ]
