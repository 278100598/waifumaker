import json
import boto3
import requests


def lambda_handler(event, context):
    s3 = boto3.client('s3')

    for record in event["Records"]:
        message = json.loads(record["body"])
        res = requests.get(message["url"])
        with open("/tmp/tmp.jpg", "wb") as f:
            f.write(res.content)

        s3.upload_file('/tmp/tmp.jpg', message["bucket"], message["file_name"])
        print(message)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
