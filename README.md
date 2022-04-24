# api_gateway_lambda
api_gateway_lambda

<img width="1300" alt="image" src="https://user-images.githubusercontent.com/74225291/164957345-b9b44e03-9572-4921-92a3-d478cc0f5168.png">


The AWS services are:

- API Gateway — This service is responsible for deploying and serving HTTP RESTful endpoints. Thus you can trigger actions, when HTTP calls arrives to the generated endpoints.
- Lambda — This let you run code without provisioning or managing servers.
- DynamoDB — The NoSQL amazon database, where you can insert the information of your application on tables (Collections).

**AWS API Gateway**

Amazon API Gateway is an AWS service that enables you to create, publish, maintain, monitor, and secure your own REST and Websocket APIs at any scale. You can create robust, secure, and scalable APIs that access AWS or other web services, as well as data stored in the AWS cloud. You can create APIs for use in your own client applications (apps). Or you can make your APIs available to third-party app developers.

**AWS Lambda**

AWS Lambda is a compute service that lets you run code without provisioning or managing servers. AWS Lambda executes your code only when needed and scales automatically, from a few requests per day to thousands per second. You pay only for the compute time you consume — there is no charge when your code is not running. With AWS Lambda, you can run code for virtually any type of application or backend service — all with zero administration. AWS - Lambda runs your code on a high-availability compute infrastructure and performs all of the administration of the compute resources, including server and operating system maintenance, capacity provisioning and automatic scaling, code monitoring and logging. All you need to do is supply your code in one of the languages that AWS lambda supports.

You can use AWS Lambda to run your code in response to events, such as changes to data in an Amazon S3 bucket or an Amazon DynamoDB table; to run your code in response to HTTP requests using Amazon API Gateway; or invoke your code using API calls made using AWS SDKs. With these capabilities, you can use Lambda to easily build data processing triggers for AWS services like Amazon S3 and Amazon DynamoDB, process streaming data stored in Kinesis, or create your own back end that operates at AWS scale, performance, and security.

**AWS DynamoDB**

Amazon DynamoDB is a fully managed NoSQL database service that allows to create database tables that can store and retrieve any amount of data. It automatically manages the data traffic of tables over multiple servers and maintains performance. It also relieves the customers from the burden of operating and scaling a distributed database. Hence, hardware provisioning, setup, configuration, replication, software patching, cluster scaling, etc. is managed by Amazon.

**Iot Temperature Device Example**
So, let’s imagine that we have a raspberry pi with a temperature sensor on our room, and we want to save the data every hour in a database where an android/Ios app will get these information and display to an user. One of the most simplest way is making an HTTP request every hour passing through the request body the temperature we want to save in the database. So let’s first create the dynamodb table where the information will be saved.

**Creating the DynamoDB Table**

This table will have save the temperature of a current device, so we will create three fields(Columns) to this table:

- eventDateTime — The event timestamp
- deviceId — An unique id for the device that is sending the information
- temperature — The current temperature measured by a sensor

So let's create tables like below:

![image](https://user-images.githubusercontent.com/74225291/164957458-e1c216a1-f832-481e-9a06-9a951da1647a.png)

Different from relational databases, we don’t need to create the others table’s columns, we only need to include this column as one of the attributes of the json passed to the lambda function.

<img width="836" alt="image" src="https://user-images.githubusercontent.com/74225291/164957438-43e3cf65-e370-47ea-bf06-76fa84981493.png">

**Creating Lambda Function for POST Request**

Create a role to access dynamoDB first. we will assign that role to the lambda function as execution role.

<img width="1165" alt="image" src="https://user-images.githubusercontent.com/74225291/164957521-393f256f-ffd3-4b5b-815f-63c741be3e2b.png">


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
