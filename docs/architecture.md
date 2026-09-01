# AWS Account Inventory - Architecture

## Overview

AWS Account Inventory is a small Python application that uses `boto3` to
collect read-only information about AWS resources.

The application uses AWS CLI authentication and AWS STS AssumeRole to obtain
temporary credentials for a dedicated read-only IAM role.

The initial inventory scope is:

- EC2
- S3
- RDS
- VPC

The application separates authentication, configuration, AWS client
creation, resource collection, data transformation, orchestration, and
presentation.

---

## High-Level Architecture

```text
┌──────────────────────┐
│         User         │
└──────────┬───────────┘
           │
           │ aws login
           ▼
┌──────────────────────┐
│    AWS CLI Profile   │
│      inventory       │
└──────────┬───────────┘
           │
           │ boto3
           ▼
┌──────────────────────┐
│    Source Session    │
│  Authenticated AWS   │
│      identity        │
└──────────┬───────────┘
           │
           │ STS AssumeRole
           ▼
┌──────────────────────┐
│ AWSInventoryReadOnly │
│        Role          │
└──────────┬───────────┘
           │
           │ Temporary credentials
           ▼
┌──────────────────────┐
│ Read-Only boto3      │
│       Session        │
└──────────┬───────────┘
           │
     ┌─────┼─────┬─────┐
     ▼     ▼     ▼     ▼
    EC2    S3    RDS   VPC
     │     │     │     │
     └─────┼─────┼─────┘
           │
           ▼
┌──────────────────────────┐
│   Data Transformations   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│      Presentation        │
└──────────────────────────┘
```

---

## Application Structure

The application code is organized into the following modules:

```text
src/
├── aws_auth.py
├── aws_clients.py
├── aws_collectors.py
├── config.py
├── custom_types.py
├── data_transformations.py
├── inventory.py
└── presentation.py
```

Each module has a specific responsibility.

---

## Configuration

`config.py` provides application configuration.

Current configuration values include:

- AWS profile
- IAM role name
- AWS region
- Logging level

The configuration can be controlled through environment variables.

Default values are:

```text
export AWS_INVENTORY_PROFILE=inventory
export AWS_INVENTORY_ROLE=AWSInventoryReadOnly
export AWS_INVENTORY_REGION=us-east-1
export AWS_INVENTORY_LOG_LEVEL=INFO
```

Keeping configuration separate from application logic prevents environment
specific settings from being spread throughout the code.

---

## Authentication

`aws_auth.py` contains the role-assumption logic.

The module:

1. Receives an authenticated boto3 source session.
2. Creates an STS client.
3. Builds the IAM role ARN.
4. Calls `AssumeRole`.
5. Receives temporary credentials.
6. Creates a new boto3 session using those credentials.

The authentication module does not collect inventory data.

---

## AWS Clients

`aws_clients.py` is responsible for creating boto3 service clients.

Currently supported clients include:

- EC2
- S3
- RDS

VPC operations use the EC2 client because VPC resources are accessed through
the EC2 API.

Keeping client creation in its own module prevents boto3 client creation
from being duplicated throughout the collectors.

---

## Collectors

`aws_collectors.py` contains the AWS resource collection functions.

Current collectors are:

```text
collect_ec2_inventory()
collect_s3_inventory()
collect_rds_inventory()
collect_vpc_inventory()
```

Each collector:

1. Obtains the required AWS client.
2. Calls the appropriate read-only AWS API.
3. Passes the response to a transformation function.
4. Returns a consistent inventory result.

Collectors are responsible for retrieving AWS data, not displaying it.

---

## Data Transformations

`data_transformations.py` converts AWS API responses into the application's
internal inventory format.

AWS APIs return service-specific response structures.

The transformation layer converts those different structures into a
consistent representation.

This keeps AWS-specific response formats isolated from the presentation and
orchestration layers.

---

## Custom Types

`custom_types.py` contains shared type definitions used throughout the
application.

The shared types provide a consistent structure for inventory results and
improve readability and static type checking.

The collectors and presentation layer can therefore work with the same
internal representation.

---

## Inventory Orchestration

`inventory.py` is the main application entry point.

It coordinates the complete inventory workflow:

1. Load configuration.
2. Configure logging.
3. Create the source boto3 session.
4. Verify the source AWS identity using STS.
5. Assume the read-only IAM role.
6. Create the temporary role session.
7. Run the inventory collectors.
8. Combine the inventory results.
9. Pass the results to the presentation layer.
10. Handle AWS errors at the application boundary.

The orchestration layer does not contain the detailed implementation of
individual AWS collectors.

---

## Presentation

`presentation.py` is responsible for displaying inventory results.

The presentation layer receives transformed inventory data and formats it
for the user.

It does not:

- Create AWS clients.
- Authenticate with AWS.
- Assume IAM roles.
- Make AWS API calls.
- Collect resources.

This keeps presentation logic independent of AWS operations.

---

## Inventory Data Flow

The application processes data through the following stages:

```text
AWS authentication
        │
        ▼
Temporary role session
        │
        ▼
AWS service clients
        │
        ▼
AWS collectors
        │
        ▼
AWS API responses
        │
        ▼
Data transformations
        │
        ▼
Consistent inventory data
        │
        ▼
Presentation
```

This separation allows each stage to be tested independently.

---

## Error Handling

AWS API errors are handled at the application boundary.

AWS `ClientError` exceptions are converted into an application-level
`InventoryError`.

Permission-related errors such as:

- `AccessDenied`
- `UnauthorizedOperation`

are identified and reported as permission errors.

The application does not attempt to bypass or escalate permissions when an
operation is denied.

---

## Logging

The application uses Python's standard `logging` module.

Logging is used to provide visibility into the application lifecycle without
exposing sensitive information.

The default log level is `INFO`.

Typical log levels are:

- `DEBUG` for technical details useful during development.
- `INFO` for normal application events.
- `WARNING` for unexpected conditions that do not stop execution.
- `ERROR` for failures.
- `CRITICAL` for severe failures.

The log level can be overridden through the following environment variable:

```text
export AWS_INVENTORY_LOG_LEVEL=DEBUG
```

Credentials, secret keys, and session tokens are not logged.

---

## Testing Architecture

The project separates unit tests from real AWS integration checks.

```text
tests/
├── test_aws_auth.py
├── test_aws_collectors.py
├── test_config.py
├── test_data_transformations.py
└── test_inventory.py
```

AWS API calls are mocked where appropriate.

The tests cover:

- AWS authentication and role assumption
- AWS collectors
- Data transformations
- Configuration
- Inventory orchestration
- Empty AWS responses
- AWS API failures
- Permission failures
- Application-level error handling

The test suite allows most application behavior to be validated without
creating AWS resources.

---

## Separation of Responsibilities

The architecture intentionally keeps responsibilities separate.

```text
config.py
    │
    ▼
Configuration

aws_auth.py
    │
    ▼
Authentication / Role Assumption

aws_clients.py
    │
    ▼
AWS Client Creation

aws_collectors.py
    │
    ▼
AWS Resource Collection

data_transformations.py
    │
    ▼
Data Normalization

inventory.py
    │
    ▼
Application Orchestration

presentation.py
    │
    ▼
Human-Readable Output
```

This structure makes the application easier to test, maintain, and extend.

---

## Regional Scope

The application currently operates in a single configured AWS region:

```text
us-east-1
```

The region is configurable through:

```text
AWS_INVENTORY_REGION
```

EC2, RDS, and VPC inventory are regional.

S3 has different regional and global characteristics and is handled
separately by its collector.

Multi-region support is intentionally postponed until the regional behavior
of the current services is better understood.

---

## Security Boundary

The application architecture is designed around a read-only security
boundary.

```text
Authenticated Source Identity
            │
            ▼
      STS AssumeRole
            │
            ▼
  AWSInventoryReadOnly
            │
            ▼
 Read-Only AWS Operations
```

The detailed IAM design and security configuration are documented separately
in:

- `iam-design.md`
- `aws-account-security.md`

---

## Future Architecture

Future improvements may include:

- Multi-region inventory
- Additional AWS service collectors
- JSON output
- More detailed resource information
- Additional configuration options
- Improved observability
- Expanded automated testing

New AWS services should be added incrementally.

Each new service should have:

1. A collector.
2. Required IAM permissions.
3. Data transformations.
4. Unit tests.
5. Error handling.
6. Documentation.

This keeps the architecture small and maintainable while allowing the
application to grow modular over time.
