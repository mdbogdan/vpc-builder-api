# AWS VPC Builder API
This repository contains a serverless Python API that dynamically provisions AWS VPCs and Subnets. The infrastructure and application are deployed as a single unit using the AWS Serverless Application Model (SAM).

## Architecture Overview

This solution relies on a fully serverless architecture:
* **Compute:** AWS Lambda (Python 3.12)
* **API Layer:** Amazon API Gateway (REST API)
* **Authentication:** Amazon Cognito User Pools for JWT-based endpoint protection
* **Storage:** Amazon DynamoDB to store metadata of the created networks
* **Infrastructure as Code :** AWS SAM (`template.yaml`)

## Project Structure

* `template.yaml`: The SAM template defining all AWS resources and permissions
* `src/app.py`: The Python Lambda handlers for the POST and GET API routes
* `src/requirements.txt`: Python dependencies (`boto3`)

## Prerequisites

To deploy and test this API locally, you will need:
* AWS CLI
* AWS SAM CLI installed
* Python 3.12

## Quick Start: Deployment

1. **Build the application:**
   ```console
   sam build
   ```

2. **Deploy to AWS:**
   ```console
   sam deploy --guided
   ```
   The deployment will output the ApiUrl, CognitoClientId, and CognitoUserPoolId needed to test the endpoints.

## API Usage
The API is secured. You must first create a user in the Cognito User Pool and retrieve an IdToken via the AWS CLI to authenticate your requests.

1. **Create a VPC:**
   Creates a new VPC and the specified subnets, then stores the metadata in DynamoDB.

    ```console
      curl -X POST <YOUR_API_URL> \
      -H "Authorization: <YOUR_ID_TOKEN>" \
      -H "Content-Type: application/json" \
      -d '{"vpc_cidr": "<CIDR1>", "subnet_cidrs": ["<CIDR2>", "<CIDR3>"]}'
      ```


2. **List Created VPCs:**
  ```console
     curl -X GET <ApiUrl> \
      -H "Authorization: <YOUR_ID_TOKEN>"
  ```