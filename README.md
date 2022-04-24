# api_gateway_lambda
api_gateway_lambda

The AWS services are:

- API Gateway — This service is responsible for deploying and serving HTTP RESTful endpoints. Thus you can trigger actions, when HTTP calls arrives to the generated endpoints.
- Lambda — This let you run code without provisioning or managing servers.
- DynamoDB — The NoSQL amazon database, where you can insert the information of your application on tables (Collections).

<img width="1044" alt="image" src="https://user-images.githubusercontent.com/74225291/164957231-04e3d183-4791-4561-8f34-1e9c84230d4b.png">


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


<img width="1519" alt="image" src="https://user-images.githubusercontent.com/74225291/164957160-1ddcf1ec-cf56-4c2e-bf21-909e6c372b77.png">


<img width="1442" alt="image" src="https://user-images.githubusercontent.com/74225291/164957197-1a20c76c-b20a-42b4-b69f-c67305edfc04.png">


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


<img width="1407" alt="image" src="https://user-images.githubusercontent.com/74225291/164957216-6196ba9e-e8ae-48a9-ba15-ac2747da7a19.png">

<img width="1461" alt="image" src="https://user-images.githubusercontent.com/74225291/164957259-4bb7b846-8e2d-44aa-ac2c-21174e4ed304.png">
