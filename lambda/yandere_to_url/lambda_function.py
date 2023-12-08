import json
import requests
import boto3
import re


def lambda_handler(event, context):
    for record in event["Records"]:
        message = json.loads(record["body"])
        ret = requests.get(f"https://yande.re/tag.xml?name={message['tag']}&order=count")
        for id, name, count, type, ambiguous in re.findall(
                r'<tag id="(.+?)" name="(.+?)" count="(.+?)" type="(.+?)" ambiguous="(.+?)"/>', ret.text):
            if name == message['tag']:

                sqs = boto3.client('sqs')
                queue_url = 'https://sqs.us-east-1.amazonaws.com/702275283179/firstqueue'

                cnt = 0
                for p in range(1, 10):
                    ret = requests.get(f"https://yande.re/post.xml?tags={name}&limit=100&page={p}")
                    images = re.findall(r'<post (.+?)/>', ret.text)
                    cnt += len(images)
                    if len(images) == 0:
                        break

                    for image in images:
                        md5 = re.search(r'md5="(.+?)"', image).group(1)
                        jpeg_url = re.search(r'jpeg_url="(.+?)"', image).group(1)
                        preview_url = re.search(r'preview_url="(.+?)"', image).group(1)

                        body = {"url": jpeg_url, "bucket": "waifumakerbucket", "file_name": f"yandere/{name}/{md5}.jpg"}
                        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(body))
                        body = {"url": preview_url, "bucket": "waifumakerbucket",
                                "file_name": f"yandere/{name}/preview_{md5}.jpg"}
                        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(body))

                print(f"next!!!!!!!!!! {message} total:{cnt}images")
                return {
                    'statusCode': 200,
                    'body': json.dumps('Hello from Lambda!')
                }


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
