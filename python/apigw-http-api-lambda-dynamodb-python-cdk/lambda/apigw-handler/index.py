# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import os
import json
import logging
import uuid
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

# Instrument AWS SDK clients with X-Ray
patch_all()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_client = boto3.client("dynamodb")


def handler(event, context):
    table = os.environ.get("TABLE_NAME")
    
    # Extract security context
    request_id = context.request_id
    source_ip = event.get("requestContext", {}).get("identity", {}).get("sourceIp", "unknown")
    user_agent = event.get("requestContext", {}).get("identity", {}).get("userAgent", "unknown")
    http_method = event.get("httpMethod", "unknown")
    path = event.get("path", "unknown")
    
    # Structured logging with security context
    logger.info(json.dumps({
        "event": "request_received",
        "request_id": request_id,
        "source_ip": source_ip,
        "user_agent": user_agent,
        "http_method": http_method,
        "path": path,
        "table_name": table,
    }))
    
    if event["body"]:
        item = json.loads(event["body"])
        logger.info(json.dumps({
            "event": "processing_payload",
            "request_id": request_id,
            "payload": item,
        }))
        year = str(item["year"])
        title = str(item["title"])
        id = str(item["id"])
        dynamodb_client.put_item(
            TableName=table,
            Item={"year": {"N": year}, "title": {"S": title}, "id": {"S": id}},
        )
        message = "Successfully inserted data!"
        logger.info(json.dumps({
            "event": "data_inserted",
            "request_id": request_id,
            "item_id": id,
        }))
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": message}),
        }
    else:
        logger.info(json.dumps({
            "event": "no_payload_received",
            "request_id": request_id,
        }))
        item_id = str(uuid.uuid4())
        dynamodb_client.put_item(
            TableName=table,
            Item={
                "year": {"N": "2012"},
                "title": {"S": "The Amazing Spider-Man 2"},
                "id": {"S": item_id},
            },
        )
        message = "Successfully inserted data!"
        logger.info(json.dumps({
            "event": "default_data_inserted",
            "request_id": request_id,
            "item_id": item_id,
        }))
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": message}),
        }
