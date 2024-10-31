import __main__
import requests


# ฟังก์ชัน fetch_pill_names สำหรับการดึงชื่อยา
def fetch_pill_names():
    url = __main__.config["url"] + "/user/getMedicines"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # เริ่มต้นด้วย "โปรดเลือกชื่อยา"
        pill_ids = [""]
        pill_names = ["โปรดเลือกชื่อยา"]
        pill_medicalname = ["Select Pill"]

        for pill in data:
            pill_ids.append(pill["id"])
            pill_names.append(pill["name"])
            pill_medicalname.append(pill["medicalname"])
        return pill_names, pill_ids, pill_medicalname
    else:
        # กรณีที่เกิดข้อผิดพลาดในการดึงข้อมูล
        return ["โปรดเลือกชื่อยา"], [""]
