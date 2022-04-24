import json
import boto3
def lambda_handler(event, context):
  # TODO implement
  dynamodb = boto3.resource('dynamodb')
  tableTemperatures = dynamodb.Table('temperatures')
  response = tableTemperatures.scan()
  return {
    'statusCode': 200,
    'body': response['Items']
  }
