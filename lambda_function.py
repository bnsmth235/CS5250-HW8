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
        
    except Exception as e:
        
