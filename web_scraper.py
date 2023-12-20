import json
import re
import boto3

import requests
from bs4 import BeautifulSoup

ret = requests.get("https://yande.re/post.xml?tags=hatsune_miku&limit=100&page=2")
x = re.findall(r"md5=\"(.+?)\"",ret.text)
print(len(set(x)))

exit()

region_name = 'us-east-1'
aws_access_key_id = "ASIA2HAW6NDV4KAXUCSZ"
aws_secret_access_key = "fvnozi/GUWujI2O+/E9n0HhGqhGCuUi+oHbDQFR3"
aws_session_token = "FwoGZXIvYXdzEI///////////wEaDGSE1SniJhw70eL5iyLMATZ3Ug3k8ktHv7uIm78YHqt7y7TNzbdpTEfQX4dddH60pBGJ2ZVbTXFjubqGOL9TkoBYSjqf/4gMrICB31fZEsxCmv/X7ML3Lm9VCI2I8UYr1D7xTPAHYwQR31UfFn/N6U46c+DajIydmkycffXons/6aqoecE0iRqCb0k1GkpImRxmfY6JF9e6snQJnxbUVcoAQ5l8rZfF4SrtTGoljVzGlcPkKLKC+/zSO/aJLekgNT71b5C2qlJT0ktJZzDvsoh+Jl9EXqe5dXRATmyihmNWrBjItynIn+bA5cv5VL3yEi9utQF5DY3bQPemAZDbjtW0jHGVSv6JkNemMiytpkFO/"


s3 = boto3.client('s3', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,aws_session_token=aws_session_token)

queue_url = 'https://sqs.us-east-1.amazonaws.com/702275283179/firstqueue'

body = {"url": "https://files.yande.re/image/a605c795b12f18f414345a8eac8f23f6/yande.re", "bucket": "waifumakerbucket",
        "file_name": "yandere/furina/s.jpg"}
ret = s3.list_objects(Bucket="waifumakerbucket",Prefix="aa/",Delimiter='/')
print(json.dumps(ret,indent=1, default=str))
#ret = sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(body))
