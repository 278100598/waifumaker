import json
import re
import boto3

import requests
from bs4 import BeautifulSoup

sqs = boto3.client('sqs', region_name='us-east-1', aws_access_key_id="ASIA2HAW6NDVTA7O7P2A", aws_secret_access_key="ww3uVWxXOe7RlXJ2HDxtP7jcLj9H5Wet9mZc8f6m"
                   ,aws_session_token="FwoGZXIvYXdzEFsaDK4pehBxaMdU1Zx7RyLMAdGuhKuRwh0bE7WNJDC2in9B4UHHBt4GAp0U/sh41CGI93M5YG8rfEP4rRb5IOp2QFDNmrtH2usz2cqcfVhSN0pq4ZoGQ5RxAV8EQuoGP5CcgFDGTfkSRZvkUZfF6V8NCDYwtJ25CtCFIVD+9Vqy+G/hlXhnaH8Be7ocRVKAv+JGrOp37XWvJvmCgSj9MzHoVqVHCQyDHZ1nKtfYOLak/RZz4VLZBttjoGOwnMZOwOX4r41ONlPS0AogfuaGdJ1PdTOjLCWfx0fwO9I6tijh38mrBjItPLJSS4rLJJHlrg5+Gao9L48pJC5KZn0kgixIQT3jVnUteWz6l5zyh0Ybs6oI")
queue_url = 'https://sqs.us-east-1.amazonaws.com/702275283179/firstqueue'

body = {"url": "https://files.yande.re/image/a605c795b12f18f414345a8eac8f23f6/yande.re", "bucket": "waifumakerbucket",
        "file_name": "yandere/furina/s.jpg"}

ret = sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(body))
print(ret)
