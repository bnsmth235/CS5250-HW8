import json
import boto3

sqs = boto3.client('sqs')

QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/130314348081/cs5250-requests'

def validate_request(widget_request):
    if 'widget_id' in widget_request and 'description' in widget_request:
        return True
    return False

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        if validate_request(body):
            sqs.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=json.dumps(body)
            )
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Widget request submitted successfully'})
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid widget request'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
