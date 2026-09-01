# AWS Account Inventory - IAM Design

## Purpose

This document describes the IAM design used by the AWS Account Inventory
project.

The design focuses on:

- Least privilege
- Temporary credentials
- Separation of administrative and application access
- Explicit role assumption
- Read-only inventory operations

---

## IAM Components

The project currently uses the following IAM components:

    Admin IAM User
          |
          | sts:AssumeRole
          v
    AWSInventoryReadOnly
          |
          v
    AWSInventoryReadOnlyPolicy

The administrator identity is used to authenticate and assume the dedicated
inventory role.

The application performs AWS inventory operations using the permissions
attached to the `AWSInventoryReadOnly` role.

---

## Administrator User

An existing IAM administrator user is used for administrative tasks.

The administrator user has:

- `AdministratorAccess`
- `IAMUserChangePassword`
- MFA enabled

The administrator user is not used directly by the inventory collectors.

Its role in the application flow is to provide the authenticated identity
that is permitted to assume the inventory role.

---

## Inventory Role

The application uses the dedicated IAM role:

    AWSInventoryReadOnly

The role is designed specifically for the inventory application.

The role does not contain administrative permissions.

It has the custom policy:

    AWSInventoryReadOnlyPolicy

The role is assumed through AWS STS using temporary credentials.

---

## AssumeRole Permission

The administrator user has a separate policy:

    AWSInventoryAssumeRolePolicy

This policy allows:

    sts:AssumeRole

The permission is restricted to the specific role:

    AWSInventoryReadOnly

The application therefore does not receive general permission to assume
arbitrary IAM roles.

---

## Read-Only Policy

The inventory role uses:

    AWSInventoryReadOnlyPolicy

The policy contains only the permissions required for the current inventory
scope.

The initial scope is:

- EC2
- S3
- RDS
- VPC

The application uses read-only AWS API operations to retrieve resource
information.

No create, modify, or delete permissions are required for the current
inventory functionality!

---

## Least Privilege

The project follows the principle of least privilege.

Instead of granting broad permissions such as full access to AWS services,
the inventory role receives only the permissions required for the
implemented collectors.

The IAM policy should grow only when application functionality grows.

For example, adding Lambda inventory in the future should involve:

1. Implementing the Lambda collector.
2. Identifying the required read-only Lambda API operations.
3. Adding only the required IAM permissions.
4. Adding unit tests.
5. Testing the permissions.
6. Updating the documentation.

Permissions for services that are not implemented should not be added
prematurely.

---

## Authentication and Authorization

The IAM design separates authentication from authorization.

### Authentication

Authentication establishes the identity used to access AWS.

The application starts with an authenticated boto3 session based on the AWS
CLI login flow.

### Role Assumption

AWS STS is used to assume:

    AWSInventoryReadOnly

STS returns temporary credentials for the assumed role.

### Authorization

Authorization determines which AWS API operations the assumed role is
allowed to perform.

Those permissions come from:

    AWSInventoryReadOnlyPolicy

The resulting flow is:

    Authenticated identity
            |
            v
      sts:AssumeRole
            |
            v
    AWSInventoryReadOnly
            |
            v
    AWSInventoryReadOnlyPolicy
            |
            v
    Read-only AWS operations

---

## Temporary Credentials

The application uses temporary credentials returned by AWS STS.

The credentials include:

- Access key ID
- Secret access key
- Session token
- Expiration information

These credentials are used to create the boto3 session for the inventory
operations.

The application does not store permanent AWS access keys in source code.

Temporary credentials are not intentionally written to application logs.

---

## Current Inventory Permissions

The IAM policy is intentionally limited to the services currently supported
by the application:

    EC2
    S3
    RDS
    VPC

The exact API actions should remain aligned with the implemented collectors.

As the application grows, permissions should be reviewed rather than
automatically expanded.

---

## Security Considerations

The IAM design provides several security boundaries:

- MFA protects the administrative identity.
- The application uses a dedicated IAM role.
- Role assumption is explicitly permitted.
- The AssumeRole permission is restricted to the intended role.
- The inventory role is read-only.
- Temporary credentials are used for inventory operations.
- Unnecessary AWS service permissions are avoided.
- The application does not require permanent access keys.

This reduces the impact of accidentally using the wrong credentials and
prevents the inventory application from performing AWS write operations
allowed by the inventory role.

---

## Future IAM Changes

Future AWS services will be added incrementally.

When a new service is introduced, its IAM requirements should be evaluated
independently.

The project should avoid creating a broad policy containing every AWS
service simply for future compatibility.

The intended approach is:

    New feature
        ↓
    Required AWS API calls
        ↓
    Required IAM actions
        ↓
    Least-privilege policy update
        ↓
    Tests
        ↓
    Documentation

This keeps the IAM configuration understandable, reviewable, and aligned
with the actual application functionality.
