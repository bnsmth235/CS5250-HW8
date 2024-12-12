import json
import boto3
from jsonschema import validate, ValidationError

# SQS Client
sqs = boto3.client('sqs')

# Replace with your SQS queue URL
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/130314348081/cs5250-requests'

# Widget Schema
WIDGET_SCHEMA = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "type": {
      "type": "string",
      "pattern": "WidgetCreateRequest|WidgetDeleteRequest|WidgetUpdateRequest"
    },
    "requestId": {
      "type": "string"
    },
    "widgetId": {
      "type": "string"
    },
    "owner": {
      "type": "string",
      "pattern": "[A-Za-z ]+"
    },
    "label": {
      "type": "string"
    },
    "description": {
      "type": "string"
    },
    "otherAttributes": {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "name": {
              "type": "string"
            },
            "value": {
              "type": "string"
            }
          },
          "required": [
            "name",
            "value"
          ]
        }
      ]
    }
  },
  "required": [
    "type",
    "requestId",
    "widgetId",
    "owner"
  ]
}

# Lambda Handler
def lambda_handler(event, context):
    try:
        # Parse the incoming request
        body = json.loads(event['body'])

        # Validate the JSON against the schema
        validate(instance=body, schema=WIDGET_SCHEMA)

        # Send the valid request to SQS
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(body)
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Widget request submitted successfully'})
        }
    except ValidationError as e:
        # Handle schema validation errors
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid widget request', 'error': str(e)})
        }
    except Exception as e:
        # Handle other unexpected errors
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
