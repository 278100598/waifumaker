import json
import os
import shutil
import re

import boto3
import requests
import tls_client
from flask import Flask,  request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
region_name = 'us-east-1'
aws_access_key_id = "ASIA2HAW6NDV4KAXUCSZ"
aws_secret_access_key = "fvnozi/GUWujI2O+/E9n0HhGqhGCuUi+oHbDQFR3"
aws_session_token = "FwoGZXIvYXdzEI///////////wEaDGSE1SniJhw70eL5iyLMATZ3Ug3k8ktHv7uIm78YHqt7y7TNzbdpTEfQX4dddH60pBGJ2ZVbTXFjubqGOL9TkoBYSjqf/4gMrICB31fZEsxCmv/X7ML3Lm9VCI2I8UYr1D7xTPAHYwQR31UfFn/N6U46c+DajIydmkycffXons/6aqoecE0iRqCb0k1GkpImRxmfY6JF9e6snQJnxbUVcoAQ5l8rZfF4SrtTGoljVzGlcPkKLKC+/zSO/aJLekgNT71b5C2qlJT0ktJZzDvsoh+Jl9EXqe5dXRATmyihmNWrBjItynIn+bA5cv5VL3yEi9utQF5DY3bQPemAZDbjtW0jHGVSv6JkNemMiytpkFO/"


@app.route("/get")
def get():
    URL = request.args.get("URL")
    print(URL)
    res = requests.get(URL)
    return res.content, 200

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
queue_url = 'https://sqs.us-east-1.amazonaws.com/702275283179/zeroqueue'
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
print(len(zh_to_cn))


def get_voice(speaker: str,  text:str, lang:str, length:str=1, noise:str=0.6, noisew:str=0.8):
    url = f"https://v2.genshinvoice.top/run/predict"
    headers = {'Content-Type': 'application/json'}
    data = {
        "data": [
            text,
            speaker,
            0,
            0.2,
            noise,
            noisew,
            length,
            lang,
            None
        ],
        "event_data": None,
        "fn_index": 2,
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
        voice_path = get_voice(SPEAKER,TEXT,LANG)
        url = f"https://v2.genshinvoice.top/file={voice_path}"

        try:
            voice = requests.get(url).content
        except Exception as e:
            VOCIE_CACHE.remove(filename)
            return "", 200

        with open(filename, "wb") as f:
            f.write(voice)
        s3.upload_file(filename, BUCKET, f"Voice/{filename}")
        #os.remove(filename)
        return f"https://v2.genshinvoice.top/file={voice_path}", 200

    return f"https://{BUCKET}.s3.amazonaws.com/Voice/{SPEAKER}_{LANG}_{TEXT}.wav", 200







if __name__ == "__main__":
    app.run(host="0.0.0.0",port=11234, threaded=True, processes=1)