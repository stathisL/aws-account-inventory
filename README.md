[# AWS Account Inventory

A small Python application that inventories AWS account resources using
`boto3` and a dedicated read-only IAM role.

The project is designed as a practical AWS and Python learning project,
covering IAM, STS, temporary credentials, boto3, AWS API interaction,
testing, configuration, and application architecture.

## Features

- AWS CLI authentication with `aws login`
- Dedicated `inventory` AWS profile
- AWS STS AssumeRole
- Temporary credentials
- Dedicated read-only IAM role
- Least-privilege permissions
- EC2 inventory
- S3 inventory
- RDS inventory
- VPC inventory
- AWS API error handling
- Application-level error handling
- Environment-based configuration
- Structured application logging
- Unit testing with pytest
- Mocked AWS API calls
- Data transformation layer
- Modular application architecture

## Current Inventory Scope

The application currently inventories:

- EC2
- S3
- RDS
- VPC

The application performs read-only operations and does not intentionally
create AWS infrastructure.

Additional services will be added incrementally as the project develops.

## Architecture

The application separates configuration, authentication, AWS clients,
collectors, transformations, orchestration, and presentation.

```text
AWS CLI
   |
   v
boto3 source session
   |
   v
STS AssumeRole
   |
   v
AWSInventoryReadOnly
   |
   v
Temporary credentials
   |
   v
AWS collectors
   |
   v
Data transformations
   |
   v
Inventory results
   |
   v
Presentation
```

Source code is organized by responsibility:

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

For a detailed explanation of the architecture, see
`docs/architecture.md`.

## Security

The application uses the dedicated IAM role:

```text
AWSInventoryReadOnly
```

with a custom least privilege policy. The role is limited to the read-only permissions
required by the current inventory scope.

AWS STS provides temporary credentials for the assumed role.

No permanent AWS credentials are stored in the application source code.

The development account also uses MFA and AWS Budget alerts as additional
security and cost controls.

For more information, see:

- `docs/aws-account-security.md`
- `docs/iam-design.md`
- `docs/authentication.md`

## Configuration

The application supports configuration through environment variables:

```text
AWS_INVENTORY_PROFILE
AWS_INVENTORY_ROLE
AWS_INVENTORY_REGION
AWS_INVENTORY_LOG_LEVEL
```

Default values:

```text
AWS_INVENTORY_PROFILE=inventory
AWS_INVENTORY_ROLE=AWSInventoryReadOnly
AWS_INVENTORY_REGION=us-east-1
AWS_INVENTORY_LOG_LEVEL=INFO
```

Configuration is kept separate from the application logic so that
environment-specific settings do not need to be hard-coded.

## Prerequisites

You need:

- Python 3 (and the dependencies in requirements.txt installed)
- AWS CLI
- An AWS account
- An authenticated AWS CLI profile named **inventory**
- The required IAM permissions

The application currently uses the AWS CLI `aws login` authentication flow.

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## AWS Authentication

Authenticate using the dedicated profile:

```bash
aws login --profile inventory
```

The application creates a boto3 session using the authenticated profile.

It then uses AWS STS to assume the role:

```text
AWSInventoryReadOnly
```

The resulting temporary credentials are used for the inventory operations.

No permanent AWS access key is required by the application.

## Running the Application

Run:

```bash
make run
```

Or:

```bash
python -m src.inventory
```

## Example Output

The following is illustrative output. Resource counts and timestamps are
examples only and will vary depending on the AWS account and configured
region.

```text
2026-01-15 10:30:00,000 - INFO - __main__ - Starting AWS account inventory
2026-01-15 10:30:01,000 - INFO - src.aws_auth - Starting IAM role assumption
2026-01-15 10:30:01,300 - INFO - src.aws_auth - IAM role assumed successfully
2026-01-15 10:30:01,700 - INFO - src.aws_collectors - EC2 inventory retrieved successfully
2026-01-15 10:30:02,000 - INFO - src.aws_collectors - S3 inventory retrieved successfully
2026-01-15 10:30:02,400 - INFO - src.aws_collectors - RDS inventory retrieved successfully
2026-01-15 10:30:02,800 - INFO - src.aws_collectors - VPC inventory retrieved successfully

AWS ACCOUNT INVENTORY

EC2
  Resources: 2

S3
  Resources: 3

RDS
  Resources: 1

VPC
  Resources: 4
```

The output demonstrates the application lifecycle:

1. Application startup
2. IAM role assumption
3. Inventory collection
4. Resource counting
5. Human-readable presentation

## Testing

The project uses `pytest` for automated unit testing.

Run the tests with:

```bash
make test
```

or:

```bash
python -m pytest -v
```

The tests cover:

- Authentication and role assumption
- AWS collectors
- Data transformations
- Configuration
- Inventory orchestration
- Empty AWS responses
- AWS API failures
- Permission failures
- Application-level error handling

AWS API calls are mocked where appropriate, allowing the test suite to run
without creating AWS resources.

## Makefile

The project provides simple commands for common development tasks:

```text
make run
make test
```

- `make run` runs the inventory application.
- `make test` runs the test suite.

## Project Structure

The application is organized into separate modules for configuration,
authentication, AWS clients, collection, transformation, orchestration,
presentation, and testing.

For a detailed explanation of the application architecture and module
responsibilities, see `docs/architecture.md`.


## Cost and Safety

The application is designed to minimize AWS cost and operational risk.

It does not intentionally create:

- EC2 instances
- RDS databases
- NAT Gateways
- Load balancers
- Other billable infrastructure

The development account uses AWS Budget alerts to help detect unexpected
costs.

The project follows these safety principles:

- Use temporary credentials.
- Use least-privilege IAM permissions.
- Never commit credentials.
- Never hard-code credentials.
- Avoid unnecessary AWS permissions.
- Prefer read-only operations.
- Monitor AWS costs.


## Documentation

Detailed project documentation is available in the `docs/` directory:

- `architecture.md` - application architecture and module responsibilities.
- `authentication.md` - AWS authentication, STS, AssumeRole, and temporary credentials.
- `aws-account-security.md` - account security and cost protection.
- `iam-design.md` - IAM roles, policies, trust relationships, and least-privilege design.
- `TASKS.md` - project roadmap and implementation progress.

## Current Limitations

The application currently operates in a single configured AWS region.

The inventory scope is limited to:

- EC2
- S3
- RDS
- VPC

Multi-region support and additional AWS services are planned for future
iterations.

## Future Improvements

Planned improvements include:

- Multi-region inventory
- Additional AWS service collectors
- JSON output
- Expanded resource information
- Additional configuration options
- Expanded automated testing
- Documentation of lessons learned

The project will continue to grow incrementally rather than attempting to
support every AWS service at once.

## Learning Goals

This project provides practical experience with:

- AWS IAM
- IAM policies and roles
- Least privilege
- AWS STS
- Temporary credentials
- AWS CLI
- boto3
- AWS regional services
- Python application architecture
- Automated testing
- AWS security practices
- AWS cost awareness
- AWS Solutions Architect Associate concepts

## License

This project is intended as a personal learning and portfolio project.
