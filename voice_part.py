import googletrans
import requests
from playsound import playsound


'''
speaker 是指角色的名字(簡體中文字)
nation = {'中配'='ZH','英配'='EN','日配'='JP'}
text 是要角色說的話
lang 是要角色說的話的語言'ZH','EN','JP'，如果混合不同語言的字在同一句話裡的話就只會說指定語言的字
length 語速
noise 感情：控制感情变化和稳定程度
noisew 音素长度：控制音节发音长度变化程度
'''
def get_vocie(speaker: str, nation: str,  text:str, lang:str, length:str=1, noise:str=0.6, noisew:str=0.8):
    url = f"https://v2.genshinvoice.top/run/predict"
    data = {
        "data": [
            text,
            speaker,
            0,
            0.2,
            0.6,
            0.8,
            1,
            "ZH",
            None
        ],
        "event_data": None,
        "fn_index": 2,
    }

    res = requests.get(url=url,timeout=len(text)/10)
    print(res.text)
    with open("save.wav","wb") as f:
        f.write(res.content)
txt = "Hmm... So you're that Traveler everyone seems to speak about these days, no? | I wonder what kind of surprise you may bring to Fontaine... "
get_vocie("芙宁娜","EN",txt,lang="EN")
#playsound("save.wav")

# unknown_sentence = 'おはよう'
# translator = googletrans.Translator()
# results = translator.detect(unknown_sentence)
# print(results)
# print('Japanese:', translator.translate('我覺得今天天氣不好', dest='ja').text)
"今日は天気が悪いみたいです"
"""
with open("all_character.txt", "r", encoding='UTF-8') as f:
    line = f.read()
    names = re.findall(r'<option value="(.+?)">', line)

    with open("zh-cn_and_zh-tw.txt", "w", encoding='UTF-8') as f:
        for zh_cn in sorted(list(set(names))):
            zh_tw = convert(zh_cn, 'zh-tw')
            f.write(f'{zh_cn} {zh_tw}\n')
"""
