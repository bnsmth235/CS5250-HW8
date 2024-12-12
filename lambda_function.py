import json
import boto3

sqs = boto3.client('sqs')
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/130314348081/cs5250-requests'

# Validate function
def is_valid_widget_request(data):
    """Validate the widget request against the schema."""
    # Check required fields
    required_fields = ["type", "requestId", "widgetId", "owner"]
    for field in required_fields:
        if field not in data or not isinstance(data[field], str):
            return False, f"Missing or invalid required field: {field}"

    # Validate `type` pattern
    if data["type"] not in ["WidgetCreateRequest", "WidgetDeleteRequest", "WidgetUpdateRequest"]:
        return False, "Invalid type field value"

    # Validate `owner` pattern
    if not all(char.isalpha() or char.isspace() for char in data["owner"]):
        return False, "Invalid owner field value"

    # Validate `otherAttributes` if present
    if "otherAttributes" in data:
        if not isinstance(data["otherAttributes"], list):
            return False, "Invalid otherAttributes field value"
        for attr in data["otherAttributes"]:
            if not isinstance(attr, dict):
                return False, "Invalid otherAttributes item"
            if "name" not in attr or "value" not in attr:
                return False, "Missing required fields in otherAttributes item"
            if not isinstance(attr["name"], str) or not isinstance(attr["value"], str):
                return False, "Invalid fields in otherAttributes item"

    return True, None

# Lambda handler
def lambda_handler(event, context):
    try:
        # Parse the incoming request
        body = json.loads(event['body'])

        # Validate the JSON request
        is_valid, error_message = is_valid_widget_request(body)
        if not is_valid:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid widget request', 'error': error_message})
            }

        # Send the valid request to SQS
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(body)
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Widget request submitted successfully'})
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid JSON format'})
        }
    except Exception as e:
        # Handle unexpected errors
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
