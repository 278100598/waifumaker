import characterai
import requests
import tls_client

token = "579aa6cc6e6096637499c0e89e2e3ab0b2142d25"

from characterai import PyCAI

client = PyCAI(token)

#char = input('Enter CHAR: ')
char = "al66ie2MAHSMunfxBvlU60_hPHSguDbInquKKu2e2XY"

chat = client.chat.get_chat(char)

participants = chat['participants']
session = tls_client.Session(
    client_identifier='chrome112'
)
headers = {
    'Authorization': f'Token {token}'
}
res = session.get(f"https://beta.character.ai/chat/history/msgs/user/?history_external_id=AZShptBkU6PsDKU_gehdpgMOtkLMWY90C_7G8m-r6xE",headers=headers)
print(res.json())
#client.chat.get_histories(char,number=1)
exit()

if not participants[0]['is_human']:
    tgt = participants[0]['user']['username']
else:
    tgt = participants[1]['user']['username']

while True:
    message = input('You: ')

    data = client.chat.send_message(
        chat['external_id'], tgt, message
    )

    name = data['src_char']['participant']['name']
    text = data['replies'][0]['text']

    print(f"{name}: {text}")

