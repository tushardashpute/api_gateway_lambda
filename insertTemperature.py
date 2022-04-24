import json
import boto3
from datetime import datetime
#That's the lambda handler, you can not modify this method
# the parameters from JSON body can be accessed like deviceId = event['deviceId']
def lambda_handler(event, context):
    # Instanciating connection objects with DynamoDB using boto3 dependency
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')

    # Getting the table the table Temperatures object
    tableTemperature = dynamodb.Table('temperatures')

    # Getting the current datetime and transforming it to string in the format bellow
    eventDateTime = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    deviceId = event['deviceId']
    temperature = event['temperature']

    # Putting a try/catch to log to user when some error occurs
    try:

        tableTemperature.put_item(
           Item={
                'eventDateTime': eventDateTime,
                'deviceId': deviceId,
                'temperature': int(temperature)
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Succesfully inserted temperature!')
        }
    except:
        print('Closing lambda function')
        return {
                'statusCode': 400,
                'body': json.dumps('Error saving the temperature')
        }
