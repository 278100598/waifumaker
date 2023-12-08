import re
import urllib.request

import requests
from bs4 import BeautifulSoup






res = requests.get("https://yande.re/post.xml?tags=furina&page=1&limit=4")
#print(re.findall(r'file_ext="(.+?)".*file_url="(.+?)".*sample_url="(.+?)"',res.text))
print(res.text)
print(re.search(r'file_ext="(.+?)"',res.text).group(1))
soup = BeautifulSoup(res.content, 'xml')
ls = soup.find_all('post')
#print(ls[0])