import json
import requests
import urllib.parse as urlparse
import boto3
import re


def yandere(message):
    tag = message['tag']

    ret = requests.get(f"https://yande.re/tag.xml?name={tag}&order=count")
    for id, name, count, type, ambiguous in re.findall(
            r'<tag id="(.+?)" name="(.+?)" count="(.+?)" type="(.+?)" ambiguous="(.+?)"/>', ret.text):
        if name == tag:
            sqs = boto3.client('sqs')
            queue_url = 'https://sqs.us-east-1.amazonaws.com/089106211772/firstqueue'

            cnt = 0
            for p in range(1, 3):
                ret = requests.get(f"https://yande.re/post.xml?tags={name}&limit=100&page={p}")
                images = re.findall(r'<post (.+?)/>', ret.text)
                cnt += len(images)
                if len(images) == 0:
                    break

                for image in images:
                    md5 = re.search(r'md5="(.+?)"', image).group(1)
                    jpeg_url = re.search(r'jpeg_url="(.+?)"', image).group(1)
                    preview_url = re.search(r'preview_url="(.+?)"', image).group(1)

                    body = {"type": "yandere", "url": jpeg_url, "bucket": "waifumakerbucket2",
                            "file_name": f"Gallery/yandere/{name}/{md5}.jpg"}
                    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(body))
                    body = {"type": "yandere", "url": preview_url, "bucket": "waifumakerbucket2",
                            "file_name": f"Gallery/yandere/{name}/preview_{md5}.jpg"}
                    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(body))

            print(f"next!!!!!!!!!! {message} total:{cnt}images")
            return


def pixiv(message):
    keyword = message["keyword"]
    order = message["order"]
    mode = message["mode"]
    cookie = message["cookie"]
    ai = message["ai"]

    url = "https://www.pixiv.net/ajax/search/artworks/" + \
          "{}?word={}".format(urlparse.quote(keyword, safe="()"), urlparse.quote(keyword)) + \
          "&order={}".format("popular_d" if order else "date_d") + \
          f"&mode={mode}" + "&p={}&type=all&lang=zh&s_mode=s_tag"
    if not ai:
        url += "&ai_type=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "COOKIE": cookie,
        "Referer": "https://www.pixiv.net/"
    }

    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/089106211772/pixiv_midqueue'

    id_set = []
    for p in range(1, 2):
        ret = requests.get(url.format(p), headers=headers)
        ids = [art["id"] for art in ret.json()["body"]["illustManga"]["data"]]
        for id in ids:
            if id in id_set:
                continue
            id_set.append(id)

            body = {"type": "pixiv", "id": id, "cookie": cookie, "keyword": keyword, "ai": ai, "mode": mode}
            sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(body))

    print(f"next!!!!!!!!!! {keyword} {mode} {ai} total:{len(id_set)}images")
    return


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
