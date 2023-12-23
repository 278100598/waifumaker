import json

import requests
from bs4 import BeautifulSoup
import urllib.parse as urlparse
from typing import List

keyword = "FGO"
order = True
mode = "r18"

def search_id(keyword, order, mode, ai:bool=True) -> List[str]:
    url = "https://www.pixiv.net/ajax/search/artworks/" + \
                "{}?word={}".format(urlparse.quote(keyword, safe="()"), urlparse.quote(keyword)) + \
                "&order={}".format("popular_d" if order else "date_d") + \
                f"&mode={mode}" + "&p=1&type=all&lang=zh&s_mode=s_tag"
    if not ai:
        url += "&ai_type=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "COOKIE": "first_visit_datetime_pc=2023-12-06%2002%3A30%3A04; yuid_b=I1NGCUA; p_ab_id=7; p_ab_id_2=2; p_ab_d_id=1213741604; PHPSESSID=35673257_oZsuLoF9gGbrzhcbhIMauGAPVO5KWLUs; device_token=51387302cc6ac444401fd5bdef37363e; _ga_MZ1NL4PHH0=GS1.1.1701797514.1.1.1701797526.0.0.0; c_type=32; privacy_policy_agreement=0; privacy_policy_notification=0; a_type=0; b_type=1; cf_clearance=qq.P0AJR37AVvyZwStlMmXuapzLcw1PlZGq0g9sUAyE-1703248618-0-2-c09965ff.36ccb9e3.d8889a89-0.2.1703248618; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.372031141.1703248627; __cf_bm=6rG_kJ3AqLe8yEYNvUpQdSidjBvUvOCeMes2AoZrJtA-1703250749-1-AS1ToRVIMXCAcD42PRVZZXsEqQIcmmmrRd70JyCC09h3j2lFytivpoH5XwILXKJ3+r/zyFaXZYvM6MscmCYNdZhU/dSQHwCHIBT9p+g53dzB; _ga=GA1.1.387688919.1701797405; _ga_75BBYNYN9J=GS1.1.1703248617.2.1.1703251821.0.0.0",
        "Referer": "https://www.pixiv.net/"
    }
    ret = requests.get(url, headers=headers)
    return [art["id"] for art in ret.json()["body"]["illustManga"]["data"]]

def get_urls(illust_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "COOKIE": "first_visit_datetime_pc=2023-12-06%2002%3A30%3A04; yuid_b=I1NGCUA; p_ab_id=7; p_ab_id_2=2; p_ab_d_id=1213741604; PHPSESSID=35673257_oZsuLoF9gGbrzhcbhIMauGAPVO5KWLUs; device_token=51387302cc6ac444401fd5bdef37363e; _ga_MZ1NL4PHH0=GS1.1.1701797514.1.1.1701797526.0.0.0; c_type=32; privacy_policy_agreement=0; privacy_policy_notification=0; a_type=0; b_type=1; cf_clearance=qq.P0AJR37AVvyZwStlMmXuapzLcw1PlZGq0g9sUAyE-1703248618-0-2-c09965ff.36ccb9e3.d8889a89-0.2.1703248618; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.372031141.1703248627; __cf_bm=6rG_kJ3AqLe8yEYNvUpQdSidjBvUvOCeMes2AoZrJtA-1703250749-1-AS1ToRVIMXCAcD42PRVZZXsEqQIcmmmrRd70JyCC09h3j2lFytivpoH5XwILXKJ3+r/zyFaXZYvM6MscmCYNdZhU/dSQHwCHIBT9p+g53dzB; _ga=GA1.1.387688919.1701797405; _ga_75BBYNYN9J=GS1.1.1703248617.2.1.1703251821.0.0.0",
        "Referer": f"https://www.pixiv.net/{illust_id}"
    }
    ret = requests.get(f"https://www.pixiv.net/ajax/illust/{illust_id}/pages?lang=zh",headers=headers)

    return [urls["urls"] for urls in ret.json()["body"]]

def download_img(illust_id, url, path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "COOKIE": "first_visit_datetime_pc=2023-12-06%2002%3A30%3A04; yuid_b=I1NGCUA; p_ab_id=7; p_ab_id_2=2; p_ab_d_id=1213741604; PHPSESSID=35673257_oZsuLoF9gGbrzhcbhIMauGAPVO5KWLUs; device_token=51387302cc6ac444401fd5bdef37363e; _ga_MZ1NL4PHH0=GS1.1.1701797514.1.1.1701797526.0.0.0; c_type=32; privacy_policy_agreement=0; privacy_policy_notification=0; a_type=0; b_type=1; cf_clearance=qq.P0AJR37AVvyZwStlMmXuapzLcw1PlZGq0g9sUAyE-1703248618-0-2-c09965ff.36ccb9e3.d8889a89-0.2.1703248618; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.372031141.1703248627; __cf_bm=6rG_kJ3AqLe8yEYNvUpQdSidjBvUvOCeMes2AoZrJtA-1703250749-1-AS1ToRVIMXCAcD42PRVZZXsEqQIcmmmrRd70JyCC09h3j2lFytivpoH5XwILXKJ3+r/zyFaXZYvM6MscmCYNdZhU/dSQHwCHIBT9p+g53dzB; _ga=GA1.1.387688919.1701797405; _ga_75BBYNYN9J=GS1.1.1703248617.2.1.1703251821.0.0.0",
        "Referer": f"https://www.pixiv.net/{illust_id}"
    }
    ret = requests.get(url,headers=headers)
    with open(path, "wb") as f:
        f.write(ret.content)

cookie = "first_visit_datetime_pc=2023-12-06%2002%3A30%3A04; yuid_b=I1NGCUA; p_ab_id=7; p_ab_id_2=2; p_ab_d_id=1213741604; PHPSESSID=35673257_oZsuLoF9gGbrzhcbhIMauGAPVO5KWLUs; device_token=51387302cc6ac444401fd5bdef37363e; _ga_MZ1NL4PHH0=GS1.1.1701797514.1.1.1701797526.0.0.0; c_type=32; privacy_policy_agreement=0; privacy_policy_notification=0; a_type=0; b_type=1; cf_clearance=qq.P0AJR37AVvyZwStlMmXuapzLcw1PlZGq0g9sUAyE-1703248618-0-2-c09965ff.36ccb9e3.d8889a89-0.2.1703248618; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.372031141.1703248627; __cf_bm=6rG_kJ3AqLe8yEYNvUpQdSidjBvUvOCeMes2AoZrJtA-1703250749-1-AS1ToRVIMXCAcD42PRVZZXsEqQIcmmmrRd70JyCC09h3j2lFytivpoH5XwILXKJ3+r/zyFaXZYvM6MscmCYNdZhU/dSQHwCHIBT9p+g53dzB; _ga=GA1.1.387688919.1701797405; _ga_75BBYNYN9J=GS1.1.1703248617.2.1.1703251821.0.0.0"


x = {
    "type": "pixiv",
    "cookie": cookie,
    "id": 114428040,
    "mode": "xxx",
    "ai": False,
    "keyword": "keyword"
}

urls = get_urls("105316714")
print(urls)

exit()

ret = requests.get("https://www.pixiv.net/artworks/114338282")
bs = BeautifulSoup(ret.text,'lxml')

content = bs.find("meta",id="meta-preload-data").get("content")

j = json.loads(content)
print(json.dumps(j,ensure_ascii=False , indent=2))

print(j["illust"]["114338282"]["urls"].keys())



exit()

headers = {
    "Referer": "https://www.pixiv.net/"
}
ret = requests.get("https://i.pximg.net/c/250x250_80_a2/custom-thumb/img/2023/12/18/20/07/34/114338282_p0_custom1200.jpg",
                   headers=headers)
print(len(ret.content))