import json
import re
import boto3

import requests
from bs4 import BeautifulSoup
from scraper import zero_pixiv

cookie = "first_visit_datetime_pc=2023-12-06%2002%3A30%3A04; yuid_b=I1NGCUA; p_ab_id=7; p_ab_id_2=2; p_ab_d_id=1213741604; PHPSESSID=35673257_oZsuLoF9gGbrzhcbhIMauGAPVO5KWLUs; device_token=51387302cc6ac444401fd5bdef37363e; _ga_MZ1NL4PHH0=GS1.1.1701797514.1.1.1701797526.0.0.0; c_type=32; privacy_policy_agreement=0; privacy_policy_notification=0; a_type=0; b_type=1; cf_clearance=qq.P0AJR37AVvyZwStlMmXuapzLcw1PlZGq0g9sUAyE-1703248618-0-2-c09965ff.36ccb9e3.d8889a89-0.2.1703248618; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.372031141.1703248627; __cf_bm=6rG_kJ3AqLe8yEYNvUpQdSidjBvUvOCeMes2AoZrJtA-1703250749-1-AS1ToRVIMXCAcD42PRVZZXsEqQIcmmmrRd70JyCC09h3j2lFytivpoH5XwILXKJ3+r/zyFaXZYvM6MscmCYNdZhU/dSQHwCHIBT9p+g53dzB; _ga=GA1.1.387688919.1701797405; _ga_75BBYNYN9J=GS1.1.1703248617.2.1.1703251821.0.0.0"

zero_pixiv({"type": "pixiv", "cookie": cookie, "keyword": "鳴瀬しろは", "order": True, "mode": "safe", "ai": True})

"""
region_name = 'us-east-1'
aws_access_key_id = "ASIARJPZE4O6LH4PV6WN"
aws_secret_access_key = "cfrzGG5a6pcao0EbSsJnZSzws3Oari6aPZFaJaAo"
aws_session_token = "FwoGZXIvYXdzEMf//////////wEaDOALLt4/Yjo7jxubHSLIAdQ7qDNWlTxDSGOyeY3yZlaMnsDTw4kyh30A9SPXavUb9jyf16+5rAaqehpFaOxO7ovygB0eAAtGce2LYMoqh1muZBkl6lzsYpXVhb32ZzxmAc9cVaJcrUwrpMwawofmL0Hz6fU188Xo0oPLkjCDXM4CB4CWaMCW8LqNDP1OiUqUK8rtAoVy41abpTuv3a+Lvfnb4yaKzqSD0/M8x6oCh3omhpOEAPkkkcq3ZLgzxcqoGL718yODKdEeA5y1rQ7h1CzIz3fmgGLmKOzjmawGMi0q7b62Znr1ZrLxzVMWoWaXYBdfangpBDpOTtNS51ieqXK5zWl93v99pCnERzI="

s3 = boto3.client('s3', region_name=region_name, aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
sqs = boto3.client('sqs', region_name=region_name, aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

queue_url = 'https://sqs.us-east-1.amazonaws.com/089106211772/zeroqueue'
cookie = "first_visit_datetime_pc=2023-12-06%2002%3A30%3A04; yuid_b=I1NGCUA; p_ab_id=7; p_ab_id_2=2; p_ab_d_id=1213741604; PHPSESSID=35673257_oZsuLoF9gGbrzhcbhIMauGAPVO5KWLUs; device_token=51387302cc6ac444401fd5bdef37363e; _ga_MZ1NL4PHH0=GS1.1.1701797514.1.1.1701797526.0.0.0; c_type=32; privacy_policy_agreement=0; privacy_policy_notification=0; a_type=0; b_type=1; cf_clearance=qq.P0AJR37AVvyZwStlMmXuapzLcw1PlZGq0g9sUAyE-1703248618-0-2-c09965ff.36ccb9e3.d8889a89-0.2.1703248618; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.372031141.1703248627; __cf_bm=6rG_kJ3AqLe8yEYNvUpQdSidjBvUvOCeMes2AoZrJtA-1703250749-1-AS1ToRVIMXCAcD42PRVZZXsEqQIcmmmrRd70JyCC09h3j2lFytivpoH5XwILXKJ3+r/zyFaXZYvM6MscmCYNdZhU/dSQHwCHIBT9p+g53dzB; _ga=GA1.1.387688919.1701797405; _ga_75BBYNYN9J=GS1.1.1703248617.2.1.1703251821.0.0.0"

body = {"type": "pixiv", "cookie": cookie, "keyword": "鳴瀬しろは", "order": True, "mode": "safe", "ai": True}
# ret = s3.list_objects(Bucket="waifumakerbucket1",Prefix="aa/",Delimiter='/')
# print(json.dumps(ret,indent=1, default=str))
print(json.dumps(body).replace('"','\\"'))
ret = sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(body))
print(ret)
"""