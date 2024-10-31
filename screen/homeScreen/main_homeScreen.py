import datetime
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
        for index in range(8):
            pill_channel_btn = pill_channel_buttons[index]
            pill_channel_data = pill_channel_datas[str(index)]

            if len(pill_channel_data) != 0:
                for time in pill_channel_data['timeToTake']:
                    now = datetime.now()

                    if time.split(":")[0] == "00":
                        now += timedelta(days=1)

                    time_diff = self.isTimeToTakePill(time, now)

                    if 0 <= time_diff.total_seconds() and (time_diff.seconds // 60 % 60) <= 5 and (time_diff.seconds // 3600) == 0:
                        alreadyTakeFlag = False
                        haveItemFlag = False

                        for item in haveToTake:
                            if item["channelId"] == index:
                                haveItemFlag = True
                            if item["channelId"] == index and item["isTaken"]:
                                alreadyTakeFlag = True
                                break

                        if not haveItemFlag:
                            # ดึง pillId จาก pill_channel_data
                            id = pill_channel_data.get("id", "")
                            pillId = pill_channel_data.get("pillId", "")
                            
                            takeTimeData = {
                                "id": id,
                                "channelId": index,
                                "time": time,
                                "pillId": pillId,
                                "isTaken": False,
                                "isLateMessageSended": False,
                            }
                            haveToTake.append(takeTimeData)

                        if not alreadyTakeFlag and not self.alreadyShownPopup[index]:
                            self.manageSound('play')
                            sendLineMessage(pill_channel_datas[str(index)], str(time_diff), config)

                            for button in pill_channel_buttons:
                                button.setVisible(False)

                            # Use showTakePillScreen to create the pill detail screen with a callback
                            self.detailScreen = showTakePillScreen(pill_channel_data, lambda: self.onTakePillButtonClicked(index, haveToTake, takeTimeData, config, pill_channel_buttons))

                            __main__.widget.addWidget(self.detailScreen)
                            __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
                            self.alreadyShownPopup[index] = True
                        else:
                            self.manageSound('stop')
                    else:
                        if self.checkLateMessageStatus(index, haveToTake):
                            sendLateMessage(pill_channel_datas[str(index)], time, config)
                            for no, item in enumerate(haveToTake):
                                if item["channelId"] == index:
                                    haveToTake[no]["isLateMessageSended"] = True

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













