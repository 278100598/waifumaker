import urllib.request

import requests
from bs4 import BeautifulSoup

res = requests.get("https://yande.re/post.xml?tags=furina&page=1")
print(res.content)
soup = BeautifulSoup(res.content, 'xml')
ls = soup.find_all('post')
print(ls[0])