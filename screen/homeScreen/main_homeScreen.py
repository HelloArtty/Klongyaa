import os
import sys
from datetime import datetime
from functools import partial
from time import sleep

import __main__
import requests
from linebot import LineBotApi
from linebot.models import TextMessage
from pygame import mixer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog
from screen.homeScreen.line_messaging import sendLateMessage, sendLineMessage
from screen.homeScreen.pill_checking import (checkIsSendLateMessage,
                                             checkIsTaken, checkTakePill)
from screen.homeScreen.sound_functions import playSound, stopSound
from screen.homeScreen.ui_setup import setupUi
# from screen.homeScreen.worker import Worker
from screen.inputPillNameScreen.main_inputPillnameScreen import PillNameScreen
from screen.pillDetailScreen.main_detail_screen import DetailScreen

sys.path.append(os.path.abspath('../klongyaa/Klongyaa'))

isChangePage = False
isSoundOn = False
isFirstLoop = True
mixer.init()
sound_notification = mixer.Sound("../Klongyaa/screen/homeScreen/sound_notification.wav")

class HomeScreen(QDialog):
    def __init__(self, pill_channel_datas, config):
        super().__init__()
        self.pill_channel_datas = pill_channel_datas
        self.config = config
        global isChangePage
        isChangePage = False
        self.setupUi(self)

    def setupUi(self, UIHomeScreen):
        pill_channel_buttons = []
        setupUi(self, UIHomeScreen, pill_channel_buttons, self.pill_channel_datas, self.config)
        self.checkTakePillThread(pill_channel_buttons, self.pill_channel_datas)

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

    # def ledLightFunction(self, index) :
    #     alreadyTake = False
    #     for no, item in enumerate(__main__.haveToTake) :
    #         if item["id"] == no and item["isTaken"]:
    #             alreadyTake = True
                
    #     light = __main__.lightList[str(index)]
    #     if light["dout"] != -1 and light["pdPin"] != -1 and not alreadyTake:
    #     # if True:
    #         if light["firstWeightValue"] == -1:
    #             dout = __main__.lightList[str(index)]["dout"]
    #             pdPin = __main__.lightList[str(index)]["pdPin"]
    #             value = get_first_load_value(dout,pdPin) # Don't forget to adding this Register Pin parameter
    #             __main__.lightList[str(index)]["firstWeightValue"] = value
    #         firstWeightValue = __main__.lightList[str(index)]["firstWeightValue"]
    #         dout = __main__.lightList[str(index)]["dout"]
    #         pdPin = __main__.lightList[str(index)]["pdPin"]
    #         led = __main__.lightList[str(index)]["led"]
    #         isLightOn = pick_pill_detection(firstWeightValue, dout, pdPin, led) # Don't forget to adding this Register Pin parameter
    #         if not isLightOn :
    #             stopSound()
    #             __main__.lightList[str(index)]["firstLightValue"] = -1
    #             print("Not light on")
    #             for no, item in enumerate(__main__.haveToTake) :
    #                 if item["id"] == index :
    #                     __main__.haveToTake[no]["isTaken"] = True
    #                     res = requests.post(__main__.config["url"] + "/user/addHistory", json={
    #                             "channelID": str(item["id"]),
    #                             "lineUID": __main__.config["userId"],
    #                             "task": "Take pill"
    #                             })
    #                     print(f'res : {res}')
    #                     print('Take pill')

    def checkTakePill(self, n, pill_channel_buttons, pill_channel_datas):
        checkTakePill(self, n, pill_channel_buttons, pill_channel_datas, __main__.haveToTake, self.config)

    def checkTakePillThread(self, pill_channel_buttons, pill_channel_datas):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(lambda n : self.checkTakePill(n, pill_channel_buttons, pill_channel_datas))
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