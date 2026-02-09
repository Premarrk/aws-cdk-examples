
# AWS API Gateway HTTP API to AWS Lambda in VPC to DynamoDB CDK Python Sample!


## Overview

Creates an [AWS Lambda](https://aws.amazon.com/lambda/) function writing to [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) and invoked by [Amazon API Gateway](https://aws.amazon.com/api-gateway/) REST API. 

This implementation includes AWS Well-Architected Framework best practices:
- **End-to-end tracing** with AWS X-Ray for monitoring request flows
- **CloudWatch alarms** for proactive error detection
- **VPC endpoints** for secure, private connectivity
- **Comprehensive security logging** with CloudTrail, VPC Flow Logs, and API Gateway access logs
- **Structured application logging** with security context (request ID, source IP, user agent)
- **Log retention policies** aligned with compliance requirements (1 year retention)
- **DynamoDB point-in-time recovery** for data protection and audit

![architecture](docs/architecture.png)

## Setup

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Deploy
At this point you can deploy the stack. 

Using the default profile

```
$ cdk deploy
```

With specific profile

```
$ cdk deploy --profile test
```

## After Deploy
Navigate to AWS API Gateway console and test the API with below sample data 
```json
{
    "year":"2023", 
    "title":"kkkg",
    "id":"12"
}
```

You should get below response 

```json
{"message": "Successfully inserted data!"}
```

### Monitoring with X-Ray
After deployment, you can monitor request traces in the AWS X-Ray console:
1. Navigate to AWS X-Ray console
2. View the service map to see request flows between API Gateway → Lambda → DynamoDB
3. Analyze traces to identify latency bottlenecks and errors
4. Use CloudWatch alarms to receive notifications for Lambda errors and API Gateway 5xx responses

### Security Logging and Audit
The stack implements comprehensive security logging:

**CloudTrail**: All API calls to AWS services are logged to S3 bucket with 7-year retention
- View logs: Navigate to CloudTrail console → Event history
- S3 bucket: Check CloudFormation outputs for bucket name

**VPC Flow Logs**: Network traffic is logged to CloudWatch Logs
- View logs: CloudWatch console → Log groups → `/aws/vpc/flowlogs`
- Retention: 1 year

**API Gateway Access Logs**: All API requests are logged with caller identity, IP, and request details
- View logs: CloudWatch console → Log groups → API Gateway access logs
- Format: JSON with standard fields (caller, IP, method, status, etc.)

**Lambda Application Logs**: Structured JSON logs with security context
- View logs: CloudWatch console → Log groups → `/aws/lambda/apigw_handler`
- Includes: request_id, source_ip, user_agent, event details
- Retention: 1 year

**DynamoDB Point-in-Time Recovery**: Enabled for data protection and audit
- Restore capability: Up to 35 days of continuous backups

## Cleanup 
Run below script to delete AWS resources created by this sample stack.
```
cdk destroy
```

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
