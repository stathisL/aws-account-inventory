# AWS Account Inventory - Task List

## Project Goal

Build a small Python application that inventories AWS account resources
using read-only access.

The project should:

- Be safe to run in a personal AWS account.
- Avoid creating billable AWS infrastructure during development.
- Use least-privilege IAM permissions.
- Use temporary credentials rather than permanent access keys.
- Be suitable as a GitHub portfolio project.
- Grow incrementally as AWS knowledge and hands-on experience improve.

---

# Phase 1 - AWS Account Security

- [x] Enable MFA on the root account.
- [x] Confirm root account has no access keys.
- [x] Confirm no unnecessary root credentials exist.
- [x] Configure AWS Budget with a $10 threshold.
- [x] Configure an actual-cost alert at $2.
- [x] Configure a forecasted-cost alert at $5.
- [x] Confirm the account currently has no infrastructure/resources
      created intentionally.

---

# Phase 2 - IAM Foundation

## Admin User

- [x] Confirm existing admin IAM user.
- [x] Confirm `AdministratorAccess`.
- [x] Confirm `IAMUserChangePassword`.
- [x] Confirm MFA is enabled.
- [x] Confirm the admin user has no unnecessary access keys.

## Read-Only Inventory Policy

- [x] Create custom policy:
      `AWSInventoryReadOnlyPolicy`
- [x] Keep the policy limited to the initial inventory scope.
- [x] Avoid adding every AWS service at this stage.

Initial services:

- EC2
- S3
- RDS
- VPC

## Inventory Role

- [x] Create IAM role:
      `AWSInventoryReadOnly`
- [x] Configure the trust relationship.
- [x] Attach `AWSInventoryReadOnlyPolicy`.
- [x] Verify the role contains only the intended policy.

## AssumeRole Permission

- [x] Create:
      `AWSInventoryAssumeRolePolicy`
- [x] Allow `sts:AssumeRole`.
- [x] Restrict the resource to the specific
      `AWSInventoryReadOnly` role.
- [x] Attach the policy to the admin IAM user.

---

# Phase 3 - AWS CLI Authentication

- [x] Confirm AWS CLI is installed.
- [x] Configure AWS region:
      `us-east-1`
- [x] Authenticate using:
      `aws login`
- [x] Create/use dedicated `inventory` profile.
- [x] Verify AWS identity using STS.
- [x] Confirm CLI authentication works without a permanent access key.
- [x] Successfully test `sts:AssumeRole` manually.
- [x] Establish a reusable role-assumption workflow.

### Note

The initial `source_profile` approach did not work correctly with the
newer `aws login` authentication flow.

The project therefore uses Python/boto3 to perform the role assumption.

No permanent access key is used as a workaround.

---

# Phase 4 - Local Python Environment

- [x] Confirm Python is installed.
- [x] Create project directory:
      `aws-account-inventory`
- [x] Create Python virtual environment:
      `.venv`
- [x] Activate virtual environment.
- [x] Install boto3.
- [x] Install `boto3-stubs`.
- [x] Install `botocore[crt]`.
- [x] Create `requirements.txt`.
- [x] Create Makefile for common development commands.

## Project Structure

Current structure:

    aws-account-inventory/
    ├── .gitignore
    ├── Makefile
    ├── README.md
    ├── requirements.txt
    ├── src/
    │   ├── aws_auth.py
    │   ├── aws_clients.py
    │   ├── aws_collectors.py
    │   ├── config.py
    │   ├── custom_types.py
    │   ├── data_transformations.py
    │   ├── inventory.py
    │   └── presentation.py
    ├── tests/
    │   ├── test_aws_auth.py
    │   ├── test_aws_collectors.py
    │   ├── test_config.py
    │   ├── test_data_transformations.py
    │   └── test_inventory.py
    └── docs/
        ├── architecture.md
        ├── authentication.md
        ├── aws-account-security.md
        ├── iam-design.md
        └── TASKS.md

---

# Phase 5 - First Python/AWS Connection

- [x] Create initial `inventory.py`.
- [x] Import boto3.
- [x] Create a boto3 session.
- [x] Create an STS client.
- [x] Call `get_caller_identity()`.
- [x] Successfully connect from Python to AWS.
- [x] Confirm Python receives the AWS account identity.
- [x] Confirm no credentials are stored in source code.
- [x] Confirm no AWS infrastructure is created by the application.

Initial flow:

    Linux
      ↓
    aws login
      ↓
    temporary credentials
      ↓
    boto3
      ↓
    STS
      ↓
    AWS account

---

# Phase 6 - Use the Read-Only Role

- [x] Make boto3 assume `AWSInventoryReadOnly`.
- [x] Obtain temporary credentials from STS.
- [x] Create a boto3 session using the temporary role credentials.
- [x] Verify the resulting identity is:
      `assumed-role/AWSInventoryReadOnly/...`
- [x] Test EC2 read access.
- [x] Test S3 read access.
- [x] Test RDS read access.
- [x] Test VPC read access.
- [x] Verify unauthorized/write operations are denied.

---

# Phase 7 - First Inventory Implementation

- [x] Implement EC2 inventory.
- [x] Implement S3 inventory.
- [x] Implement RDS inventory.
- [x] Implement VPC inventory.
- [x] Create a consistent internal data structure.
- [x] Display a simple human-readable inventory.
- [x] Handle currently empty services cleanly.
- [x] Handle AWS API errors cleanly.
- [x] Avoid modifying AWS resources.

Current inventory scope:

    EC2
    S3
    RDS
    VPC

---

# Phase 8 - Testing

- [x] Install pytest.
- [x] Create unit tests.
- [x] Mock AWS API calls where appropriate.
- [x] Test EC2 inventory transformation.
- [x] Test S3 inventory transformation.
- [x] Test RDS inventory transformation.
- [x] Test VPC inventory transformation.
- [x] Test empty AWS responses.
- [x] Test AWS API failures.
- [x] Test permission failures.
- [x] Test application-level AWS error handling.
- [x] Separate unit tests from real AWS integration checks.
- [x] Separate tests by production module.

Current test modules:

    test_aws_auth.py
    test_aws_collectors.py
    test_config.py
    test_data_transformations.py
    test_inventory.py

---

# Phase 9 - Code Quality

- [x] Add type hints to functions.
- [x] Add function docstrings.
- [x] Use `boto3-stubs` where useful.
- [x] Add logging.
- [x] Add structured error handling.
- [x] Separate AWS authentication from inventory logic.
- [x] Separate AWS clients from inventory logic.
- [x] Separate presentation from collection logic.
- [x] Separate AWS collectors from inventory orchestration.
- [x] Separate inventory transformations from collectors.
- [x] Define shared custom types.
- [x] Add Makefile commands for development.
- [x] Add configuration handling.
- [x] Avoid hard-coded credentials.
- [x] Avoid hard-coded account IDs.

## Configuration

Current configurable settings:

    AWS_INVENTORY_PROFILE
    AWS_INVENTORY_ROLE
    AWS_INVENTORY_REGION
    AWS_INVENTORY_LOG_LEVEL

Default values:

    Profile: inventory
    Role: AWSInventoryReadOnly
    Region: us-east-1
    Log level: INFO

Configuration can be overridden through environment variables.


## Logging

The application uses Python's standard `logging` module.

The default log level is `INFO`.

Logging levels are used according to the importance of the message:

- `DEBUG` for technical details useful during development.
- `INFO` for normal application events.
- `WARNING` for unexpected conditions that do not stop execution.
- `ERROR` for failures.
- `CRITICAL` for severe failures.

The log level can be overridden through:

      AWS_INVENTORY_LOG_LEVEL

Sensitive information such as credentials and session tokens is not logged.


---

# Phase 10 - Documentation

- [x] Create README.
- [x] Create task list.
- [x] Create architecture documentation.
- [x] Document AWS account security setup.
- [x] Document IAM architecture.
- [x] Document authentication flow.
- [x] Document role assumption.
- [x] Document least-privilege decisions.
- [x] Document dependencies.
- [x] Document local setup.
- [x] Document how to run the application.
- [x] Document expected output.
- [x] Document cost considerations.
- [ ] Document lessons learned.

Current documentation:

    README.md
    docs/architecture.md
    docs/authentication.md
    docs/aws-account-security.md
    docs/iam-design.md
    docs/TASKS.md

---

# Phase 11 - Multi-Region Support

Do not implement initially.

- [ ] Understand regional AWS services.
- [ ] Define supported regions.
- [ ] Add region selection.
- [ ] Add multi-region inventory.
- [ ] Prevent accidental scanning of unintended regions.
- [ ] Document global vs regional AWS services.

---

# Phase 12 - Expand AWS Coverage

Add services only when the project needs them.

## Serverless / Messaging

- [ ] Lambda
- [ ] DynamoDB
- [ ] SQS
- [ ] SNS

## Containers

- [ ] ECS
- [ ] EKS
- [ ] ECR

## Networking / Edge

- [ ] Route 53
- [ ] CloudFront
- [ ] Elastic Load Balancing

## Monitoring / Security

- [ ] CloudWatch
- [ ] CloudTrail
- [ ] IAM
- [ ] KMS
- [ ] AWS Config

Do not add permissions until the corresponding functionality is
implemented.

---

# Phase 13 - GitHub Portfolio

- [x] Initialize Git repository.
- [x] Create `.gitignore`.
- [x] Verify no credentials are tracked.
- [x] Make initial commit.
- [x] Create GitHub repository.
- [x] Push project.
- [x] Add architecture documentation.
- [x] Add example output.
- [x] Add security considerations.
- [x] Add future improvements.

---

# Cost / Safety Rules

These rules apply throughout the project.

- Never commit AWS credentials.
- Never put credentials in Python source code.
- Never create access keys unless there is a specific reason.
- Prefer temporary credentials.
- Do not create EC2 instances.
- Do not create RDS databases.
- Do not create NAT Gateways.
- Do not create load balancers.
- Do not create other intentionally billable infrastructure.
- Check AWS billing regularly.
- Keep the AWS Budget alerts configured.
- Prefer read-only API operations during development.
- Test write permissions using permission evaluation or denied
  operations where possible, rather than actually creating resources.

---

# Current Status

Completed:

- AWS account security baseline
- MFA
- AWS Budget and cost alerts
- IAM admin verification
- Read-only IAM policy
- Read-only IAM role
- AssumeRole permission
- AWS CLI authentication
- Dedicated `inventory` profile
- Temporary credential testing
- Python virtual environment
- boto3
- boto3 development stubs
- botocore CRT support
- Python → AWS STS connection
- Python → STS AssumeRole
- Read-only permission verification
- Initial EC2 inventory
- Initial S3 inventory
- Initial RDS inventory
- Initial VPC inventory
- Consistent inventory structure
- Automated unit testing
- AWS API error testing
- Permission failure testing
- Application-level AWS error handling
- Authentication/role-assumption separation
- AWS client separation
- AWS collector separation
- Inventory transformation separation
- Presentation separation
- Shared custom types
- EC2 transformation tests
- S3 transformation tests
- RDS transformation tests
- VPC transformation tests
- Test modules separated by production module
- Empty-response tests
- Makefile for common development commands
- Logging
- Configuration handling
- README
- Architecture documentation
- AWS account security documentation
- IAM design documentation
- Authentication and role-assumption documentation

Current focus:

    Multi-region support
    ↓
    Expand AWS coverage
