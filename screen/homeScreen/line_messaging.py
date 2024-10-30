import requests
from linebot import LineBotApi
from linebot.models import TextMessage


def sendLateMessage(pill_data, timeWillTake, config):
    pill_name = pill_data['name']
    pill_amount_pertime = pill_data['pillsPerTime']
    text = f'นาย {config["username"]} ลืมทานยา {pill_name} จำนวน {pill_amount_pertime} เม็ด เวลา {timeWillTake}'
    print(text)
    
    # line_bot_api = LineBotApi(config['botAccessToken'])
    # line_bot_api.push_message(config['lineId'], TextMessage(text=text))
    
    # ตรวจสอบ userId
    if not config['userId']:
        print("Error: userId is missing or invalid.")
        return
    # print(f'Sending message to userId: {config["username"]}, message: {text}')

    res = requests.post(config["url"] + "/user/addHistory", json={
        "task": "forget",
        "userID": config["userId"],
        "medicine": str(pill_data["pillId"]),
    })
    
    # print(str(pill_data["channelId"]))
    print('Forgot to take pill')


def sendLineMessage(pill_data, timeWillTake, config):
    # print(timeWillTake)
    pill_name = pill_data['name']
    pill_amount_pertime = pill_data['pillsPerTime']
    inMinute = timeWillTake.split(':')[1]
    if inMinute.startswith('0'):
        # print(inMinute)
        inMinute = inMinute[1]
    text = f'นาย {config["username"]} มียาต้องทานชื่อ {pill_name} จำนวน {pill_amount_pertime} เม็ด ในอีก {inMinute} นาที'
    print(text)
    # line_bot_api = LineBotApi(config['botAccessToken'])
    # line_bot_api.push_message(config['lineId'], TextMessage(text=text))
    
    # ตรวจสอบ userId
    if not config['userId']:
        print("Error: userId is missing or invalid.")
        return
    # print(f'Sending message to userId: {config["userId"]}, message: {text}')
    
    res = requests.post(config["url"] + "/user/addHistory", json={
            "task": "alert",
            "userID": config["userId"],
            "medicine": str(pill_data["pillId"]),
            })
    # print(f'res : {res}')
    print('Time to take pill')
    
