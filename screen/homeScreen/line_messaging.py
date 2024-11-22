from datetime import datetime

import requests
from linebot import LineBotApi
from linebot.models import TextMessage


def sendLineMessage(pill_data, time, config):
    """
    Send Line notification for pill taking
    """
    # ตรวจสอบคีย์ 'name' และ 'pillsPerTime' ใน pill_data
    pill_name = pill_data.get('name', 'ไม่ทราบชื่อยา')
    pill_amount_pertime = pill_data.get('pillsPerTime', 1)
    print('time', time)
    
    # แปลงเวลาเป็นจำนวนนาทีทั้งหมด
    try:
        specified_minutes = int(time.split(':')[0]) * 60 + int(time.split(':')[1])
    except ValueError:
        print("Invalid time format.")
        return

    # แปลงเวลาปัจจุบันเป็นจำนวนนาทีทั้งหมด
    current_time = datetime.now()
    current_minutes = current_time.hour * 60 + current_time.minute

    # คำนวณความแตกต่างในรูปแบบนาที
    inMinute = specified_minutes - current_minutes
        
    text = f"🕒 ถึงเวลากินยา!\n" \
            f"ชื่อ: {pill_name}\n" \
            f"จำนวน: {pill_amount_pertime} เม็ด\n" \
            f"ในอีก: {inMinute} นาที"
    print(text)
    
    try:
        LineBotApi(config.get('botAccessToken')).push_message(config.get('lineId'), TextMessage(text=text))
    except Exception as e:
        print(f"Error sending message to Line: {e}")
    
    # ตรวจสอบ userId
    if not config.get('userId'):
        print("Error: userId is missing or invalid.")
        return
    
    # ส่งข้อมูลการแจ้งเตือนไปยัง backend
    try:
        res = requests.post(config["url"] + "/user/addHistory", json={
            "task": "alert",
            "userID": config["userId"],
            "medicine": str(pill_data.get("pillId", "")),
        })
        if res.status_code == 200:
            print('Pill alert sent successfully to backend')
        else:
            print(f'Failed to send pill alert to backend, status code: {res.status_code}')
    except requests.exceptions.RequestException as e:
        print(f"Error in backend request: {e}")

def sendLateMessage(pill_data, time, config):
    """
    Send late pill taking notification
    """
    pill_name = pill_data.get('name', 'ไม่ทราบชื่อยา')
    pill_amount_pertime = pill_data.get('pillsPerTime', 1)

    text = f"⚠️ ลืมทานยา!\n" \
            f"ชื่อ: {pill_name}\n" \
            f"จำนวน: {pill_amount_pertime} เม็ด\n" \
            f"เวลา: {time}"
    print(text)
    
    try:
        LineBotApi(config.get('botAccessToken')).push_message(config.get('lineId'), TextMessage(text=text))
    except Exception as e:
        print(f"Error sending message to Line: {e}")
    
    # ตรวจสอบ userId
    if not config.get('userId'):
        print("Error: userId is missing or invalid.")
        return

    # ส่งข้อมูลการแจ้งเตือนไปยัง backend
    try:
        res = requests.post(config["url"] + "/user/addHistory", json={
            "task": "forget",
            "userID": config["userId"],
            "medicine": str(pill_data["pillId"]),
        })
        if res.status_code == 200:
            print('Late message sent successfully to backend')
        else:
            print(f'Failed to send late message to backend, status code: {res.status_code}')
    except requests.exceptions.RequestException as e:
        print(f"Error in backend request: {e}")
    except KeyError as e:
        print(f"KeyError: {e} - Missing key in pill_data or config.")
    except Exception as e:
        print(f"An error occurred: {e}")
