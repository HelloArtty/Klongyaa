import json
import sys
from datetime import datetime
from functools import partial

import __main__
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QDialog
from screen.inputPillNameScreen.gen.gen_input_voice_screen import *
from screen.inputPillNameScreen.gen.gen_input_voice_screen_again import *
from screen.inputPillNameScreen.gen.gen_voice_loading_screen import *

globalTimesToTakePillArr = []
globalPillData = {}

def resetGlobalData() :
    global globalPillData
    global globalTimesToTakePillArr

    globalTimesToTakePillArr = []
    globalPillData = {}

class InputTimeToTakePillScreen(QDialog):
    def __init__(self, pillData, editIndex, isFromSummaryScreen):
        super().__init__()
        global globalPillData
        globalPillData = pillData
        self.editIndex = editIndex
        self.isFromSummaryScreen = isFromSummaryScreen
        self.selected_hour = 0
        self.selected_minute = 0
        self.setupUi(self)
        self.connect_signals()

    def setupUi(self, background_input_times_to_take_pill):
        background_input_times_to_take_pill.setObjectName("background_input_times_to_take_pill")
        background_input_times_to_take_pill.resize(800, 480)
        background_input_times_to_take_pill.setStyleSheet("QWidget#background_input_times_to_take_pill{\n""background-color: #97C7F9}")
        
        self.no_channel = QtWidgets.QLabel(background_input_times_to_take_pill)
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 191, 71))
        font = QtGui.QFont()
        font.setFamily("JasmineUPC")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF;\n""font: 75 36pt \"JasmineUPC\";\n""border-radius: 25px;\n""color: #070021;\n""")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")
        
        self.question_input_times_to_take_pill = QtWidgets.QLabel(background_input_times_to_take_pill)
        self.question_input_times_to_take_pill.setGeometry(QtCore.QRect(245, 30, 350, 70))
        self.question_input_times_to_take_pill.setStyleSheet("font: 34pt \"JasmineUPC\";")
        self.question_input_times_to_take_pill.setAlignment(QtCore.Qt.AlignCenter)
        self.question_input_times_to_take_pill.setObjectName("question_input_times_to_take_pill")

        # Time Frame
        self.time_frame = QtWidgets.QFrame(background_input_times_to_take_pill)
        self.time_frame.setGeometry(QtCore.QRect(75, 120, 650, 265))
        self.time_frame.setStyleSheet("background-color: #97C7F9; border: none")

        # Hour Frame
        self.hour_frame = QtWidgets.QFrame(self.time_frame)
        self.hour_frame.setGeometry(QtCore.QRect(50, 10, 250, 240))
        self.hour_frame.setStyleSheet("background-color: #97C7F9; border: none")
        
        # Minute Frame
        self.minute_frame = QtWidgets.QFrame(self.time_frame)
        self.minute_frame.setGeometry(QtCore.QRect(350, 10, 250, 240))
        self.minute_frame.setStyleSheet("background-color: #97C7F9; border: none")

        # Hour Display
        self.hour_display = QtWidgets.QLabel(f"{self.selected_hour:02d}", self.hour_frame)
        self.hour_display.setFont(QtGui.QFont("Arial", 96, QtGui.QFont.Bold))
        self.hour_display.setStyleSheet("color: black; background-color: #97C7F9; padding: 10px;")
        self.hour_display.setAlignment(QtCore.Qt.AlignCenter)
        self.hour_display.setGeometry(QtCore.QRect(0, 58, 250, 125))

        # Minute Display
        self.minute_display = QtWidgets.QLabel(f"{self.selected_minute:02d}", self.minute_frame)
        self.minute_display.setFont(QtGui.QFont("Arial", 96, QtGui.QFont.Bold))
        self.minute_display.setStyleSheet("color: black; background-color: #97C7F9; padding: 10px;")
        self.minute_display.setAlignment(QtCore.Qt.AlignCenter)
        self.minute_display.setGeometry(QtCore.QRect(0, 58, 250, 125))

        # Up Hour Button
        self.up_hour_button = QtWidgets.QPushButton("▲", self.hour_frame)
        self.up_hour_button.setFont(QtGui.QFont("Arial", 36))
        self.up_hour_button.setStyleSheet("background-color: #97C7F9; color: #000; padding: 10px;")
        self.up_hour_button.setGeometry(QtCore.QRect(0, 0, 250, 65))

        # Down Hour Button
        self.down_hour_button = QtWidgets.QPushButton("▼", self.hour_frame)
        self.down_hour_button.setFont(QtGui.QFont("Arial", 36))
        self.down_hour_button.setStyleSheet("background-color: #97C7F9; color: #000; padding: 10px;")
        self.down_hour_button.setGeometry(QtCore.QRect(0, 175, 250, 65))

        # Up Minute Button
        self.up_minute_button = QtWidgets.QPushButton("▲", self.minute_frame)
        self.up_minute_button.setFont(QtGui.QFont("Arial", 36))
        self.up_minute_button.setStyleSheet("background-color: #97C7F9; color: #000; padding: 10px;")
        self.up_minute_button.setGeometry(QtCore.QRect(0, 0, 250, 65))

        # Down Minute Button
        self.down_minute_button = QtWidgets.QPushButton("▼", self.minute_frame)
        self.down_minute_button.setFont(QtGui.QFont("Arial", 36))
        self.down_minute_button.setStyleSheet("background-color: #97C7F9; color: #000; padding: 10px;")
        self.down_minute_button.setGeometry(QtCore.QRect(0, 175, 250, 65))

        # Correct button (green)
        self.button_correct_pill_name = QtWidgets.QToolButton(background_input_times_to_take_pill)
        self.button_correct_pill_name.setGeometry(QtCore.QRect(295, 375, 200, 90))
        self.button_correct_pill_name.setStyleSheet("QToolButton#button_correct_pill_name { font: 75 36pt \"JasmineUPC\"; background-color:#24BD73; color: #ffffff; border-radius:20px; } QToolButton#button_correct_pill_name:hover { font: 75 36pt \"JasmineUPC\"; background-color:#23B36D; color: #ffffff; border-radius:20px; }")
        self.button_correct_pill_name.setObjectName("button_correct_pill_name")
        self.button_correct_pill_name.clicked.connect(self.goToAddSummaryTimeScreen)
        
        self.retranslateUi(background_input_times_to_take_pill)
        QtCore.QMetaObject.connectSlotsByName(background_input_times_to_take_pill)

    def retranslateUi(self, background_input_times_to_take_pill):
        _translate = QtCore.QCoreApplication.translate
        global globalPillData
        
        channelID = "ช่องที่ " + str(globalPillData["id"] + 1)
        background_input_times_to_take_pill.setWindowTitle(_translate("background_input_times_to_take_pill", "Dialog"))
        self.no_channel.setText(_translate("background_input_times_to_take_pill", channelID))
        self.question_input_times_to_take_pill.setText(_translate("background_input_times_to_take_pill", "เพิ่มเวลาทานยา"))
        self.button_correct_pill_name.setText(_translate("background_total_pills", "ถัดไป"))
    
    def connect_signals(self):
        self.up_hour_button.clicked.connect(lambda: self.change_time("hour", 1))
        self.down_hour_button.clicked.connect(lambda: self.change_time("hour", -1))
        self.up_minute_button.clicked.connect(lambda: self.change_time("minute", 1))
        self.down_minute_button.clicked.connect(lambda: self.change_time("minute", -1))
        
    def change_time(self, time_type, increment):
        if time_type == "hour":
            self.selected_hour = (self.selected_hour + increment) % 24
            self.hour_display.setText(f"{self.selected_hour:02d}")
        elif time_type == "minute":
            self.selected_minute = (self.selected_minute + increment) % 60
            self.minute_display.setText(f"{self.selected_minute:02d}")
    
    def goToAddSummaryTimeScreen(self):
        
        current_time = f"{self.selected_hour:02d}:{self.selected_minute:02d}"
        if 'timeToTake' not in globalPillData:
            globalPillData['timeToTake'] = []
        if current_time not in globalPillData['timeToTake']:
            globalPillData['timeToTake'].append(current_time)
    
        # Sort times
        globalPillData['timeToTake'].sort(key=lambda time: datetime.strptime(time, "%H:%M"))
        print(json.dumps(globalPillData, indent=4))
        add_summary_time_screen = AddSummaryTimeScreen(globalPillData)
        __main__.widget.addWidget(add_summary_time_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)


#เพิ่มเวลาทานยา
class AddSummaryTimeScreen(QDialog):
    def __init__(self, pillData):
        super().__init__()
        global globalTimesToTakePillArr
        global globalPillData
        globalTimesToTakePillArr = pillData['timeToTake']
        globalPillData = pillData
        self.timesToTakesPillArr = globalTimesToTakePillArr
        self.setupUi(self)
        self.success_button.clicked.connect(self.goToPillSummaryScreen)


    def setupUi(self, background_confirm_times_to_take_pill):
        background_confirm_times_to_take_pill.setObjectName("background_confirm_times_to_take_pill")
        background_confirm_times_to_take_pill.resize(800, 480)
        background_confirm_times_to_take_pill.setStyleSheet("QWidget#background_confirm_times_to_take_pill{\n""background-color: #97C7F9}")
        self.no_channel = QtWidgets.QLabel(background_confirm_times_to_take_pill)
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 190, 70))
        font = QtGui.QFont()
        font.setFamily("JasmineUPC")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF;\n""font: 75 36pt \"JasmineUPC\";\n""border-radius: 25px;\n""color: #070021;\n""")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")
        self.header_text = QtWidgets.QLabel(background_confirm_times_to_take_pill)
        self.header_text.setGeometry(QtCore.QRect(280, 30, 330, 80))
        self.header_text.setStyleSheet("font: 34pt \"JasmineUPC\";")
        self.header_text.setAlignment(QtCore.Qt.AlignCenter)
        self.header_text.setObjectName("header_text")
        self.scrollArea = QtWidgets.QScrollArea(background_confirm_times_to_take_pill)
        self.scrollArea.setGeometry(QtCore.QRect(50, 150, 700, 200))
        self.scrollArea.setStyleSheet("background-color:rgb(156, 183, 255);\n""border-color:rgb(156, 183, 255);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 698, 198))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")

        self.add_time_button = QtWidgets.QToolButton(background_confirm_times_to_take_pill)
        self.add_time_button.setGeometry(QtCore.QRect(700, 20, 70, 70))
        self.add_time_button.setMinimumSize(QtCore.QSize(70, 70))
        self.add_time_button.setStyleSheet("QToolButton#add_time_button {\n""   font-size: 40px;\n""    background-color:#24BD73;\n""  border-radius: 35px;\n""  color: white;\n""}\n""QToolButton#add_time_button {\n""    font-size: 40px;\n""    background-color:#24BD73;\n""  border-radius: 35px;\n""  color: white;\n""}")
        self.add_time_button.setText("+")
        self.add_time_button.clicked.connect(self.goToInputTimeToTakePillScreen)
        self.add_time_button.setObjectName("add_time_button")
        
        for idx, time in enumerate(self.timesToTakesPillArr) :
            objIndex = self.timesToTakesPillArr.index(time)

            timeToTakePillLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            timeToTakePillLabel.setMinimumSize(QtCore.QSize(250, 0))
            timeToTakePillLabel.setMaximumSize(QtCore.QSize(250, 16777215))
            timeToTakePillLabel.setStyleSheet("background-color: none;\n""font: 75 30pt \"JasmineUPC\";\n""border-radius: 25px;\n""color: #070021;\n""background-color: #C5E1FF;")
            timeToTakePillLabel.setAlignment(QtCore.Qt.AlignCenter)
            timeToTakePillLabel.setText("เวลาที่ " + str(objIndex + 1))
            timeToTakePillLabel.setObjectName("question_time_no" + str(objIndex))
            self.gridLayout.addWidget(timeToTakePillLabel, 9+objIndex, 0, 1, 1)

            timeToTakePillData = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            timeToTakePillData.setStyleSheet("font: 75 34pt \"JasmineUPC\";\n""color: #070021;\n""")
            timeToTakePillData.setText(time)
            timeToTakePillData.setObjectName("show_time_" + str(objIndex))
            self.gridLayout.addWidget(timeToTakePillData, 9+objIndex, 1, 1, 1)

            timeToTakePillEditButton = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
            timeToTakePillEditButton.setIconSize(QtCore.QSize(68, 68))
            timeToTakePillEditButton.setIcon(QtGui.QIcon('../klongyaa/Klongyaa/shared/images/edit2.png'))
            timeToTakePillEditButton.setStyleSheet("background-color : rgb(255, 74, 74); border-radius: 35px;")
    
            timeToTakePillEditButton.setObjectName("button_edit_time_" + str(objIndex))
            
            timeToTakePillEditButton.clicked.connect(partial(self.editTimeToTakePill, idx))

            timeToTakePillEditButton.setText( "🖉")
            self.gridLayout.addWidget(timeToTakePillEditButton, 9+objIndex, 2, 1, 1)


        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.success_button = QtWidgets.QToolButton(background_confirm_times_to_take_pill)
        self.success_button.setGeometry(QtCore.QRect(295, 375, 200, 90))
        self.success_button.setMinimumSize(QtCore.QSize(100, 50))
        self.success_button.setStyleSheet("QToolButton#success_button {\n""       font: 75 36pt \"JasmineUPC\";\n""    background-color:#24BD73;\n""    color: #ffffff;\n""    border-radius:20px;\n""    width: 170px;\n""    height: 100px;\n""}\n""QToolButton#success_button:hover {\n""    font: 75 36pt \"JasmineUPC\";\n""    background-color:#23B36D;\n""    color: #ffffff;\n""    border-radius:20px;\n""    width: 170px;\n""    height:100px;\n""}")
        self.success_button.setObjectName("success_button")

        self.retranslateUi(background_confirm_times_to_take_pill)
        QtCore.QMetaObject.connectSlotsByName(background_confirm_times_to_take_pill)

    def retranslateUi(self, background_confirm_times_to_take_pill):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        channelID = "ช่องที่ " + str(globalPillData["id"] + 1)

        background_confirm_times_to_take_pill.setWindowTitle(_translate("background_confirm_times_to_take_pill", "Dialog"))
        self.no_channel.setText(_translate("background_confirm_times_to_take_pill", channelID))
        self.header_text.setText(_translate("background_confirm_times_to_take_pill", "เวลาที่ต้องทานยา"))
        self.success_button.setText(_translate("background_confirm_times_to_take_pill", "เสร็จสิ้น"))

    def editTimeToTakePill(self, objIndex):
        global globalPillData

        screen = InputTimeToTakePillScreen(globalPillData, objIndex, False)

        time_to_edit = globalPillData['timeToTake'][objIndex]
        del globalPillData['timeToTake'][objIndex]
        hour, minute = map(int, time_to_edit.split(':'))
        screen.selected_hour = hour
        screen.selected_minute = minute

        screen.hour_display.setText(f"{hour:02d}")
        screen.minute_display.setText(f"{minute:02d}")

        __main__.widget.removeWidget(self)
        __main__.widget.addWidget(screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)


    def goToInputTimeToTakePillScreen(self):
        #================ go to add summary time screen ====================#
        global globalPillData

        screen = InputTimeToTakePillScreen(globalPillData, -1, False)
        __main__.widget.removeWidget(self)
        __main__.widget.addWidget(screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)

    def goToPillSummaryScreen(self):
        #================ go to add summary time screen ====================#
        global globalTimesToTakePillArr
        global globalPillData
        globalPillData["timeToTake"] = globalTimesToTakePillArr
        print("\n ไปหน้าสรุป \n")
        print(json.dumps(globalPillData, indent=4))

        add_summary_time_screen = __main__.PillSummaryScreen(globalPillData)
        __main__.widget.removeWidget(self)
        __main__.widget.addWidget(add_summary_time_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)
        resetGlobalData()