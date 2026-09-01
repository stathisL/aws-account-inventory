# AWS Account Inventory - AWS Account Security

## Purpose

This document describes the security baseline configured for the AWS
account used during development of the AWS Account Inventory project.

## Root Account Security

The AWS root account is protected with MFA.

The root account is not used for normal development activities.

The root account has no access keys.

## Inventory Role

The application uses a dedicated IAM role:

    AWSInventoryReadOnly

The role uses the custom policy:

    AWSInventoryReadOnlyPolicy

The policy is limited to the read-only permissions required by the current
inventory scope.

Current services include:

- EC2
- S3
- RDS
- VPC

## Temporary Credentials

The application uses temporary credentials obtained through AWS STS.

The authentication flow is:

    AWS CLI
       ↓
    aws login
       ↓
    Temporary credentials
       ↓
    boto3 source session
       ↓
    STS AssumeRole
       ↓
    AWSInventoryReadOnly
       ↓
    Temporary role credentials
       ↓
    Inventory operations

Permanent AWS access keys are not stored in the application source code.

## Cost Protection

AWS Budget alerts are configured to help detect unexpected costs.

The account uses:

- $10 budget threshold
- $2 actual-cost alert
- $5 forecasted-cost alert

The application does not intentionally create AWS infrastructure.

## Security Philosophy

The project follows these principles:

- MFA
- Temporary credentials
- Dedicated IAM role
- Least-privilege permissions
- Read-only API operations
- No intentional infrastructure creation
- Cost monitoring
