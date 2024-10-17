import requests
from linebot import LineBotApi
from linebot.models import TextMessage


def sendLateMessage(pill_data, timeWillTake, config):
    pill_name = pill_data['name']
    pill_amount_pertime = pill_data['pillsPerTime']
    text = f'ผู้สูงอายุลืมทานยา {pill_name} จำนวน {pill_amount_pertime} เม็ด เวลา {timeWillTake}'
    line_bot_api = LineBotApi(config['botAccessToken'])
    line_bot_api.push_message(config['userId'], TextMessage(text=text))
    res = requests.post(config["url"] + "/user/addHistory", json={
            "channelID": str(pill_data["channelId"]),
            "lineUID": config["userId"],
            "task": "Forgot to take pill"
            })
    print(str(pill_data["id"]))
    print(f'res {res}')
    print('Forgot to take pill')

def sendLineMessage(pill_data, timeWillTake, config):
    print(timeWillTake)
    pill_name = pill_data['name']
    pill_amount_pertime = pill_data['pillsPerTime']
    inMinute = timeWillTake.split(':')[1]
    if inMinute.startswith('0'):
        print(inMinute)
        inMinute = inMinute[1]
    text = f'ผู้สูงอายุมียาต้องทานในอีก {inMinute} นาที'
    line_bot_api = LineBotApi(config['botAccessToken'])
    line_bot_api.push_message(config['userId'], TextMessage(text=text))
    res = requests.post(config["url"] + "/user/addHistory", json={
            "task": "Take pill remider",
            "userID": config["userId"],
            "medicine": str(pill_data["pillId"]),
            })
    print(f'res : {res}')