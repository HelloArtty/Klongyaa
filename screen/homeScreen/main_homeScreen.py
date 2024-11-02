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
from screen.homeScreen.pill_checking import (checkIsSendLateMessage,
                                             checkIsTaken)
from screen.homeScreen.showTakePillDetails import showTakePillScreen
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
def releaseCooldown():
    global sound_cooldown
    sound_cooldown = False

def playSound():
    sound_notification.play()
    sound_cooldown = True
    threading.Timer(2, releaseCooldown).start()

def stopSound():
    sound_notification.stop()


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
        if action == 'play' and not self.isSoundOn:
            playSound()
            self.isSoundOn = True
        elif action == 'stop' and self.isSoundOn:
            stopSound()
            self.isSoundOn = False

    def updatePillStatus(self, takeTimeData, haveToTake):
        index = int(takeTimeData["channelId"])
        for no, item in enumerate(haveToTake):
            if item["channelId"] == index:
                haveToTake[no]["isTaken"] = True
                item['isTaken'] = True

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

    def checkLateMessageStatus(self, index, haveToTake):
        return checkIsTaken(index, haveToTake) == "not take" and checkIsSendLateMessage(index, haveToTake) == "not send"

    def onTakePillButtonClicked(self, index, haveToTake, takeTimeData, config, pill_channel_buttons):
        print("Pill confirmed as taken")
        
        # ใช้ takeTimeData ในการอัปเดตสถานะการทานยา
        self.updatePillStatus(takeTimeData, haveToTake)
        print (takeTimeData)

        # หยุดเสียงเตือน
        self.manageSound('stop')

        # ส่งข้อมูลการกินยาไปยัง backend
        res = requests.post(config["url"] + "/user/addHistory", json={
            "task": "take",
            "userID": config["userId"],
            "medicine": str(takeTimeData["pillId"]),
        })
        print("Add history response:", res.status_code)
        
        print("id", takeTimeData["id"])
        id = str(takeTimeData["id"])
        res = requests.put(config["url"] + "/user/userTakePill/" + id)
        print("Update pill status response:", res.status_code)

        # เปลี่ยนกลับไปที่หน้า HomeScreen
        self.showHomeScreen(pill_channel_buttons)

        # รีเซ็ตค่า popup เพื่อให้สามารถแสดง popup ในครั้งถัดไปได้
        self.alreadyShownPopup[int(takeTimeData["channelId"])] = False

    def checkTakePill(self, n, pill_channel_buttons, pill_channel_datas, haveToTake, config):
        # วนลูปเฉพาะช่องที่มีข้อมูลใน pill_channel_datas
        for index, pill_channel_data in pill_channel_datas.items():
            index = int(index)
            pill_channel_btn = pill_channel_buttons[index]

            # ข้ามช่องที่ไม่มีข้อมูล
            if not pill_channel_data:
                continue

            now = datetime.now()

            # ตรวจสอบเวลาที่อยู่ภายในช่วง 5 นาทีจากเวลาปัจจุบันเท่านั้น
            for time_entry in pill_channel_data['timeToTake']:
                time = time_entry
                
                print(f"Checking time: {time} for channel {index}")
                
                # เลื่อนเป็นวันถัดไปถ้าเวลาเริ่มต้นที่ "00"
                check_time = now + timedelta(days=1) if time.startswith("00") else now
                time_diff = self.isTimeToTakePill(time, check_time)
                
                # ข้ามเวลาทานยาที่เลยเวลามานานกว่า 5 นาที
                if time_diff.total_seconds() < -300:
                    continue  # ข้ามเวลาที่เลยมาเกิน 5 นาที

                # ถ้าพบว่าเวลานั้นอยู่ในช่วง 5 นาทีจากเวลาปัจจุบัน
                if 0 <= time_diff.total_seconds() <= 300:
                    # ดึงข้อมูลจาก API และตรวจสอบ isTaken
                    pill_channel_data = checkTakePill(index)
                    print(f"Pill channel data: {json.dumps(pill_channel_data, indent=4)}")
                    
                    # ตรวจสอบ isTaken ใน timeToTake ของ pill_channel_data
                    for entry in pill_channel_data.get('timeToTake', []):
                        print(f"Time: {entry['time']}, isTaken: {entry['isTaken']}")

                        # ตรวจสอบว่ามีเวลาใดที่ isTaken เป็น False หรือไม่
                        if entry['isTaken'] == False:
                            print(f"Time {entry['time']} for channel {index} is not taken yet.")
                            is_taken = False
                        else:
                            is_taken = True
                    
                    if not pill_channel_data:
                        continue  # ถ้า API ไม่คืนข้อมูลให้ข้ามช่องนี้

                    # สร้าง takeTimeData สำหรับการแสดงข้อมูล
                    takeTimeData = {
                        "id": pill_channel_data.get("id", ""),
                        "channelId": index,
                        "time": time,
                        "pillId": pill_channel_data.get("pillId", ""),
                        "isTaken": is_taken,
                        "isLateMessageSended": False,
                    }
                    print(f"Take time data: {json.dumps(takeTimeData , indent=4)}")
                    
                    # ตรวจสอบว่า haveToTake มีข้อมูลนี้อยู่หรือไม่ก่อนเพิ่มเข้าไป
                    if not any(item["channelId"] == takeTimeData["channelId"] and item["time"] == takeTimeData["time"] for item in haveToTake):
                        haveToTake.append(takeTimeData)
                        print(f"Added to haveToTake: {takeTimeData}")
                    else:
                        print(f"Data for channelId {takeTimeData['channelId']} and time {takeTimeData['time']} already exists in haveToTake.")

                    print(f"Current haveToTake data: {json.dumps(haveToTake, indent=4)}")


                    # ตรวจสอบ isTaken สำหรับเวลาที่กำลังจะถึง
                    is_taken = checkIsTaken(index, haveToTake)
                    print(f"Is taken: {is_taken}")

                    if is_taken == "is taken":
                        continue  # ถ้า isTaken เป็น True ข้ามไปยังช่องถัดไป

                    # แสดงหน้าจอการทานยาถ้ายังไม่เคยแสดงมาก่อนสำหรับช่องนี้
                    if not self.alreadyShownPopup[index]:
                        self.manageSound('play')
                        sendLineMessage(pill_channel_data, str(time_diff), config)

                        for button in pill_channel_buttons:
                            button.setVisible(False)

                        # แสดงหน้าจอการทานยา
                        self.detailScreen = showTakePillScreen(
                            pill_channel_data,
                            lambda: self.onTakePillButtonClicked(index, haveToTake, takeTimeData, config, pill_channel_buttons)
                        )

                        __main__.widget.addWidget(self.detailScreen)
                        __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
                        self.alreadyShownPopup[index] = True
                        break  # ถ้าเจอเวลาที่ตรงแล้วให้ข้ามไปตรวจสอบช่องถัดไป
                    else:
                        self.manageSound('stop')
                    break  # ถ้าเจอเวลาที่ตรงแล้วให้ข้ามไปตรวจสอบช่องถัดไป
                else:
                    # ส่งข้อความเตือนถ้ายังไม่ได้ทานยา
                    if self.checkLateMessageStatus(index, haveToTake):
                        sendLateMessage(pill_channel_data, time, config)
                        for item in haveToTake:
                            if item["channelId"] == index:
                                item["isLateMessageSended"] = True

                        self.showHomeScreen(pill_channel_buttons)
                        self.alreadyShownPopup[index] = False

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
                sleep(1)
            isFirstLoop = False
            if isChangePage : break
            self.progress.emit(num + 1)
            num += 1
        self.finished.emit()













