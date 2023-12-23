import requests


IP = "44.221.144.31"
IP = "127.0.0.1"
url = f"http://{IP}:11234/set_aws"
headers = {'Content-Type': 'application/json'}

aws_access_key_id = "ASIARJPZE4O6LH4PV6WN"
aws_secret_access_key = "cfrzGG5a6pcao0EbSsJnZSzws3Oari6aPZFaJaAo"
aws_session_token = "FwoGZXIvYXdzEMf//////////wEaDOALLt4/Yjo7jxubHSLIAdQ7qDNWlTxDSGOyeY3yZlaMnsDTw4kyh30A9SPXavUb9jyf16+5rAaqehpFaOxO7ovygB0eAAtGce2LYMoqh1muZBkl6lzsYpXVhb32ZzxmAc9cVaJcrUwrpMwawofmL0Hz6fU188Xo0oPLkjCDXM4CB4CWaMCW8LqNDP1OiUqUK8rtAoVy41abpTuv3a+Lvfnb4yaKzqSD0/M8x6oCh3omhpOEAPkkkcq3ZLgzxcqoGL718yODKdEeA5y1rQ7h1CzIz3fmgGLmKOzjmawGMi0q7b62Znr1ZrLxzVMWoWaXYBdfangpBDpOTtNS51ieqXK5zWl93v99pCnERzI="

payload = {
    "aws_access_key_id": aws_access_key_id,
    "aws_secret_access_key": aws_secret_access_key,
    "aws_session_token": aws_session_token,
}

ret = requests.post(url,headers=headers,json=payload)
print(ret)