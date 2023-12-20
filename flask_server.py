import json
import os
import shutil
import re
from threading import Thread

import boto3
import requests
import tls_client
from flask import Flask,  request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
region_name = 'us-east-1'
aws_access_key_id = None
aws_secret_access_key = None
aws_session_token = None
queue_url = 'https://sqs.us-east-1.amazonaws.com/414999586208/zeroqueue'

@app.post("/set_aws")
def set_aws():
    j = request.json
    global aws_access_key_id, aws_secret_access_key, aws_session_token
    aws_access_key_id = j["aws_access_key_id"]
    aws_secret_access_key = j["aws_secret_access_key"]
    aws_session_token = j["aws_session_token"]
    global s3, sqs
    s3 = boto3.client('s3', region_name=region_name, aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
    sqs = boto3.client('sqs', region_name=region_name, aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
    return "success", 200

@app.get("/get")
def get():
    URL = request.args.get("URL")
    print(URL)
    res = requests.get(URL)
    return res.content, 200

@app.get("/get/voice_list")
def get_voice_list():
    ret = []
    with open("zh-cn_and_zh-tw.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            ret.append(line.strip().split(' ')[1])
    return ret, 200

session = tls_client.Session(
    client_identifier='chrome112'
)


@app.get("/get/with_token")
def get_with_token():
    URL = request.args.get("URL")
    TOKEN = request.args.get("TOKEN")
    headers = {'Authorization': f'Token {TOKEN}'}
    res = session.get(URL,headers=headers)
    try:
        print(json.dumps(res.json(), indent=1))
    except Exception as e:
        print(res.text)
        pass

    return res.content, 200

@app.post("/post/with_token")
def post_with_token():
    j = request.json
    URL = request.args.get("URL")
    TOKEN = request.args.get("TOKEN")
    headers = {'Authorization': f'Token {TOKEN}', 'Content-Type': 'application/json'}
    res = session.post(URL,headers=headers,json=j)
    try:
        print(json.dumps(res.json(), indent=1))
    except Exception as e:
        pass

    return res.content, 200

s3 = boto3.client('s3', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,aws_session_token=aws_session_token)
@app.get("/get/s3_list")
def get_s3_list():
    BUCKET = request.args.get("BUCKET")
    PREFIX = request.args.get("PREFIX")
    res = s3.list_objects(Bucket=BUCKET, Prefix=PREFIX, Delimiter='/')
    ret = []
    if "CommonPrefixes" in res:
        for x in res["CommonPrefixes"]:
            ret.append(x["Prefix"])
    elif "Contents" in res:
        for x in res["Contents"]:
            ret.append(x["Key"])
    return ret, 200

sqs = boto3.client('sqs', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,aws_session_token=aws_session_token)

CACHE = set()
@app.get("/get/sqs")
def get_sqs():
    TAG = request.args.get("TAG")
    if TAG not in CACHE:
        CACHE.add(TAG)
        ret = sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps({"tag": TAG}))
        print(ret)
        return ret, 200
    else:
        print(f"{TAG} have been searched")
        return f"{TAG} have been searched", 418


VOCIE_CACHE = set()
zh_to_cn = dict()
with open("zh-cn_and_zh-tw.txt","r",encoding="utf-8") as f:
    for line in f.readlines():
        two = line.strip().split(' ')
        zh_to_cn[two[1]] = two[0]


def get_voice(speaker: str,  text:str, lang:str, length:str=1, noise:str=0.6, noisew:str=0.8):
    url = f"https://v2.genshinvoice.top/run/predict"
    headers = {'Content-Type': 'application/json'}
    data = {
        "data": [
            text,
            speaker,
            0.2,
            noise,
            noisew,
            length,
            lang,
            None,
            "Happy",
            "Text prompt",
        ],
        "event_data": None,
        "fn_index": 0,
    }

    res = requests.post(url=url, json=data, headers=headers)
    print(res.text)
    return res.json()["data"][1]["name"]

@app.post("/post/vocie")
def post_voice():
    j = request.json
    BUCKET = j["BUCKET"]
    SPEAKER = zh_to_cn[j["SPEAKER"]]
    LANG = j["LANG"]
    TEXT = re.sub(r'[\'"!@#$?<>*\\/|:.]', '', j["TEXT"])
    filename = f"{SPEAKER}_{LANG}_{TEXT}.wav"
    if filename not in VOCIE_CACHE:
        VOCIE_CACHE.add(filename)

        try:
            voice_path = get_voice(SPEAKER,TEXT,LANG)
        except Exception as e:
            VOCIE_CACHE.remove(filename)
            return "", 200

        url = f"https://v2.genshinvoice.top/file={voice_path}"
        voice = requests.get(url).content
        with open(filename, "wb") as f:
            f.write(voice)
        Thread(target=lambda: {
            s3.upload_file(filename, BUCKET, f"Voice/{filename}"),
            os.remove(filename)
        }, daemon=True).start()
        return f"https://v2.genshinvoice.top/file={voice_path}", 200

    return f"https://{BUCKET}.s3.amazonaws.com/Voice/{SPEAKER}_{LANG}_{TEXT}.wav", 200



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=11234, threaded=True, processes=1)