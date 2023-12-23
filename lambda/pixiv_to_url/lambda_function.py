import json
import requests
import boto3


def pixiv(message):
    id = message["id"]
    keyword = message["keyword"]
    mode = message["mode"]
    cookie = message["cookie"]
    ai = message["ai"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "COOKIE": cookie,
        "Referer": f"https://www.pixiv.net/{id}"
    }
    ret = requests.get(f"https://www.pixiv.net/ajax/illust/{id}/pages?lang=zh", headers=headers)

    urlss = [item["urls"] for item in ret.json()["body"]]

    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/089106211772/firstqueue'

    folder_name = keyword + ("" if ai else "_no_ai")

    for index, urls in enumerate(urlss):
        if index == 3:
            break

        original = urls["original"]
        regular = urls["regular"]
        small = urls["small"]

        body = {"type": "pixiv", "url": small, "bucket": "waifumakerbucket2",
                "file_name": f"Gallery/pixiv/{mode}/{folder_name}/preview_{id}_p{index}.{small.split('.')[-1]}",
                "cookie": cookie, "id": id}
        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(body))
        body = {"type": "pixiv", "url": original, "bucket": "waifumakerbucket2",
                "file_name": f"Gallery/pixiv/{mode}/{folder_name}/original_{id}_p{index}.{original.split('.')[-1]}",
                "cookie": cookie, "id": id}
        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(body))


def lambda_handler(event, context):
    for record in event["Records"]:
        message = json.loads(record["body"])
        if message["type"] == "pixiv":
            pixiv(message)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
