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
    specified_minutes = int(time.split(':')[0]) * 60 + int(time.split(':')[1])

    # แปลงเวลาปัจจุบันเป็นจำนวนนาทีทั้งหมด
    current_time = datetime.now()
    current_minutes = current_time.hour * 60 + current_time.minute

    # คำนวณความแตกต่างในรูปแบบนาที
    inMinute = specified_minutes - current_minutes
        
    # text = f'คุณ {config["username"]} มียาต้องทานชื่อ {pill_name} จำนวน {pill_amount_pertime} เม็ด ในอีก {inMinute} นาที'
    text = f"🕒 ถึงเวลากินยา!\n" \
            f"ชื่อ: {pill_name}\n" \
            f"จำนวน: {pill_amount_pertime} เม็ด\n" \
            f"ในอีก: {inMinute} นาที\n"
    print(text)
    
    # ตรวจสอบ userId
    if not config.get('userId'):
        print("Error: userId is missing or invalid.")
        return
    
    # ส่งข้อมูลการแจ้งเตือนไปยัง backend
    res = requests.post(config["url"] + "/user/addHistory", json={
            "task": "alert",
            "userID": config["userId"],
            "medicine": str(pill_data.get("pillId", "")),
            })
    if res.status_code == 200:
        print('Pill alert sent successfully to backend')
    else:
        print('Failed to send pill alert to backend')



def sendLateMessage(pill_data, time, config):
    """
    Send late pill taking notification
    """
    pill_name = pill_data['name']
    pill_amount_pertime = pill_data['pillsPerTime']
    # text = f'คุณ {config["username"]} ลืมทานยา {pill_name} จำนวน {pill_amount_pertime} เม็ด เวลา {time}'
    text = f"⚠️ ลืมทานยา!\n" \
            f"ชื่อ: {pill_name}\n" \
            f"จำนวน: {pill_amount_pertime} เม็ด\n" \
            f"เวลา: {time}\n"
    print(text)
    
    
    # ส่งข้อความจริง (แสดงว่าการส่งสำเร็จหากไม่มีปัญหา)
    try:
        res = requests.post(config["url"] + "/user/addHistory", json={
            "task": "forget",
            "userID": config["userId"],
            "medicine": str(pill_data["pillId"]),
        })
        print('Late message sent successfully' if res.status_code == 200 else 'Failed to send late message')
    except Exception as e:
        print(f"Error in sending late message: {e}")

    
    except KeyError as e:
        print(f"KeyError: {e} - Missing key in pill_data or config.")
    except Exception as e:
        print(f"An error occurred: {e}")