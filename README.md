# Basic S3 API

This API uses the Serverless platform to interact with images in an S3 bucket and list all objects in the same bucket.
By launching with `sls deploy` Serverless sets up everything needed between AWS LAmbda and AWS API Gateway, and will list
the endpoints for your functions after deploying.

```
getimage
```
This function will use Serverless, AWS LAmbda and AWS API Gateway to get the image from an S3 bucket using a GET request. 
It will return a string of base64 code (via the browser) which can be used in any free online converter to show the image.

```
uploadimage
```
This function will use Serverless, AWS Lambda, and AWS API Gateway to upload an image to an S3 bucket using a POST request.
The function accepts one arguement: img64 (the base64 code string that codes for an image). The imagename you want it to have
will be entered into the API endpoint directly. Can use any online image to base64 coverter to get the base64 code, then can
use POSTMAN to input RAW data as a JSON onject with no spaces/indents/new lines.

```
deleteimage
```
Function uses a DELETE request to delete an image from an S3 bucket via API Gateway.

```
listobjects
```
Function uses a GET request from the images path to get a list of all objects in an S3 bucket via API Gateway.


Thank you for checking out this API!