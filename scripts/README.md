# Scripts Directory

This directory contains utility scripts for the Starshield Network Monitor project.

## AWS iperf3 Server Scripts

### `create_iperf3_server.py`
**Purpose**: Automatically creates an AWS EC2 instance with iperf3 server in Frankfurt region
**Usage**: `python create_iperf3_server.py`
**Requirements**: AWS CLI configured with valid credentials

### `cleanup_iperf3_server.py`
**Purpose**: Terminates AWS EC2 instance and cleans up all resources
**Usage**: `python cleanup_iperf3_server.py`
**Requirements**: Must have `iperf3_server_info.json` file from create script

### `update_aws_server.py`
**Purpose**: Updates the monitoring app to use your AWS iperf3 server
**Usage**: `python update_aws_server.py <AWS_EC2_IP>`
**Example**: `python update_aws_server.py 3.15.123.45`

### `test_iperf3_server.py`
**Purpose**: Tests iperf3 server connection and performance
**Usage**: `python test_iperf3_server.py <SERVER_IP> [PORT] [DURATION]`
**Example**: `python test_iperf3_server.py 3.15.123.45 5201 10`

## Documentation

### `AWS_iperf3_Setup_Guide.md`
Complete setup guide for AWS iperf3 server with both manual and automated options.

### `Frankfurt_Setup_Quick.md`
Quick 5-minute setup guide specifically for Frankfurt region (optimized for Germany).

## Prerequisites

Before running any AWS scripts, ensure you have:
1. AWS CLI installed: `pip install awscli`
2. AWS credentials configured: `aws configure`
3. Region set to Frankfurt: `aws configure set region eu-central-1`
4. boto3 installed: `pip install boto3`

## Quick Start

1. **Manual Setup** (Recommended):
   - Follow `Frankfurt_Setup_Quick.md`
   - Test with `test_iperf3_server.py`
   - Update app with `update_aws_server.py`

2. **Automated Setup**:
   - Run `create_iperf3_server.py`
   - Test with `test_iperf3_server.py`
   - Update app with `update_aws_server.py`

## Cleanup

When done testing, run `cleanup_iperf3_server.py` to terminate all AWS resources and avoid charges.
