#!/bin/bash
# AWS EC2 Instances List Script
# Usage: list-instances.sh [--region <region>]

AWS_ACCESS_KEY="${AWS_ACCESS_KEY_ID:-}"
AWS_SECRET_KEY="${AWS_SECRET_ACCESS_KEY:-}"
REGION="${AWS_DEFAULT_REGION:-us-east-1}"

if ! command -v aws &> /dev/null; then
  echo "Error: AWS CLI not installed"
  echo "Install: brew install awscli"
  exit 1
fi

if [ -z "$AWS_ACCESS_KEY" ]; then
  echo "Error: AWS_ACCESS_KEY_ID not set"
  exit 1
fi

echo "Listing EC2 instances in region: $REGION"
aws ec2 describe-instances --region "$REGION" --output table \
  --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,PublicIpAddress]'
