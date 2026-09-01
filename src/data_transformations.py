from typing import Any


def transform_ec2_response(response: dict) -> list[dict[str, Any]]:
    """Transform an EC2 API response into inventory resources."""

    resources = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            resources.append(
                {
                    "id": instance["InstanceId"],
                    "type": instance["InstanceType"],
                    "state": instance["State"]["Name"],
                    "availability_zone": instance["Placement"]["AvailabilityZone"]
                }
            )

    return resources


def transform_s3_response(response: dict) -> list[dict[str, Any]]:
    """Transform an S3 API response into inventory resources."""

    resources = []

    for bucket in response["Buckets"]:
        resources.append(
            {
                "id": bucket["Name"],
                "created": bucket["CreationDate"].isoformat()
            }
        )

    return resources


def transform_rds_response(response: dict) -> list[dict[str, Any]]:
    """Transform an RDS API response into inventory resources."""

    resources = []

    for db_instance in response["DBInstances"]:
        resources.append(
            {
                "id": db_instance["DBInstanceIdentifier"],
                "engine": db_instance["Engine"],
                "status": db_instance["DBInstanceStatus"],
                "instance_class": db_instance["DBInstanceClass"],
                "availability_zone": db_instance.get("AvailabilityZone")
            }
        )

    return resources


def transform_vpc_response(response: dict) -> list[dict[str, Any]]:
    """Transform a VPC API response into inventory resources."""

    resources = []

    for vpc in response["Vpcs"]:
        resources.append(
            {
                "id": vpc["VpcId"],
                "cidr_block": vpc.get("CidrBlock"),
                "state": vpc["State"],
                "is_default": vpc["IsDefault"]
            }
        )

    return resources
