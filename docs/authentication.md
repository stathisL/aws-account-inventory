# AWS Account Inventory — Authentication

## Overview

AWS Account Inventory uses the AWS CLI aws login authentication flow with AWS STS AssumeRole.

The application does not use or store permanent AWS access keys.

The authentication flow is:

```text
AWS CLI
|
| aws login
v
inventory profile
|
| boto3
v
Source session
|
| STS AssumeRole
v
AWSInventoryReadOnly
|
v
Temporary credentials
|
v
Read-only boto3 session
|
v
AWS inventory operations
```

## AWS CLI Authentication

The dedicated inventory profile is authenticated with:

```bash
aws login --profile inventory
```

boto3 uses this authenticated profile to create the initial source session.

The source session is used to request the read-only inventory role.

## STS AssumeRole

The application uses AWS STS to assume the AWSInventoryReadOnly role.

STS returns temporary credentials containing:

Access key ID
Secret access key
Session token
Expiration time

The application uses these temporary credentials to create a new boto3 session for inventory operations.

The inventory collectors therefore operate using the permissions of the read-only role.

## IAM Security Boundary

The source identity is allowed to assume the specific inventory role using:

```text
sts:AssumeRole
```

The AWSInventoryReadOnly role contains the custom AWSInventoryReadOnlyPolicy.

The policy currently provides only the read-only permissions required for:

EC2
S3
RDS
VPC

Additional permissions will be added only when new inventory functionality is implemented.

The detailed IAM design is documented in:

docs/iam-design.md

## Credential Security

The application:

Does not contain permanent AWS access keys.
Does not hard-code credentials.
Uses temporary STS credentials.
Does not log secret keys or session tokens.
Does not attempt to bypass denied permissions.

Credentials are obtained at runtime and passed to the temporary boto3 session.

## Identity Verification

The application verifies the AWS identity using STS get_caller_identity().

After assuming the role, the expected identity is similar to:

```text
arn:aws:sts::<account-id>:assumed-role/AWSInventoryReadOnly/<session-name>
```

This confirms that inventory operations are performed using the intended role.

## Why AssumeRole?

The application does not need the broad permissions of an administrator.

Instead, the authenticated source identity assumes a dedicated role with only the permissions required for inventory.

This provides a clear least-privilege security boundary:

```text
Source Identity
|
| AssumeRole
v
AWSInventoryReadOnly
|
| Read-only permissions
v
AWS Resources
```

## source_profile Note

The project initially attempted to use a source_profile role-assumption configuration.

This did not work correctly with the newer aws login authentication flow.

The project therefore performs AssumeRole directly through boto3 and STS.

No permanent access key was introduced as a workaround.

## Testing

Authentication logic is tested in:

```text
tests/test_aws_auth.py
```

Tests cover:

Role assumption
Temporary credential handling
Authentication failures
Permission failures

AWS API calls are mocked where appropriate so authentication logic can be tested without creating AWS resources.
