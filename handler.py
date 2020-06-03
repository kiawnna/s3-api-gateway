import json
import boto3
import base64
from botocore.exceptions import ClientError
import os

BUCKET = os.environ['BUCKET']

# Function uses a GET request to get an image from an S3 bucket via API Gateway and returns a string of base64 code
# (when requested through the browser).


def handler(event, context):
    try:
        key = event["pathParameters"]["imagename"]

        if not any([key.endswith('.png'), key.endswith('.jpeg'), key.endswith('.jpg'), key.endswith('.PNG'), key.endswith('.JPEG'), key.endswith('.JPG')]):
            return {
                "statusCode": 403,
                "body": "Access denied. Please search for either .png or .jpeg images only."
            }

        s3 = boto3.resource('s3')
        obj = s3.Object(
            bucket_name=BUCKET,
            key=key
        )

        return {
            "isBase64Encoded": True,
            "statusCode": 200,
            "body": json.dumps(base64.b64encode(obj.get()['Body'].read()).decode()),
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "AccessDenied":
            return {
                "statusCode": 404,
                "body": "Image not found."
            }
            
# Function uses a POST request to upload an image into an S3 bucket given two events: img64 (the base64 code string
# that codes for an image) and ImageName (the name of the image you want uploaded). Can use any online image to base64
# converter to get the base64 code, then can use POSTMAN to input RAW data as a JSON object with no
# spaces/indents/new lines.


def handler1(event, context):
    print(event)
    key = event["pathParameters"]["imagename"]  # assign a name to your image and pass it through your API path.
    body = json.loads(event["body"])            # sets the variable 'body', turns the json string into a python object.
    s3 = boto3.resource(u's3')                  # invokes the 'resource' method and passes in the service name s3.
    bucket = s3.Bucket(u'kia-random-storage')   # names the bucket you want your image uploaded to.
    path_test = '/tmp/output'                   # temp path in lambda                    
    data = body["img64"]                        # assign base64 of an image to data variable 
    data1 = data                                # assigns data to a new variable, data1
    img = base64.b64decode(data1)               # decode the encoded image data (base64) and saves it as img
    
    with open(path_test, 'wb') as data:
        data.write(img)
        bucket.upload_file(path_test, key)      # Upload image directly inside bucket OR can use below line.
        # bucket.upload_file(path_test, 'FOLDERNAME-IN-YOUR-BUCKET /{}'.format(key))
        # Uploads image inside folder of your s3 bucket.

    return {
        "isBase64Encoded": True,
        'statusCode': 200, 
        'body': 'Image Uploaded'
    }

# Function uses a DELETE request to delete an image from an S3 bucket via API Gateway.


def handler2(event, context):
    try:
        key = event["pathParameters"]["imagename"]
        s3 = boto3.resource('s3')
        obj = s3.Object(
            bucket_name=BUCKET,
            key=key
        )
        obj.delete()
            
        return {
            'isBase64Encoded' : True,
            'statusCode': 200, 
            'body': 'Image Deleted'
        }
   
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "AccessDenied":
            return {
                "statusCode": 404,
                "body": "Image not found."
            }

# Function uses a GET request from the images path to get a list of all objects in an S3 bucket via API Gateway.


def handler3(event, context):
    try:
        s3 = boto3.client('s3')
        response = s3.list_objects(Bucket=BUCKET)

        return {
            "isBase64Encoded": True,
            "statusCode": 200,
            "body": json.dumps(response['Contents'], default=str)
        }

    except ClientError as e:
        print(e)
        error_code = e.response["Error"]["Code"]
        if error_code == "AccessDenied":
            return {
                "statusCode": 404,
                "body": "Bucket empty."
            }