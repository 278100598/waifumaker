import requests


IP = "44.221.144.31"
#IP = "127.0.0.1"
url = f"http://{IP}:11234/set_aws"
headers = {'Content-Type': 'application/json'}

aws_access_key_id = "ASIAWBH7HEWQDDQPPRWM"
aws_secret_access_key = "raqHXucZ+fcTdTdqnq95DYuVhqSbi55NwPVdhwnP"
aws_session_token = "FwoGZXIvYXdzEPL//////////wEaDGsTvlZOnU6TbIbeDyLIATRGF/G04mgh/fbPOY7QLLaHyZhVl7UnEWuhQxMIJgMcq/VLGn68H0PZYGt6OWt+DFm2+8xcS8vgorKp6P5V87nXWnFi5Od7jrI6vXQ/ieZ6XBRvBzpy+o8bM1aYhO4emXL5lfXY5djxbLKW3mmj+2LBiJEX+vdzOKzd3Ou1kHoLm7unXyo1jirshg5UqncqspeomLvd/erMlwUtTuRYH2nVh5eJU0jT9hmktgBY547z0HfO1hpNzdIRCzhnsY8fncfAqE7mWdoyKJ3x6qsGMi0d3rvNI0rlt895wuiMu/OnKePFKODJQv2FsKUZ8SY6MHHCISyAIUI4ArxxsB4="

payload = {
    "aws_access_key_id": aws_access_key_id,
    "aws_secret_access_key": aws_secret_access_key,
    "aws_session_token": aws_session_token,
}

ret = requests.post(url,headers=headers,json=payload)
print(ret)