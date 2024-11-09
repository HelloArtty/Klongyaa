import datetime
import json
import os
import sys
import threading
from datetime import datetime, timedelta
from time import sleep

import __main__
import requests
from linebot import LineBotApi
from linebot.models import TextMessage
from pygame import mixer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog

# from screen.homeScreen.ldr import DistanceSensor, detect_pill_removal
from screen.homeScreen.line_messaging import sendLateMessage, sendLineMessage
from screen.homeScreen.showTakePillDetails import showTakePillScreen
from screen.homeScreen.test import SuccessSaveScreen
from screen.homeScreen.ui_setup import setupUi
from screen.inputPillNameScreen.main_inputPillnameScreen import PillNameScreen
from screen.pillDetailScreen.main_detail_screen import DetailScreen
from shared.api.getchecktakepill import checkTakePill
from shared.api.getMedicines import fetch_pill_names

sys.path.append(os.path.abspath('../klongyaa/Klongyaa'))


mixer.init()
# กำหนดตัวแปรสำหรับ path ของไฟล์เสียง
sound_file_path = "D:/klongyaa/Klongyaa/screen/homeScreen/sound_notification.wav"

# สร้างตัวแปรสำหรับเสียงโดยใช้ path ที่แยกออกมา
sound_notification = mixer.Sound(sound_file_path)

print(sound_notification)
#---------------- Function play sound notification ----------------#

class HomeScreen(QDialog):
    def __init__(self, pill_channel_datas, config):
        super().__init__()
        self.pill_channel_datas = pill_channel_datas
        self.config = config
        global isChangePage
        isChangePage = False
        self.detailScreen = None  # Keep track of the popup screen
        self.isSoundOn = False  # Manage sound state
        self.alreadyShownPopup = [False] * 8  # Manage popup display state
        self.pill_channel_buttons = []  # Store the buttons as an instance variable
        self.notification_queue = []
        self.current_date = datetime.now().date()
        self.last_check_times = {}
        self.sound_cooldown = False
        self.setupUi(self)
    
    def setupUi(self, UIHomeScreen):
        setupUi(self, UIHomeScreen, self.pill_channel_buttons, self.pill_channel_datas, self.config)
        haveToTake = []
        self.checkTakePillThread(self.pill_channel_buttons, self.pill_channel_datas, haveToTake, self.config, UIHomeScreen)
        
    def gotoPillDetailScreen(self, channelID, pill_channel_data):
        global isChangePage
        isChangePage = True

        if pill_channel_data:  # ตรวจสอบว่าช่องนี้มีข้อมูลยาหรือไม่
            pillThatHaveToTakeFlag = any(item["channelId"] == channelID for item in __main__.haveToTake)
            takeEveryPillFlag = any(not item["isTaken"] for item in __main__.haveToTake)

            # กรณีที่มียาที่ยังต้องทาน หรือทุกเม็ดยาถูกทานหมดแล้ว
            if pillThatHaveToTakeFlag or not takeEveryPillFlag:
                detailScreen = DetailScreen(channelID)
                __main__.widget.addWidget(detailScreen)
                __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
        else:
            # กรณีที่ `pill_channel_data` ไม่มีข้อมูล (ยังไม่ได้เพิ่มยาในช่องนี้)
            if all(item["isTaken"] for item in __main__.haveToTake):
                pillData = {
                    "channelId": channelID,
                    "pillId": "",
                    "name": "",
                    "medicalname": "",
                    "totalPills": "",
                    "pillsPerTime": "",
                    "timeToTake": []
                }
                pill_names, pill_ids, pill_medicalname = fetch_pill_names()
                InputScreen = PillNameScreen(pillData=pillData, pillNames=pill_names, pillID=pill_ids, pillNamesEng=pill_medicalname, parent=None)
                __main__.widget.addWidget(InputScreen)
                __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)

    def manageSound(self, action='play'):
        if action == 'play':
            if not self.isSoundOn:
                self.isSoundOn = True
                sound_notification.play(-1)
        elif action == 'stop':
            if self.isSoundOn:
                self.isSoundOn = False
                sound_notification.stop()

    def showHomeScreen(self, pill_channel_buttons):
        for button in pill_channel_buttons:
            button.setVisible(True)
        new_screen = HomeScreen(self.pill_channel_datas, self.config)
        __main__.widget.addWidget(new_screen)
        __main__.widget.setCurrentIndex(__main__.widget.indexOf(new_screen))
        new_screen.show()
        print("Back To HomeScreen")

    def isTimeToTakePill(self, time, now):
        nowDate = now.strftime("%Y-%m-%d")
        takePillDateTime = nowDate + " " + time
        timeObject = datetime.strptime(takePillDateTime, '%Y-%m-%d %H:%M')
        return timeObject - now

    def updatePillStatus(self, takeTimeData, haveToTake):
        for no, item in enumerate(haveToTake):
            # ตรวจสอบ id ให้ตรงกันด้วยเพื่อความแม่นยำ
            if item["channelId"] == int(takeTimeData["channelId"]) and item["id"] == takeTimeData["id"]:
                haveToTake[no]["isTaken"] = True
                item['isTaken'] = True

    def onTakePillButtonClicked(self, index, haveToTake, takeTimeData, config, pill_channel_buttons):
        print("Pill confirmed as taken")
        
        # ใช้ takeTimeData ในการอัปเดตสถานะการทานยา
        self.updatePillStatus(takeTimeData, haveToTake)
        # print(takeTimeData)

        # หยุดเสียงเตือน
        self.manageSound('stop')

        # ส่งข้อมูลการกินยาไปยัง backend
        res = requests.post(config["url"] + "/user/addHistory", json={
            "task": "take",
            "userID": config["userId"],
            "medicine": str(takeTimeData["pillId"]),
        })
        print("Add history response:", res.status_code)
        
        # print("id", takeTimeData["id"])
        id = str(takeTimeData["id"])
        res = requests.put(config["url"] + "/user/userTakePill/" + id)
        print("Update pill status response:", res.status_code)

        # Pass pillData when creating SuccessSaveScreen
        # success_save_screen = SuccessSaveScreen()
        
        # __main__.widget.addWidget(success_save_screen)
        # __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
        # __main__.widget.removeWidget(self.detailScreen)
        
        self.detailScreen.close()  # ปิดหน้าจอการทานยา
        self.showHomeScreen(pill_channel_buttons)  # แสดงหน้าจอหลัก

        # รีเซ็ตค่า popup เพื่อให้สามารถแสดง popup ในครั้งถัดไปได้
        self.alreadyShownPopup[int(takeTimeData["channelId"])] = False

    def remove_expired_entries(self, haveToTake, now):
        """
        กรองข้อมูลยาที่หมดเวลาทานแล้วออกจาก haveToTake เพื่อป้องกันการแจ้งเตือนซ้ำหลังเวลาที่กำหนด
        """
        current_time = now.time()
        for item in haveToTake[:]:  # ใช้การทำงานผ่านสำเนาของ list เพื่อแก้ไขได้
            # แปลงเวลาทานยาเป็น datetime.time เพื่อเปรียบเทียบ
            pill_time = datetime.strptime(item["time"], "%H:%M").time()
            
            # ลบออกจากรายการถ้าเวลาปัจจุบันเลยเวลาทานยามาแล้ว และยาถูกทานแล้ว
            if pill_time < current_time and item.get("isTaken"):
                haveToTake.remove(item)


    def checkTakePill(self, n, pill_channel_buttons, pill_channel_datas, haveToTake, config):
        today = datetime.now().date()
        now = datetime.now()
        
        # Reset daily status if date has changed
        if today != self.current_date:
            for item in haveToTake:
                item['isTaken'] = False
                item['isLateMessageSended'] = False
                item['alreadyNotified'] = False
            self.current_date = today
            print("New day detected. Resetting statuses for all channels.")
            
            
        # ลบข้อมูลยาที่หมดเวลาทานแล้วออกจาก haveToTake
        self.remove_expired_entries(haveToTake, now)

        # Initialize notification queue and reset notification flag
        self.notification_queue = []
        self.notification_found = False  # Flag to check if notification is found

        # Function to check if the time should be skipped
        def should_skip_check(time_str):
            try:
                target_time = datetime.strptime(time_str, "%H:%M").time()
                current_time = now.time()
                
                if time_str.startswith("00") and current_time.hour >= 1:
                    return True
                hour_diff = current_time.hour - target_time.hour
                if hour_diff > 1 or (hour_diff == 1 and current_time.minute > target_time.minute):
                    return True
                return False
            except:
                return False

        # Loop through each pill channel
        for index, pill_channel_data in pill_channel_datas.items():
            index = int(index)
            if not pill_channel_data:
                continue

            # Check last update time for this channel to ensure 10-second intervals
            last_check = self.last_check_times.get(index, 0)
            if now.timestamp() - last_check < 1:  # 10 seconds
                continue
            self.last_check_times[index] = now.timestamp()

            # Loop through each time entry for the pill channel
            for time_entry in pill_channel_data['timeToTake']:
                time = time_entry
                
                if should_skip_check(time):
                    print(f"Skipping check for channel {index} at {time} - Too late")
                    continue
                
                existing_data = next((item for item in haveToTake if
                    item["channelId"] == index and
                    item["time"] == time and
                    item["id"] == pill_channel_data.get("id")), None)
                
                # หากยาถูกทานแล้ว ให้ข้ามไป
                if existing_data and existing_data.get("isTaken"):
                    print(f"Skipping check for channel {index} at {time} - Already taken \n")
                    continue
                
                check_time = now + timedelta(days=1) if time.startswith("00") else now
                time_diff = self.isTimeToTakePill(time, check_time)
                
                # ตรวจสอบการแจ้งเตือนล่าช้า
                is_too_late = time_diff.total_seconds() < -10
                
                if is_too_late and existing_data and not existing_data.get("isLateMessageSended"):
                    print(f"Sending late message for channel {index} at {time}")
                    sendLateMessage(pill_channel_data, time, config)
                    existing_data["isLateMessageSended"] = True
                    existing_data["alreadyNotified"] = True
                    self.showHomeScreen(pill_channel_buttons)
                    self.manageSound('stop')
                    self.notification_found = True  # Set flag to indicate notification was found
                    continue  # Continue with other checks to avoid duplicate notification
                
                # ตรวจสอบการแจ้งเตือนถ้าถึงเวลา (ในช่วง 5 นาที)
                if 0 <= time_diff.total_seconds() <= 120:
                    pill_channel_data = checkTakePill(index)
                    if not pill_channel_data:
                        continue
                    
                    is_taken = next((entry['isTaken'] for entry in pill_channel_data.get('timeToTake', []) 
                                    if entry['time'] == time), False)
                    
                    if is_taken:
                        print(f"Pill already taken for channel {index} at {time}")
                        if existing_data:
                            existing_data["isTaken"] = True
                        continue
                    
                    if existing_data:
                        # ป้องกันการแจ้งเตือนซ้ำโดยเช็คว่าเคยแจ้งแล้วหรือไม่
                        if not existing_data["alreadyNotified"]:
                            self.notification_queue.append(existing_data)
                            existing_data["alreadyNotified"] = True
                            self.notification_found = True
                    else:
                        takeTimeData = {
                            "id": pill_channel_data.get("id", ""),
                            "channelId": index,
                            "time": time,
                            "pillId": pill_channel_data.get("pillId", ""),
                            "name": pill_channel_data.get("name", ""),
                            "isTaken": is_taken,
                            "isLateMessageSended": False,
                            "alreadyNotified": False,
                        }
                        haveToTake.append(takeTimeData)
                        self.notification_queue.append(takeTimeData)
                        print(f"Queue", json.dumps(self.notification_queue, indent=4))
                        takeTimeData["alreadyNotified"] = True
                        self.notification_found = True

        # แสดงการแจ้งเตือนถ้ามีในคิว
        if self.notification_found:
            self.showNextNotification(config, pill_channel_buttons, haveToTake)

    def checkLateMessageStatus(self, index, time, haveToTake, is_too_late):
        # ถ้าไม่เลยเวลา return True เพื่อข้ามการส่งข้อความ
        if not is_too_late:
            return True
            
        for item in haveToTake:
            if item["channelId"] == index and item["time"] == time:
                # ถ้ายาถูกทานแล้ว หรือส่งข้อความแล้ว return True
                if item["isTaken"] or item["isLateMessageSended"]:
                    return True
                return False  # ต้องส่งข้อความเตือน
        return True  # ไม่พบข้อมูล ข้ามการส่งข้อความ

    def showNextNotification(self, config, pill_channel_buttons, haveToTake):
        # หยุดหากไม่มีการแจ้งเตือนในคิวแล้ว
        if not self.notification_queue:
            print("No more notifications in the queue.")
            return

        # ดึงการแจ้งเตือนตัวแรกจากคิวและตรวจสอบว่าถูกทานไปแล้วหรือยัง
        while self.notification_queue:
            next_pill = self.notification_queue.pop(0)
            
            # ตรวจสอบสถานะการทานยา หาก `isTaken` เป็น True ให้ข้ามไปแจ้งเตือนตัวถัดไป
            if next_pill.get("isTaken"):
                print(f"Skipping notification for channel {next_pill['channelId']} at {next_pill['time']} because isTaken is True.")
                continue
            
            # เริ่มแสดงการแจ้งเตือนสำหรับยาที่ยังไม่ได้ทาน
            self.manageSound('play')

            
            # แสดงการแจ้งเตือนหน้าจอ
            time = next_pill["time"]
            sendLineMessage(next_pill, time, config)  # แสดงข้อความแจ้งเตือนใน Line หรือช่องทางอื่น ๆ
            print(f"Notification sent for channel {next_pill['channelId']} at {next_pill['time']}")

            for button in pill_channel_buttons:
                button.setVisible(False)

            # แสดงหน้าจอการทานยา
            self.detailScreen = showTakePillScreen(
                next_pill,
                lambda: self.onTakePillButtonClicked(next_pill["channelId"], haveToTake, next_pill, config, pill_channel_buttons)
            )

            __main__.widget.addWidget(self.detailScreen)
            __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
            self.alreadyShownPopup[next_pill["channelId"]] = True
            return  # หยุดหลังจากแสดงการแจ้งเตือนครั้งแรกที่ยังไม่ได้ทานยา

    def checkTakePillThread(self, pill_channel_buttons, pill_channel_datas,haveToTake,config, UIHomeScreen):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(lambda n : self.checkTakePill(n, pill_channel_buttons, pill_channel_datas,haveToTake,config))
        self.thread.start()

isFirstLoop = True


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)


    def run(self):
        global isFirstLoop
        num = 0
        while True :
            if not isFirstLoop:
                sleep(9)
            isFirstLoop = False
            if isChangePage : break
            self.progress.emit(num + 1)
            num += 1
        self.finished.emit()