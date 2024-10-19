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
from PyQt5.QtWidgets import QDialog
from screen.homeScreen.ldr import DistanceSensor, detect_pill_removal
from screen.homeScreen.line_messaging import sendLateMessage, sendLineMessage
from screen.homeScreen.pill_checking import (checkIsSendLateMessage,
                                             checkIsTaken)
from screen.homeScreen.showPillDetails import showTakePillScreen
from screen.homeScreen.ui_setup import setupUi
from screen.inputPillNameScreen.main_inputPillnameScreen import PillNameScreen
from screen.pillDetailScreen.main_detail_screen import DetailScreen

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
        self.detailScreen = None  # เก็บหน้าจอ popup
        self.isSoundOn = False  # จัดการสถานะเสียง
        self.alreadyShownPopup = [False] * 8  # จัดการสถานะการแสดง popup
        self.setupUi(self)


    def setupUi(self, UIHomeScreen):
        pill_channel_buttons = []
        setupUi(self, UIHomeScreen, pill_channel_buttons, self.pill_channel_datas, self.config)
        haveToTake = []
        self.checkTakePillThread(pill_channel_buttons, self.pill_channel_datas, haveToTake, self.config, UIHomeScreen)


    def fetch_pill_names(self):
        url = __main__.config["url"] + "/user/getMedicines"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pill_names = ["โปรดเลือกชื่อยา"]
            pill_ids = [""]
            for pill in data:
                pill_names.append(pill["name"])
                pill_ids.append(pill["id"])
            return pill_names, pill_ids
        else:
            return ["โปรดเลือกชื่อยา"], [""]

    def gotoPillDetailScreen(self, channelID, pill_channel_data, parent_window):
        global isChangePage
        isChangePage = True
        if len(pill_channel_data) != 0:
            pillThatHaveToTakeFlag = 0
            takeEveryPillFlag = 0
            for index, item in enumerate(__main__.haveToTake):
                if item["channelId"] == channelID:
                    pillThatHaveToTakeFlag = 1
                if item["isTaken"] == False:
                    takeEveryPillFlag = 1
            if pillThatHaveToTakeFlag == 1 or takeEveryPillFlag == 0:
                detailScreen = DetailScreen(channelID)
                __main__.widget.addWidget(detailScreen)
                __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
        else:
            flag = 0
            for item in __main__.haveToTake:
                if item["isTaken"] == False:
                    flag = 1
            if flag == 0:
                pillData = {
                    "channelId": channelID,
                    "pillId": "",
                    "name": "",
                    "totalPills": "",
                    "pillsPerTime": "",
                    "timeToTake": []
                }
                pill_names, pill_ids = self.fetch_pill_names()
                InputScreen = PillNameScreen(pillData=pillData, pillNames=pill_names, pillID=pill_ids, parent=None)
                __main__.widget.addWidget(InputScreen)
                __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)

    # led  function

    def ledLightFunction(self, index, haveToTake, pill_data, config, timeWillTake, pill_channel_buttons) :
        alreadyTake = False
        for no, item in enumerate(haveToTake):
            if item["channelId"] == index:
                haveToTake[no]["isTaken"] = True  # อัปเดตสถานะการทานยา
                item['isTaken'] = True  # อัปเดต item เพื่อให้ระบบไม่วนซ้ำ
                alreadyTake = True
                print('Have to take', haveToTake)
    
        light = __main__.lightList[str(index)]
        if light["trigPin_1"] != -1 and light["trigPin_2"] != 1 and light["echoPin_1"] != -1 and light["echoPin_1"] and not alreadyTake:
            trigPin_1 = __main__.lightList[str(index)]["trigPin_1"]
            echoPin_1 = __main__.lightList[str(index)]["echoPin_1"]
            trigPin_2 = __main__.lightList[str(index)]["trigPin_2"]
            echoPin_2 = __main__.lightList[str(index)]["echoPin_2"]
            led = __main__.lightList[str(index)]["led"]
            sensor_1 = DistanceSensor(echo=echoPin_1, trigger=trigPin_1)
            sensor_2 = DistanceSensor(echo=echoPin_2, trigger=trigPin_2)
            isLightOn = detect_pill_removal(sensor_1, sensor_2, led, index)
            '''if not isLightOn :'''
            if True:
                print('Take pill')
                stopSound()
                __main__.lightList[str(index)]["firstLightValue"] = -1
                print('index',str(index))
                print('have to take', haveToTake)
                for no, item in enumerate(haveToTake) :
                    if item["channelId"] == (index) :
                        haveToTake[no]["isTaken"] = True
                        item['isTaken'] = True

                        pill_name = pill_data['name']
                        pill_amount_pertime = pill_data['pillsPerTime'] 
                        text = f'กินยา {pill_name} จำนวน {pill_amount_pertime} เม็ดแล้วเมื่อเวลา {timeWillTake}'
                        print(text)
                        
                        print('Take pill')

        # แสดงปุ่มทั้งหมดอีกครั้งและกลับไปหน้าหลัก
        for button in pill_channel_buttons:
            button.setVisible(True)
        new_screen = HomeScreen(self.pill_channel_datas, self.config)

        # แสดงหน้าจอใหม่
        __main__.widget.addWidget(new_screen)
        __main__.widget.setCurrentIndex(__main__.widget.indexOf(new_screen))
        new_screen.show()
        self.alreadyShownPopup[index] = False
        stopSound()
    def ledLightFunction(self, index, haveToTake, pill_data, config, timeWillTake, pill_channel_buttons):
        alreadyTake = False
        for no, item in enumerate(haveToTake):
            if item["isTaken"]:
                alreadyTake = True
                print('Already taken:', haveToTake)

        if not alreadyTake:
            light = __main__.lightList[str(index)]
            if light["trigPin_1"] != -1 and light["trigPin_2"] != 1 and light["echoPin_1"] != -1 and light["echoPin_1"]:
                trigPin_1 = light["trigPin_1"]
                echoPin_1 = light["echoPin_1"]
                trigPin_2 = light["trigPin_2"]
                echoPin_2 = light["echoPin_2"]
                led = light["led"]
                sensor_1 = DistanceSensor(echo=echoPin_1, trigger=trigPin_1)
                sensor_2 = DistanceSensor(echo=echoPin_2, trigger=trigPin_2)
                isLightOn = detect_pill_removal(sensor_1, sensor_2, led, index)

                if isLightOn:  # เมื่อมีการหยิบยา
                    print('Take pill')
                    stopSound()

                    # อัปเดตสถานะการทานยา
                    for no, item in enumerate(haveToTake):
                        if item["channelId"] == index:
                            haveToTake[no]["isTaken"] = True
                            item['isTaken'] = True

                    pill_name = pill_data['name']
                    pill_amount_pertime = pill_data['pillsPerTime']
                    text = f'กินยา {pill_name} จำนวน {pill_amount_pertime} เม็ดแล้วเมื่อเวลา {timeWillTake}'
                    print(text)

        # กลับไปหน้าหลัก
        for button in pill_channel_buttons:
            button.setVisible(True)
        new_screen = HomeScreen(self.pill_channel_datas, self.config)
        __main__.widget.addWidget(new_screen)
        __main__.widget.setCurrentIndex(__main__.widget.indexOf(new_screen))
        new_screen.show()
        self.alreadyShownPopup[index] = False
        stopSound()
    

    def checkTakePill(self, n, pill_channel_buttons, pill_channel_datas, haveToTake, config):
        for index in range(8):
            pill_channel_btn = pill_channel_buttons[index]
            pill_channel_data = pill_channel_datas[str(index)]

            # ถ้ามีข้อมูลยาในช่อง
            if len(pill_channel_data) != 0:
                for time in pill_channel_data['timeToTake']:
                    now = datetime.now()
                    
                    if time.split(":")[0] == "00":
                        now += timedelta(days=1)

                    nowDate = now.strftime("%Y-%m-%d")
                    takePillDateTime = nowDate + " " + time
                    timeObject = datetime.strptime(takePillDateTime, '%Y-%m-%d %H:%M')
                    time_diff = timeObject - now

                    # ถ้าเวลาใกล้ถึงกำหนด (ภายใน 5 นาที) และยังไม่ทานยา
                    if time_diff.total_seconds() >= 0:
                        willTakeMinute = time_diff.seconds // 60 % 60
                        willTakeHour = time_diff.seconds // 3600

                        if willTakeMinute <= 5 and willTakeMinute >= 0 and willTakeHour == 0:
                            alreadyTakeFlag = False
                            haveItemFlag = False
                            
                            for item in haveToTake:
                                if item["channelId"] == index:
                                    haveItemFlag = True
                                if item["channelId"] == index and item["isTaken"]:
                                    alreadyTakeFlag = True
                                    break
                                    

                            # ถ้าไม่มี item ใน haveToTake list
                            if not haveItemFlag:
                                takeTimeData = {
                                    "channelId": index,
                                    "time": time,
                                    "isTaken": False,
                                    "isLateMessageSended": False,
                                }
                                haveToTake.append(takeTimeData)

                            # ถ้ายังไม่ได้หยิบยาและยังไม่ได้แสดง popup
                            if not alreadyTakeFlag and not self.alreadyShownPopup[index]:
                                if not self.isSoundOn:
                                    playSound()
                                    sendLineMessage(pill_channel_datas[str(index)], str(time_diff), config)
                                    self.isSoundOn = True
                                # ซ่อนปุ่มทั้งหมด
                                for button in pill_channel_buttons:
                                    button.setVisible(False)
                                    
                                # แสดงหน้าจอรายละเอียดการทานยา (popup)
                                self.detailScreen = showTakePillScreen(pill_channel_data)
                                __main__.widget.addWidget(self.detailScreen)
                                __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
                                self.alreadyShownPopup[index] = True
                                self.ledLightFunction(index, haveToTake, pill_channel_data, config, time, pill_channel_buttons)
                            else:
                                stopSound()

                    # ถ้าเวลาทานยาผ่านไปแล้ว และยังไม่ได้ทานยา
                    else:
                        if checkIsTaken(index, haveToTake) == "not take" and checkIsSendLateMessage(index, haveToTake) == "not send":
                            sendLateMessage(pill_channel_datas[str(index)], time, config)
                            for no, item in enumerate(haveToTake):
                                if item["channelId"] == index:
                                    haveToTake[no]["isLateMessageSended"] = True
                                    
                            # แสดงปุ่มทั้งหมดอีกครั้งและกลับไปหน้าหลัก
                            for button in pill_channel_buttons:
                                button.setVisible(True)
                            new_screen = HomeScreen(self.pill_channel_datas, self.config)
                            
                            # แสดงหน้าจอใหม่
                            __main__.widget.addWidget(new_screen)
                            __main__.widget.setCurrentIndex(__main__.widget.indexOf(new_screen))
                            new_screen.show()
                            self.alreadyShownPopup[index] = False
                            stopSound()


        # การอัปเดตสถานะปุ่ม
        flag = 0
        for item in haveToTake:
            if item["isTaken"] == False:
                flag = 1

        if len(haveToTake) != 0 and flag == 1:
            for index in range(8):
                pill_channel_btn = pill_channel_buttons[index]
                pill_channel_data = pill_channel_datas[str(index)]
                # ถ้าไม่มีข้อมูลในช่องยานั้น
                if len(pill_channel_data) == 0:
                    pill_channel_btn.setStyleSheet("background-color : #FBFADD")
                    pill_channel_btn.setIcon(QtGui.QIcon())
        else:
            # ตั้งค่าข้อมูลในทุกช่องยาที่มีข้อมูล
            for index in range(8):
                pill_channel_btn = pill_channel_buttons[index]
                pill_channel_data = pill_channel_datas[str(index)]


                # ถ้ามีข้อมูลในช่อง
                if pill_channel_datas.get(str(index)) and len(pill_channel_datas[str(index)]) != 0:
                    font = QtGui.QFont()
                    font.setPointSize(18)
                    pill_channel_btn.setFont(font)
                    channel_text = "ช่องที่ " + str(index + 1) + " \n" + pill_channel_datas[str(index)]["name"]
                    pill_channel_btn.setText(channel_text)
                    pill_channel_btn.setStyleSheet("background-color : #F8F37D")


                else:
                    # If don't have data in that slot
                    icon_path = QtCore.QDir.current().absoluteFilePath("../shared/images/plus_icon.png")
                    pill_channel_btn.setIcon(QtGui.QIcon(icon_path))
                    pill_channel_btn.setIconSize(QtCore.QSize(45, 45))
                    pill_channel_btn.setStyleSheet("background-color : #97C7F9")

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













