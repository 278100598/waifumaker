FROM python:3.9

WORKDIR /app

RUN pip install boto3 tls_client flask flask_cors requests

COPY flask_server.py /app/flask_server.py
COPY zh-cn_and_zh-tw.txt /app/zh-cn_and_zh-tw.txt

CMD [ "python", "flask_server.py" ]