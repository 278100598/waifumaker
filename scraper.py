import os
import re

import requests
import urllib.parse as urlparse

def first_yandere(message):

    res = requests.get(message["url"])

    os.makedirs(os.path.dirname(message["file_name"]), exist_ok=True)
    with open(message["file_name"], "wb") as f:
        f.write(res.content)

    print(message)


def first_pixiv(message):
    cookie = message["cookie"]
    id = message["id"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "COOKIE": cookie,
        "Referer": f"https://www.pixiv.net/{id}"
    }
    res = requests.get(message["url"], headers=headers)

    os.makedirs(os.path.dirname(message["file_name"]), exist_ok=True)
    with open(message["file_name"], "wb") as f:
        f.write(res.content)

    print(id, message["file_name"])




def mid_pixiv(message):
    id = message["id"]
    keyword = message["keyword"]
    mode = message["mode"]
    cookie = message["cookie"]
    ai = message["ai"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "COOKIE": cookie,
        "Referer": f"https://www.pixiv.net/{id}"
    }
    ret = requests.get(f"https://www.pixiv.net/ajax/illust/{id}/pages?lang=zh", headers=headers)

    urlss = [item["urls"] for item in ret.json()["body"]]

    folder_name = keyword + ("" if ai else "_no_ai")

    for index, urls in enumerate(urlss):
        if index == 3:
            break

        original = urls["original"]
        regular = urls["regular"]
        small = urls["small"]

        body = {"type": "pixiv", "url": small, "bucket": "waifumakerbucket2",
                "file_name": f"Gallery/pixiv/{mode}/{folder_name}/preview_{id}_p{index}.{small.split('.')[-1]}",
                "cookie": cookie, "id": id}
        first_pixiv(body)
        body = {"type": "pixiv", "url": regular, "bucket": "waifumakerbucket2",
                "file_name": f"Gallery/pixiv/{mode}/{folder_name}/regular_{id}_p{index}.{original.split('.')[-1]}",
                "cookie": cookie, "id": id}
        first_pixiv(body)


def zero_yandere(message):
    tag = message['tag']

    ret = requests.get(f"https://yande.re/tag.xml?name={tag}&order=count")
    for id, name, count, type, ambiguous in re.findall(
            r'<tag id="(.+?)" name="(.+?)" count="(.+?)" type="(.+?)" ambiguous="(.+?)"/>', ret.text):
        if name == tag:

            cnt = 0
            for p in range(1, 3):
                ret = requests.get(f"https://yande.re/post.xml?tags={name}&limit=100&page={p}")
                images = re.findall(r'<post (.+?)/>', ret.text)
                cnt += len(images)
                if len(images) == 0:
                    break

                for image in images:
                    md5 = re.search(r'md5="(.+?)"', image).group(1)
                    jpeg_url = re.search(r'jpeg_url="(.+?)"', image).group(1)
                    preview_url = re.search(r'preview_url="(.+?)"', image).group(1)

                    body = {"type": "yandere", "url": jpeg_url, "bucket": "waifumakerbucket2",
                            "file_name": f"Gallery/yandere/{name}/{md5}.jpg"}
                    first_yandere(body)
                    body = {"type": "yandere", "url": preview_url, "bucket": "waifumakerbucket2",
                            "file_name": f"Gallery/yandere/{name}/preview_{md5}.jpg"}
                    first_yandere(body)

            print(f"next!!!!!!!!!! {message} total:{cnt}images")
            return


def zero_pixiv(message):
    keyword = message["keyword"]
    order = message["order"]
    mode = message["mode"]
    cookie = message["cookie"]
    ai = message["ai"]

    url = "https://www.pixiv.net/ajax/search/artworks/" + \
          "{}?word={}".format(urlparse.quote(keyword, safe="()"), urlparse.quote(keyword)) + \
          "&order={}".format("popular_d" if order else "date_d") + \
          f"&mode={mode}" + "&p={}&type=all&lang=zh&s_mode=s_tag"
    if not ai:
        url += "&ai_type=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "COOKIE": cookie,
        "Referer": "https://www.pixiv.net/"
    }

    id_set = []
    for p in range(1, 2):
        ret = requests.get(url.format(p), headers=headers)
        ids = [art["id"] for art in ret.json()["body"]["illustManga"]["data"]]
        for id in ids:
            if id in id_set:
                continue
            id_set.append(id)

            body = {"type": "pixiv", "id": id, "cookie": cookie, "keyword": keyword, "ai": ai, "mode": mode}
            mid_pixiv(body)

    print(f"next!!!!!!!!!! {keyword} {mode} {ai} total:{len(id_set)}images")
    return