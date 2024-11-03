import requests
from linebot import LineBotApi
from linebot.models import TextMessage


def sendLateMessage(pill_data, timeWillTake, config):
    print("Attempting to send late message...")
    pill_name = pill_data['name']
    pill_amount_pertime = pill_data['pillsPerTime']
    text = f'คุณ {config["username"]} ลืมทานยา {pill_name} จำนวน {pill_amount_pertime} เม็ด เวลา {timeWillTake}'
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



def sendLineMessage(pill_data, timeWillTake, config):
    # ตรวจสอบคีย์ 'name' และ 'pillsPerTime' ใน pill_data
    pill_name = pill_data.get('name', 'ไม่ทราบชื่อยา')
    pill_amount_pertime = pill_data.get('pillsPerTime', 1)
    
    # ประมวลผลเวลาในนาทีที่เหลือ
    inMinute = timeWillTake.split(':')[1] if ':' in timeWillTake else "0"
    if len(inMinute) > 1 and inMinute.startswith('0'):
        inMinute = inMinute[1]
        
    text = f'คุณ {config["username"]} มียาต้องทานชื่อ {pill_name} จำนวน {pill_amount_pertime} เม็ด ในอีก {inMinute} นาที'
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
    print('Time to take pill')
