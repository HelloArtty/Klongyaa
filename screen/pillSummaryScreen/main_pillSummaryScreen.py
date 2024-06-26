import sys
from screen.pillSummaryScreen.gen.gen_pill_summary_screen import *
from PyQt5.QtWidgets import QDialog, QApplication, QWidget 
from screen.pillSummaryScreen.mock.pill_data import pill_data
from PyQt5 import QtCore, QtGui, QtWidgets 
from shared.main_success_save_screen import SuccessSaveScreen
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QTimer
from screen.inputPillNameScreen.gen.gen_input_voice_screen_again import *

import requests

import __main__

globalPillData = {}
globalInputPillName = ""
mockNum = 0

class PillSummaryScreen(QDialog):
    def __init__(self, pillData):
        super().__init__()
        global globalPillData
        globalPillData = pillData

        self.setupUi(self)
        self.button_save_pill_summary.clicked.connect(self.savePillSummary)

        #----------- SET VARIABLE OF TEXT LABEL ------------#
        unit_pill = " เม็ด"
        unit_time = " น."

        #----------- SET EDIT BUTTON TO CONNECT EACH PAGE -----------#
        self.button_edit_pill_name.clicked.connect(lambda:self.editPillName("pill_name"))
        self.button_edit_amount_pill.clicked.connect(lambda:self.editPillName("amount_pill"))
        self.button_edit_time.clicked.connect(lambda:self.editPillName("time"))

        if globalPillData["totalPills"] > 0 :
                self.button_edit_total_pills.clicked.connect(lambda:self.editPillName("total_pills"))
    #หน้าสรุป
    def setupUi(self, background_summary_screen):
        global globalPillData

        currentRow = 0

        background_summary_screen.setObjectName("background_summary_screen")
        background_summary_screen.resize(800, 480)
        background_summary_screen.setStyleSheet("QWidget#background_summary_screen{\n" "background-color: #97C7F9}")
        self.text_header_summary_screen = QtWidgets.QLabel(background_summary_screen)
        self.text_header_summary_screen.setGeometry(QtCore.QRect(290, 20, 375, 60))
        self.text_header_summary_screen.setStyleSheet("font: 75 34pt \"JasmineUPC\";\n" "")
        self.text_header_summary_screen.setScaledContents(False)
        self.text_header_summary_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.text_header_summary_screen.setWordWrap(False)
        self.text_header_summary_screen.setIndent(50)
        self.text_header_summary_screen.setObjectName("text_header_summary_screen")
        self.scroll_area = QtWidgets.QScrollArea(background_summary_screen)
        self.scroll_area.setGeometry(QtCore.QRect(10, 90, 780, 300))
        self.scroll_area.setMinimumSize(QtCore.QSize(0, 300))
        self.scroll_area.setStyleSheet("background-color:rgb(156, 183, 255);\n" "border-color:rgb(156, 183, 255);\n" "\n" "")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 829, 316))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.question_pill_name = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.question_pill_name.sizePolicy().hasHeightForWidth())
        self.question_pill_name.setSizePolicy(sizePolicy)
        self.question_pill_name.setMinimumSize(QtCore.QSize(250, 35))
        self.question_pill_name.setMaximumSize(QtCore.QSize(2, 100))
        self.question_pill_name.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("JasmineUPC")
        font.setPointSize(30)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.question_pill_name.setFont(font)
        self.question_pill_name.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.question_pill_name.setStyleSheet("background-color: #C5E1FF;\n" "font: 75 30pt \"JasmineUPC\";\n" "border-radius: 25px;\n" "color: #070021;\n" "\n" "")
        self.question_pill_name.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.question_pill_name.setFrameShadow(QtWidgets.QFrame.Plain)
        self.question_pill_name.setScaledContents(False)
        self.question_pill_name.setAlignment(QtCore.Qt.AlignCenter)
        self.question_pill_name.setWordWrap(True)
        self.question_pill_name.setObjectName("question_pill_name")
        self.gridLayout_2.addWidget(self.question_pill_name, currentRow, 0, 1, 1)

        self.show_pill_name = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.show_pill_name.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_pill_name.sizePolicy().hasHeightForWidth())
        self.show_pill_name.setSizePolicy(sizePolicy)
        self.show_pill_name.setMinimumSize(QtCore.QSize(200, 40))
        self.show_pill_name.setStyleSheet("font: 75 32pt \"JasmineUPC\";\n" "color: #070021;\n" "border: none;\n" "margin-right:50px")
        self.show_pill_name.setObjectName("show_pill_name")
        self.gridLayout_2.addWidget(self.show_pill_name, currentRow, 1, 1, 1)

        self.button_edit_pill_name = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
        self.button_edit_pill_name.setIconSize(QtCore.QSize(68, 68))
        self.button_edit_pill_name.setIcon(QtGui.QIcon('/home/klongyaa1/Desktop/GUI-Klongyaa-seniorProject/shared/images/edit2.png'))
        self.button_edit_pill_name.setStyleSheet("background-color : rgb(255, 74, 74); border-radius: 35px;")
        self.button_edit_pill_name.setObjectName("button_edit_pill_name")
        self.gridLayout_2.addWidget(self.button_edit_pill_name, currentRow, 3, 1, 1)

        currentRow = currentRow + 1

        if globalPillData["totalPills"] > 0 :
                self.question_total_pills = QtWidgets.QLabel(self.scrollAreaWidgetContents)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(15)
                sizePolicy.setHeightForWidth(self.question_total_pills.sizePolicy().hasHeightForWidth())
                self.question_total_pills.setSizePolicy(sizePolicy)
                self.question_total_pills.setMinimumSize(QtCore.QSize(20, 30))
                self.question_total_pills.setMaximumSize(QtCore.QSize(360, 16777215))
                self.question_total_pills.setSizeIncrement(QtCore.QSize(0, 0))
                self.question_total_pills.setStyleSheet("background-color: none;\n" "font: 75 30pt \"JasmineUPC\";\n" "border-radius: 25px;\n" "color: #070021;\n" "background-color: #C5E1FF;")
                self.question_total_pills.setTextFormat(QtCore.Qt.AutoText)
                self.question_total_pills.setScaledContents(True)
                self.question_total_pills.setAlignment(QtCore.Qt.AlignCenter)
                self.question_total_pills.setWordWrap(True)
                self.question_total_pills.setText("จำนวนยาทั้งหมด")
                self.question_total_pills.setObjectName("question_total_pills")
                self.gridLayout_2.addWidget(self.question_total_pills, currentRow, 0, 1, 1)

                self.show_total_pills = QtWidgets.QLabel(self.scrollAreaWidgetContents)
                self.show_total_pills.setEnabled(True)
                self.show_total_pills.setMinimumSize(QtCore.QSize(200, 40))
                self.show_total_pills.setStyleSheet("font: 75 34pt \"JasmineUPC\";\n" "color: #070021;\n" "margin-right:50px")
                self.show_total_pills.setText(str(globalPillData["totalPills"]) + " เม็ด")
                self.show_total_pills.setObjectName("show_total_pills")
                self.gridLayout_2.addWidget(self.show_total_pills, currentRow, 1, 1, 1) #fix

                self.button_edit_total_pills = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
                self.button_edit_total_pills.setIconSize(QtCore.QSize(68, 68))
                self.button_edit_total_pills.setIcon(QtGui.QIcon('/home/klongyaa1/Desktop/GUI-Klongyaa-seniorProject/shared/images/edit2.png'))
                self.button_edit_total_pills.setStyleSheet("background-color : rgb(255, 74, 74); border-radius: 35px;")

                self.button_edit_total_pills.setText("🖉")
                self.button_edit_total_pills.setObjectName("button_edit_total_pills")
                self.gridLayout_2.addWidget(self.button_edit_total_pills, currentRow, 3, 1, 1)

                currentRow = currentRow + 1

        self.question_amount_pill = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.question_amount_pill.setMinimumSize(QtCore.QSize(350, 0))
        self.question_amount_pill.setMaximumSize(QtCore.QSize(400, 16777215))
        self.question_amount_pill.setStyleSheet("background-color: none;\n" "font: 75 30pt \"JasmineUPC\";\n" "border-radius: 25px;\n" "color: #070021;\n" "background-color: #C5E1FF;")
        self.question_amount_pill.setAlignment(QtCore.Qt.AlignCenter)
        self.question_amount_pill.setWordWrap(True)
        self.question_amount_pill.setObjectName("question_amount_pill")
        self.gridLayout_2.addWidget(self.question_amount_pill, currentRow, 0, 1, 1)

        self.show_amount_pill = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_amount_pill.sizePolicy().hasHeightForWidth())
        self.show_amount_pill.setSizePolicy(sizePolicy)
        self.show_amount_pill.setStyleSheet("font: 75 34pt \"JasmineUPC\";\n" "color: #070021;\n" "margin-right:50px")
        self.show_amount_pill.setObjectName("show_amount_pill")
        self.gridLayout_2.addWidget(self.show_amount_pill, currentRow, 1, 1, 1)

        self.button_edit_amount_pill = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
        self.button_edit_amount_pill.setIconSize(QtCore.QSize(68, 68))
        self.button_edit_amount_pill.setIcon(QtGui.QIcon('/home/klongyaa1/Desktop/GUI-Klongyaa-seniorProject/shared/images/edit2.png'))
        self.button_edit_amount_pill.setStyleSheet("background-color : rgb(255, 74, 74); border-radius: 35px;")

        self.button_edit_amount_pill.setObjectName("button_edit_amount_pill")
        self.gridLayout_2.addWidget(self.button_edit_amount_pill, currentRow, 3, 1, 1)

        currentRow = currentRow + 1

        self.button_edit_time = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
        self.button_edit_time.setIconSize(QtCore.QSize(68, 68))
        self.button_edit_time.setIcon(QtGui.QIcon('/home/klongyaa1/Desktop/GUI-Klongyaa-seniorProject/shared/images/edit2.png'))
        self.button_edit_time.setStyleSheet("background-color : rgb(255, 74, 74); border-radius: 35px;")

        self.button_edit_time.setObjectName("button_edit_time")
        self.gridLayout_2.addWidget(self.button_edit_time, currentRow, 3, 1, 1)

        for time in globalPillData["timeToTake"] :
                objIndex = globalPillData["timeToTake"].index(time)
                timeToTakePillLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
                timeToTakePillLabel.setMinimumSize(QtCore.QSize(250, 0))
                timeToTakePillLabel.setMaximumSize(QtCore.QSize(250, 16777215))
                timeToTakePillLabel.setStyleSheet("background-color: none;\n" "font: 75 30pt \"JasmineUPC\";\n" "border-radius: 25px;\n" "color: #070021;\n" "background-color: #C5E1FF;")
                timeToTakePillLabel.setAlignment(QtCore.Qt.AlignCenter)
                timeToTakePillLabel.setText("เวลาที่ " + str(objIndex + 1))
                timeToTakePillLabel.setObjectName("question_time_no_" + str(objIndex))
                self.gridLayout_2.addWidget(timeToTakePillLabel, (currentRow + objIndex), 0, 1, 1)

                timeToTakePillData = QtWidgets.QLabel(self.scrollAreaWidgetContents)
                timeToTakePillData.setStyleSheet("font: 75 34pt \"JasmineUPC\";\n" "color: #070021;\n" "")
                timeToTakePillData.setText(time + " น.")
                timeToTakePillData.setObjectName("show_time")
                self.gridLayout_2.addWidget(timeToTakePillData, (currentRow + objIndex), 1, 1, 1)
                 #--------------- CREATE BUTTON FAKE EDIT -------------------------------------------#
                button_fake_edit = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
                button_fake_edit.setMinimumSize(QtCore.QSize(70, 70))
                button_fake_edit.setStyleSheet("QToolButton#button_fake_edit {\n" " font-size: 40px;\n"
"  background-color:rgb(156, 183, 255);\n"
"  border-radius: 35px;\n"
"  color: white;}")
                button_fake_edit.setObjectName("button_fake_edit")
                self.gridLayout_2.addWidget(button_fake_edit, currentRow, 2, 1, 1)
                currentRow = currentRow + 1

        self.scroll_area.setWidget(self.scrollAreaWidgetContents)
        self.button_save_pill_summary = QtWidgets.QToolButton(background_summary_screen)
        self.button_save_pill_summary.setGeometry(QtCore.QRect(280, 400, 220, 75))
        self.button_save_pill_summary.setMinimumSize(QtCore.QSize(100, 50))
        self.button_save_pill_summary.setStyleSheet("QToolButton#button_save_pill_summary {\n" "       font: 75 36pt \"JasmineUPC\";\n" "    background-color:#24BD73;\n" "    color: #ffffff;\n" "    border-radius:20px;\n" "        width: 170px;\n" "    height: 100px;\n" "}\n" "QToolButton#button_save_pill_summary:hover {\n" "    font: 75 36pt \"JasmineUPC\";\n" "    background-color:#23B36D;\n" "    color: #ffffff;\n" "    border-radius:20px;\n" "        width: 170px;\n" "    height: 100px;\n" "}")
        self.button_save_pill_summary.setObjectName("button_save_pill_summary")
        self.no_channel = QtWidgets.QLabel(background_summary_screen)
        self.no_channel.setGeometry(QtCore.QRect(40, 10, 190, 70))
        font = QtGui.QFont()
        font.setFamily("JasmineUPC")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF;\n" "font: 75 36pt \"JasmineUPC\";\n" "border-radius: 25px;\n" "color: #070021;\n" "")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")

        self.retranslateUi(background_summary_screen)
        QtCore.QMetaObject.connectSlotsByName(background_summary_screen)

    def retranslateUi(self, background_summary_screen):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        pillName = globalPillData["name"]
        pillsPerTime = str(globalPillData["pillsPerTime"]) + " เม็ด/มื้อ"
        channelID = "ช่องที่ " + str(globalPillData["id"] + 1)

        
        background_summary_screen.setWindowTitle(_translate("background_summary_screen", "Dialog"))
        self.text_header_summary_screen.setText(_translate("background_summary_screen", "ข้อมูลของยาที่ต้องทาน"))
        self.show_pill_name.setText(_translate("background_summary_screen", pillName))
        self.show_amount_pill.setText(_translate("background_summary_screen", pillsPerTime))
        self.button_edit_time.setText(_translate("background_summary_screen", "🖉"))
        self.button_edit_pill_name.setText(_translate("background_summary_screen", "🖉"))
        
        self.question_amount_pill.setText(_translate("background_summary_screen", "จำนวนยาที่ต้องทาน"))
        self.button_edit_amount_pill.setText(_translate("background_summary_screen", "🖉"))
        self.question_pill_name.setText(_translate("background_summary_screen", "ชื่อยา"))
        
        self.button_save_pill_summary.setText(_translate("background_summary_screen", "บันทึก"))
        self.no_channel.setText(_translate("background_summary_screen", channelID))

    # def savePillSummary(self,edit_mode): * อย่าเพิ่งลบคอมเม้นท์
    def savePillSummary(self):
        #----------- SAVE AND THEN GO TO HOME SCREEN -----------#
        global globalPillData
        success_save_screen = SuccessSaveScreen(globalPillData)
        res = requests.post(__main__.config["url"] + "/pill-data/addPillChannelData", json={
                "channelID": str(globalPillData["id"]),
                "pillName": globalPillData["name"],
                "pillsPerTime": globalPillData["pillsPerTime"],
                "stock": str(globalPillData["totalPills"]),
                "takeTimes": globalPillData["timeToTake"],
                "total": str(globalPillData["totalPills"]),
                "lineID": __main__.config["userId"]           
        })
        # self.ui.text_screen_name.setText("Home screen")
        __main__.widget.removeWidget(self)
        __main__.widget.addWidget(success_save_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)

    def editPillName(self, edit_mode):
    # def editPillName(self):  * อย่าเพิ่งลบคอมเม้นท์
        global globalPillData
        
        if edit_mode == "pill_name" :
            screen = InputPillNameScreen(globalPillData)
        if edit_mode == "total_pills" :
            screen = TotalPillsScreen()
        if edit_mode == "amount_pill" :
            screen = AmountPillPerTimeScreen()
        if edit_mode == "time" :
            screen = __main__.AddSummaryTimeScreen(globalPillData)

        __main__.widget.addWidget(screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)


# ########### WAVE LOADING SCREEN ############
class LoadingVoiceScreen(QDialog):
    def __init__(self, nextPage):
        super().__init__()
        self.setupUi(self)
        self.nextPage = nextPage

    def setupUi(self, background_voice_loading):
        background_voice_loading.setObjectName("background_voice_loading")
        background_voice_loading.resize(800, 480)
        background_voice_loading.setStyleSheet("QWidget#background_voice_loading{\n" "background-color: #97C7F9}")
        self.frame_of_loading = QtWidgets.QFrame(background_voice_loading)
        self.frame_of_loading.setGeometry(QtCore.QRect(40, 40, 720, 400))
        self.frame_of_loading.setStyleSheet("background-color: rgb(255, 255, 255);\n" "border-radius:40px")
        self.frame_of_loading.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_of_loading.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_of_loading.setObjectName("frame_of_loading")
        self.label_voice_gif = QtWidgets.QLabel(self.frame_of_loading)
        self.label_voice_gif.setGeometry(QtCore.QRect(60, 30, 600, 230))
        self.label_voice_gif.setStyleSheet("background-color: #ffffff;\n" "font: 75 36pt \"JasmineUPC\";")
        self.label_voice_gif.setAlignment(QtCore.Qt.AlignCenter)
        self.label_voice_gif.setObjectName("label_voice_gif")
        self.text_of_waiting_process = QtWidgets.QLabel(self.frame_of_loading)
        self.text_of_waiting_process.setGeometry(QtCore.QRect(75, 280, 580, 60))
        self.text_of_waiting_process.setStyleSheet("font: 34pt \"JasmineUPC\";")
        self.text_of_waiting_process.setObjectName("text_of_waiting_process")

        self.retranslateUi(background_voice_loading)
        QtCore.QMetaObject.connectSlotsByName(background_voice_loading)

    def retranslateUi(self, background_voice_loading):
        _translate = QtCore.QCoreApplication.translate
        background_voice_loading.setWindowTitle(_translate("background_voice_loading", "Dialog"))
        self.label_voice_gif.setText(_translate("background_voice_loading", "sound loading gif"))
        self.text_of_waiting_process.setText(_translate("background_voice_loading", "ระบบกำลังประมวลผล โปรดรอสักครู่"))

        #================ set voice loading gif ====================#
        self.movie = QMovie('shared/images/sound.gif')
        self.label_voice_gif.setMovie(self.movie)
        #================ set delay 2 second ====================#
        timer = QTimer(self)
        self.startAnimation()
        timer.singleShot(2000, self.stopAnimation)
        self.show()

    def startAnimation(self):
        self.movie.start()

    def stopAnimation(self):
        self.movie.stop()
        self.close()
        __main__.widget.addWidget(self.nextPage)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)


# ########### INPUT PILL NAME FLOW CLASS ############
class InputPillNameScreen(QDialog):
    def __init__(self, pillData):
        super().__init__()
        global globalPillData
        globalPillData = pillData
        self.setupUi(self)
    #========================= 
    def clickVoiceButton(self):
        global globalPillData
        global globalInputPillName

        voiceInput = __main__.speech_recog_function()
        globalInputPillName = voiceInput

        loading_screen = LoadingVoiceScreen(ConfirmPillNameScreen(globalInputPillName))
        __main__.widget.addWidget(loading_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)
    
    def setupUi(self, background_input_pil_name):
        background_input_pil_name.setObjectName("background_input_pil_name")
        background_input_pil_name.resize(800, 480)
        background_input_pil_name.setStyleSheet("QWidget#background_input_pil_name{\n" "background-color: #97C7F9}")
        self.no_channel = QtWidgets.QLabel(background_input_pil_name)
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 190, 70))
        font = QtGui.QFont()
        font.setFamily("JasmineUPC")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF;\n" "font: 75 36pt \"JasmineUPC\";\n" "border-radius: 25px;\n" "color: #070021;\n" "")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")
        self.question_input_voice = QtWidgets.QLabel(background_input_pil_name)
        self.question_input_voice.setGeometry(QtCore.QRect(130, 110, 540, 200))
        self.question_input_voice.setStyleSheet("font: 34pt \"JasmineUPC\";")
        self.question_input_voice.setAlignment(QtCore.Qt.AlignCenter)
        self.question_input_voice.setObjectName("question_input_voice")
        self.button_input_voice = QtWidgets.QToolButton(background_input_pil_name)
        self.button_input_voice.setGeometry(QtCore.QRect(330, 300, 140, 125))
        self.button_input_voice.setStyleSheet("QToolButton#button_input_voice {\n" "   background-image: url(:/newPrefix/mic_icon.png); \n" "   border-radius: 35;\n" "   width:30px;\n" "}\n" "QToolButton#button_input_voice:hover {\n" "    background-color:#24BD73;\n" "    background-image: url(:/newPrefix/mic_icon.png);\n" "   border-radius: 35;\n" "   background-color:#B9D974;\n" "    width: 170px;\n" "    height: 100px;\n" "}")
        self.button_input_voice.setText("")
        self.button_input_voice.setObjectName("button_input_voice")
        self.button_input_voice.clicked.connect(self.clickVoiceButton)

        self.retranslateUi(background_input_pil_name)
        QtCore.QMetaObject.connectSlotsByName(background_input_pil_name)

    def retranslateUi(self, background_input_pil_name):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        channelID = "ช่องที่ " + str(globalPillData["id"] + 1)
        background_input_pil_name.setWindowTitle(_translate("background_input_pil_name", "Dialog"))
        self.no_channel.setText(_translate("background_input_pil_name", channelID))
        self.question_input_voice.setText(_translate("background_input_pil_name", "ดำเนินการกดปุ่ม \n" " เพื่อพูดชื่อยาของท่าน"))

import screen.inputPillNameScreen.gen.mic_icon

class ConfirmPillNameScreen(QDialog):
    def __init__(self, inputPillName):
        super().__init__()
        self.inputPillName = inputPillName
        self.setupUi(self)
        #================ click button correct or incorrect ====================#
        self.button_correct_pill_name.clicked.connect(self.clickCorrectButton)
        self.button_incorrect_pill_name.clicked.connect(self.clickIncorrectButton)

    def setupUi(self, background_confirm_pill_name):
        background_confirm_pill_name.setObjectName("background_confirm_pill_name")
        background_confirm_pill_name.resize(800, 480)
        background_confirm_pill_name.setStyleSheet("QWidget#background_confirm_pill_name{\n" "background-color: #97C7F9}")
        self.no_channel = QtWidgets.QLabel(background_confirm_pill_name)
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 190, 70))
        font = QtGui.QFont()
        font.setFamily("JasmineUPC")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF;\n" "font: 75 36pt \"JasmineUPC\";\n" "border-radius: 25px;\n" "color: #070021;\n" "")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")
        self.label_1 = QtWidgets.QLabel(background_confirm_pill_name)
        self.label_1.setGeometry(QtCore.QRect(315, 120, 170, 80))
        self.label_1.setStyleSheet("font:42pt \"JasmineUPC\";")
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName("label_1")
        self.show_pill_name = QtWidgets.QLabel(background_confirm_pill_name)
        self.show_pill_name.setGeometry(QtCore.QRect(120, 220, 560, 80))
        self.show_pill_name.setStyleSheet("font: 52pt \"JasmineUPC\";")
        self.show_pill_name.setAlignment(QtCore.Qt.AlignCenter)
        self.show_pill_name.setObjectName("show_pill_name")
        self.button_correct_pill_name = QtWidgets.QToolButton(background_confirm_pill_name)
        self.button_correct_pill_name.setGeometry(QtCore.QRect(100, 340, 250, 90))
        self.button_correct_pill_name.setStyleSheet("\n" "\n" "QToolButton#button_correct_pill_name {\n" "       font: 75 36pt \"JasmineUPC\";\n" "   background-color:#24BD73;\n" "   color: #ffffff;\n" "   border-radius:20px;\n" "}\n" "QToolButton#button_correct_pill_name:hover {\n" "    font: 75 36pt \"JasmineUPC\";\n" "    background-color:#23B36D;\n" "    color: #ffffff;\n" "    border-radius:20px;\n" "    width: 170px;\n" "    height:100px;\n" "}")
        self.button_correct_pill_name.setObjectName("button_correct_pill_name")
        self.button_incorrect_pill_name = QtWidgets.QToolButton(background_confirm_pill_name)
        self.button_incorrect_pill_name.setGeometry(QtCore.QRect(440, 340, 250, 90))
        self.button_incorrect_pill_name.setStyleSheet("QToolButton#button_incorrect_pill_name {\n" "       font: 75 36pt \"JasmineUPC\";\n" "    background-color: #DD5D5D;\n" "      border-radius:20px;\n" "    color: white;\n" "}\n" "QToolButton#button_incorrect_pill_name:hover {\n" "       font: 75 36pt \"JasmineUPC\";\n" "    background-color: rgb(255, 50, 50);\n" "      border-radius:20px;\n" "    color: white;\n" "}")
        self.button_incorrect_pill_name.setObjectName("button_incorrect_pill_name")

        self.retranslateUi(background_confirm_pill_name)
        QtCore.QMetaObject.connectSlotsByName(background_confirm_pill_name)

    def retranslateUi(self, background_confirm_pill_name):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        channelID = "ช่องที่ " + str(globalPillData["id"] + 1)

        background_confirm_pill_name.setWindowTitle(_translate("background_confirm_pill_name", "Dialog"))
        self.no_channel.setText(_translate("background_confirm_pill_name", channelID))
        self.label_1.setText(_translate("background_confirm_pill_name", "ชื่อยา"))
        self.show_pill_name.setText(_translate("background_confirm_pill_name", self.inputPillName))
        self.button_correct_pill_name.setText(_translate("background_confirm_pill_name", "ถูกต้อง"))
        self.button_incorrect_pill_name.setText(_translate("background_confirm_pill_name", "ไม่ถูกต้อง"))

    def clickCorrectButton(self):
        global globalPillData
        globalPillData["name"] = globalInputPillName

        total_pill_screen = PillSummaryScreen(globalPillData)
        __main__.widget.addWidget(total_pill_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)

    def clickIncorrectButton(self):
        input_voice_again = InputVoiceAgain()
        __main__.widget.addWidget(input_voice_again)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)

class InputVoiceAgain(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_input_voice_again()
        self.ui.setupUi(self)
        self.ui.button_input_voice_again.clicked.connect(self.clickVoiceButtonAgain)

    def setupUi(self, bankground_input_voice_again):
        bankground_input_voice_again.setObjectName("bankground_input_voice_again")
        bankground_input_voice_again.resize(800, 480)
        bankground_input_voice_again.setStyleSheet("QWidget#bankground_input_voice_again{\n" "background-color: #97C7F9}")
        self.frame_of_input_voice_again = QtWidgets.QFrame(bankground_input_voice_again)
        self.frame_of_input_voice_again.setGeometry(QtCore.QRect(40, 40, 720, 400))
        self.frame_of_input_voice_again.setStyleSheet("background-color: rgb(255, 255, 255);\n" "border-radius:40px")
        self.frame_of_input_voice_again.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_of_input_voice_again.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_of_input_voice_again.setObjectName("frame_of_input_voice_again")
        self.question_of_input_voice_again = QtWidgets.QLabel(self.frame_of_input_voice_again)
        self.question_of_input_voice_again.setGeometry(QtCore.QRect(185, 120, 340, 60))
        self.question_of_input_voice_again.setStyleSheet("font: 34pt \"JasmineUPC\";")
        self.question_of_input_voice_again.setAlignment(QtCore.Qt.AlignCenter)
        self.question_of_input_voice_again.setObjectName("question_of_input_voice_again")
        self.button_input_voice_again = QtWidgets.QToolButton(self.frame_of_input_voice_again)
        self.button_input_voice_again.setGeometry(QtCore.QRect(290, 230, 140, 125))
        self.button_input_voice_again.setStyleSheet("QToolButton#button_input_voice_again {\n" "   background-image: url(:/newPrefix/mic_icon.png); \n" "   border-radius: 35;\n" "   width:30px;\n" "}\n" "QToolButton#button_input_voice_again:hover {\n" "    background-color:#24BD73;\n" "    background-image: url(:/newPrefix/mic_icon.png);\n" "   border-radius: 35;\n" "   background-color:#B9D974;\n" "    width: 170px;\n" "    height: 100px;\n" "}")
        self.button_input_voice_again.setText("")
        self.button_input_voice_again.setObjectName("button_input_voice_again")

        self.retranslateUi(bankground_input_voice_again)
        QtCore.QMetaObject.connectSlotsByName(bankground_input_voice_again)

    def retranslateUi(self, bankground_input_voice_again):
        _translate = QtCore.QCoreApplication.translate
        bankground_input_voice_again.setWindowTitle(_translate("bankground_input_voice_again", "Dialog"))
        self.question_of_input_voice_again.setText(_translate("bankground_input_voice_again", "กรุณาพูดชื่อยาอีกครั้ง"))

    import screen.inputPillNameScreen.gen.mic_icon

    def clickVoiceButtonAgain(self):
        global globalInputPillName
        nameIdx = int(globalInputPillName.split(' ')[-1]) + 1
        globalInputPillName =  "พาราเซตาม่อน " + str(nameIdx)
        loading_screen = LoadingVoiceScreen(ConfirmPillNameScreen(globalInputPillName))
        __main__.widget.addWidget(loading_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)


# ########### INPUT TOTAL PILL FLOW CLASS ############
class TotalPillsScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #======================= set max-min of total pills =======================#
        self.slider_total_pills.setMaximum(30)
        self.slider_total_pills.setMinimum(0)
        self.slider_total_pills.valueChanged.connect(self.updateSliderTotalPills)
        self.button_save_total_pills.clicked.connect(lambda: self.saveTotalPills())
        
    def setupUi(self, background_total_pills):
        background_total_pills.setObjectName("background_total_pills")
        background_total_pills.resize(800, 480)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        background_total_pills.setFont(font)
        background_total_pills.setStyleSheet("QWidget#background_total_pills{\n" "background-color: #97C7F9}")
        self.no_channel = QtWidgets.QLabel(background_total_pills)
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 190, 70))
        font = QtGui.QFont()
        font.setFamily("JasmineUPC")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF;\n" "font: 75 36pt \"JasmineUPC\";\n" "border-radius: 25px;\n" "color: #070021;\n" "")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")
        self.text_question_inputting_total_pills = QtWidgets.QLabel(background_total_pills)
        self.text_question_inputting_total_pills.setGeometry(QtCore.QRect(95, 90, 610, 80))
        self.text_question_inputting_total_pills.setStyleSheet("font: 34pt \"JasmineUPC\";")
        self.text_question_inputting_total_pills.setObjectName("text_question_inputting_total_pills")
        self.lcdNumber = QtWidgets.QLCDNumber(background_total_pills)
        self.lcdNumber.setGeometry(QtCore.QRect(210, 180, 370, 130))
        self.lcdNumber.setStyleSheet("background-color: #ffffff;")
        self.lcdNumber.setObjectName("lcdNumber")
        self.slider_total_pills = QtWidgets.QSlider(background_total_pills)
        self.slider_total_pills.setGeometry(QtCore.QRect(100, 330, 600, 30))
        self.slider_total_pills.setStyleSheet("QSlider{\n" "border-radius: 10px ;\n" "}\n" "\n" "QSlider::groove:horizontal{\n" "border: 10px ;\n" "height: 15px;\n" "background: #1C84A9;\n" "}\n" "\n" "QSlider::handle:horizontal{\n" "background: #1C84A9;\n" "border: 10px ;\n" "width: 25px;\n" "margin: -8px 0;\n" "border-radius: 10px;\n" "}\n" "QSlider::add-page:horizontal{\n" "background-color: white;\n" "border: 10px;\n" "}")
        self.slider_total_pills.setSliderPosition(0)
        self.slider_total_pills.setOrientation(QtCore.Qt.Horizontal)
        self.slider_total_pills.setObjectName("slider_total_pills")
        self.button_save_total_pills = QtWidgets.QToolButton(background_total_pills)
        self.button_save_total_pills.setGeometry(QtCore.QRect(295, 375, 250, 90))
        self.button_save_total_pills.setStyleSheet("font: 75 36pt \"JasmineUPC\";\n" "background-color:#24BD73;\n" "color: #ffffff;\n" "border-radius:20px;")
        self.button_save_total_pills.setObjectName("button_save_total_pills")

        self.retranslateUi(background_total_pills)
        QtCore.QMetaObject.connectSlotsByName(background_total_pills)

    def retranslateUi(self, background_total_pills):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        channelID = "ช่องที่ " + str(globalPillData["id"] + 1)
        
        background_total_pills.setWindowTitle(_translate("background_total_pills", "Dialog"))
        self.no_channel.setText(_translate("background_total_pills", channelID))
        self.text_question_inputting_total_pills.setText(_translate("background_total_pills", "กรุณาระบุจำนวนเม็ดยาทั้งหมดที่บรรจุ"))
        self.button_save_total_pills.setText(_translate("background_total_pills", "บันทึก"))

    #======================= define function : update slibar =======================#
    def updateSliderTotalPills(self,count_of_total_pills):
        self.lcdNumber.display(count_of_total_pills)
        self.total_pills = count_of_total_pills

    #======================= define function : Go to amount pill per time =======================#
    def saveTotalPills(self):
        if hasattr(self, 'total_pills'):
            global globalPillData
            globalPillData["totalPills"] = self.total_pills

            screen = PillSummaryScreen(globalPillData)
            __main__.widget.addWidget(screen)
            __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)


# ########### INPUT PILLS PER TIME FLOW CLASS ############
class AmountPillPerTimeScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    #======================= set min-max of amount pill per time screen =======================#
        self.slider_amount_pill_per_time.setMaximum(10)
        self.slider_amount_pill_per_time.setMinimum(0)
        self.slider_amount_pill_per_time.valueChanged.connect(self.updateSliderPillPerTime)
        self.button_next.clicked.connect(self.savePillsPerTimeData)
          
    def setupUi(self, background_amount_pill_per_time):
        background_amount_pill_per_time.setObjectName("background_amount_pill_per_time")
        background_amount_pill_per_time.resize(800, 480)
        background_amount_pill_per_time.setStyleSheet("QWidget#background_amount_pill_per_time{\n" "background-color: #97C7F9}")
        self.no_channel = QtWidgets.QLabel(background_amount_pill_per_time)
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 190, 70))
        font = QtGui.QFont()
        font.setFamily("JasmineUPC")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF;\n" "font: 75 36pt \"JasmineUPC\";\n" "border-radius: 25px;\n" "color: #070021;\n" "")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")
        self.text_question_amount_pill_per_time = QtWidgets.QLabel(background_amount_pill_per_time)
        self.text_question_amount_pill_per_time.setGeometry(QtCore.QRect(40, 100, 720, 80))
        self.text_question_amount_pill_per_time.setStyleSheet("font: 34pt \"JasmineUPC\";")
        self.text_question_amount_pill_per_time.setObjectName("text_question_amount_pill_per_time")
        self.lcdNumberPillPerTime = QtWidgets.QLCDNumber(background_amount_pill_per_time)
        self.lcdNumberPillPerTime.setGeometry(QtCore.QRect(210, 180, 370, 130))
        self.lcdNumberPillPerTime.setStyleSheet("background-color: #ffffff;")
        self.lcdNumberPillPerTime.setObjectName("lcdNumberPillPerTime")
        self.slider_amount_pill_per_time = QtWidgets.QSlider(background_amount_pill_per_time)
        self.slider_amount_pill_per_time.setGeometry(QtCore.QRect(100, 330, 600, 30))
        self.slider_amount_pill_per_time.setStyleSheet("QSlider{\n" "border-radius: 10px ;\n" "}\n" "\n" "QSlider::groove:horizontal{\n" "border: 10px ;\n" "height: 15px;\n" "background: #1C84A9;\n" "}\n" "\n" "QSlider::handle:horizontal{\n" "background: #1C84A9;\n" "border: 10px ;\n" "width: 25px;\n" "margin: -8px 0;\n" "border-radius: 10px;\n" "}\n" "QSlider::add-page:horizontal{\n" "background-color: white;\n" "border: 10px;\n" "}")
        self.slider_amount_pill_per_time.setSliderPosition(0)
        self.slider_amount_pill_per_time.setOrientation(QtCore.Qt.Horizontal)
        self.slider_amount_pill_per_time.setObjectName("slider_amount_pill_per_time")
        self.button_next = QtWidgets.QToolButton(background_amount_pill_per_time)
        self.button_next.setGeometry(QtCore.QRect(295, 375, 250, 90))
        self.button_next.setStyleSheet("font: 75 36pt \"JasmineUPC\";\n" "background-color:#24BD73;\n" "color: #ffffff;\n" "border-radius:20px;")
        self.button_next.setObjectName("button_next")

        self.retranslateUi(background_amount_pill_per_time)
        QtCore.QMetaObject.connectSlotsByName(background_amount_pill_per_time)

    def retranslateUi(self, background_amount_pill_per_time):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        channelID = "ช่องที่ " + str(globalPillData["id"] + 1)

        background_amount_pill_per_time.setWindowTitle(_translate("background_amount_pill_per_time", "Dialog"))
        self.no_channel.setText(_translate("background_amount_pill_per_time", channelID))
        self.text_question_amount_pill_per_time.setText(_translate("background_amount_pill_per_time", "กรุณาระบุจำนวนเม็ดยาที่ต้องทานในเเต่ละมื้อ"))
        self.button_next.setText(_translate("background_amount_pill_per_time", "ถัดไป"))

    #======================= define function : update slibar =======================#
    def updateSliderPillPerTime(self,amount_of_pill_per_time):
        self.lcdNumberPillPerTime.display(amount_of_pill_per_time)
        self.amount_pill =  amount_of_pill_per_time
        #======================= add amount pill per time data to array object =======================#

    def savePillsPerTimeData(self):
        if hasattr(self, 'amount_pill') :
            global globalPillData
            globalPillData["pillsPerTime"] = self.amount_pill

            input_times_to_take_pill_screen = PillSummaryScreen(globalPillData)
            __main__.widget.addWidget(input_times_to_take_pill_screen)
            __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)


# ########### INPUT TIMES TO TAKE PILL FLOW CLASS ############
globalTimesToTakePillArr = []
mockTime = 12
    
if __name__ == "__main__":
     app = QApplication(sys.argv)
     screen = PillSummaryScreen()
     widget = QtWidgets.QStackedWidget()
     widget.setWindowTitle("GUI - KLONG_YAA")
     widget.addWidget(screen)
     widget.setFixedWidth(1024)
     widget.setFixedHeight(600)
     widget.show()
     sys.exit(app.exec_())	
try:
    sys.exit(app.exec_())
except:
    print("Exiting")