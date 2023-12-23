import json
import boto3
import requests


def yandere(message):
    s3 = boto3.client('s3')

    res = requests.get(message["url"])
    with open("/tmp/tmp.jpg", "wb") as f:
        f.write(res.content)

    s3.upload_file('/tmp/tmp.jpg', message["bucket"], message["file_name"])
    print(message)


def pixiv(message):
    s3 = boto3.client('s3')
    cookie = message["cookie"]
    id = message["id"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "COOKIE": cookie,
        "Referer": f"https://www.pixiv.net/{id}"
    }
    res = requests.get(message["url"], headers=headers)
    with open("/tmp/tmp.jpg", "wb") as f:
        f.write(res.content)

    s3.upload_file('/tmp/tmp.jpg', message["bucket"], message["file_name"])
    print(id, message["bucket"], message["file_name"])


def lambda_handler(event, context):
    for record in event["Records"]:
        message = json.loads(record["body"])
        if message["type"] == "yandere":
            yandere(message)
        elif message["type"] == "pixiv":
            pixiv(message)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
