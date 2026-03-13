---
name: aws-cli
description: Amazon Web Services automation. Manage EC2, S3, Lambda, RDS, and all AWS services programmatically.
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires": { "bins": ["aws"], "env": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"] },
        "primaryEnv": "AWS_ACCESS_KEY_ID",
      },
  }
---

# AWS CLI

Cloud infrastructure automation via Amazon Web Services.

## Quick Start

```bash
{baseDir}/scripts/list-instances.sh
```

## Environment Variables

- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key
- `AWS_DEFAULT_REGION` - Default region (e.g., us-east-1)
- `AWS_DEFAULT_OUTPUT` - Output format (json, text, table)

## Usage Examples

```bash
# List EC2 instances
{baseDir}/scripts/list-instances.sh

# Create S3 bucket
{baseDir}/scripts/create-bucket.sh --name my-bucket --region us-east-1

# Upload to S3
{baseDir}/scripts/s3-upload.sh --bucket my-bucket --file local-file.txt --key remote-file.txt

# List S3 buckets
{baseDir}/scripts/list-buckets.sh

# Invoke Lambda
{baseDir}/scripts/invoke-lambda.sh --function my-function --payload '{"key":"value"}'

# Deploy CloudFormation stack
{baseDir}/scripts/deploy-stack.sh --template template.yaml --stack-name my-stack
```

## Supported Services

- EC2 (compute)
- S3 (storage)
- Lambda (serverless)
- RDS (databases)
- CloudFormation (infrastructure as code)
- IAM (identity)
- CloudWatch (monitoring)
- 200+ more services

## Setup

1. Install AWS CLI: `brew install awscli` or download from AWS
2. Get access keys: AWS Console → IAM → Users → Security credentials
3. Configure: `aws configure` or set environment variables
