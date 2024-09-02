import json
import sys
from functools import partial

import __main__
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QDialog, QWidget
from screen.inputPillNameScreen.gen.gen_input_voice_screen_again import *
from screen.pillSummaryScreen.gen.gen_pill_summary_screen import *
from screen.pillSummaryScreen.mock.pill_data import pill_data
from shared.main_success_save_screen import SuccessSaveScreen

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
        if globalPillData["totalPills"] > 0 :
                self.button_edit_total_pills.clicked.connect(lambda:self.editPillName("total_pills"))
        self.button_edit_time.clicked.connect(lambda:self.editPillName("time"))


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
        self.button_edit_pill_name.setIcon(QtGui.QIcon('../klongyaa/Klongyaa/shared/images/edit2.png'))
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
                self.button_edit_total_pills.setIcon(QtGui.QIcon('../klongyaa/Klongyaa/shared/images/edit2.png'))
                self.button_edit_total_pills.setStyleSheet("background-color : rgb(255, 74, 74); border-radius: 35px;")

                self.button_edit_total_pills.setText("🖉")
                self.button_edit_total_pills.setObjectName("button_edit_total_pills")
                self.gridLayout_2.addWidget(self.button_edit_total_pills, currentRow, 3, 1, 1)

                currentRow = currentRow + 1

        self.button_edit_pill_name = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
        self.button_edit_pill_name.setIconSize(QtCore.QSize(68, 68))
        self.button_edit_pill_name.setIcon(QtGui.QIcon('../klongyaa/Klongyaa/shared/images/edit2.png'))
        self.button_edit_pill_name.setStyleSheet("background-color : rgb(255, 74, 74); border-radius: 35px;")
        self.button_edit_pill_name.setObjectName("button_edit_pill_name")
        self.gridLayout_2.addWidget(self.button_edit_pill_name, currentRow, 3, 1, 1)
        
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
        self.button_edit_amount_pill.setIcon(QtGui.QIcon('../klongyaa/Klongyaa/shared/images/edit2.png'))
        self.button_edit_amount_pill.setStyleSheet("background-color : rgb(255, 74, 74); border-radius: 35px;")
        self.button_edit_amount_pill.setObjectName("button_edit_amount_pill")
        self.gridLayout_2.addWidget(self.button_edit_amount_pill, currentRow, 3, 1, 1)
        
        self.button_edit_total_pills = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
        self.button_edit_total_pills.setIconSize(QtCore.QSize(68, 68))
        self.button_edit_total_pills.setIcon(QtGui.QIcon('../klongyaa/Klongyaa/shared/images/edit2.png'))
        self.button_edit_total_pills.setStyleSheet("background-color : rgb(255, 74, 74); border-radius: 35px;")
        self.button_edit_total_pills.setText("🖉")
        self.button_edit_total_pills.setObjectName("button_edit_total_pills")
        self.gridLayout_2.addWidget(self.button_edit_total_pills, currentRow, 3, 1, 1)
        
        currentRow = currentRow + 1

        self.button_edit_time = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
        self.button_edit_time.setIconSize(QtCore.QSize(68, 68))
        self.button_edit_time.setIcon(QtGui.QIcon('../klongyaa/Klongyaa/shared/images/edit2.png'))
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
        self.button_edit_amount_pill.setText(_translate("background_summary_screen", "🖉"))
        self.question_pill_name.setText(_translate("background_summary_screen", "ชื่อยา"))
        self.question_amount_pill.setText(_translate("background_summary_screen", "จำนวนยาที่ต้องทาน")) 
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
            screen = PillNameScreen(globalPillData)
        if edit_mode == "total_pills" :
            screen = TotalPillsScreen(globalPillData)
        if edit_mode == "amount_pill" :
            screen = AmountPillPerTimeScreen(globalPillData)
        if edit_mode == "time" :
            screen = __main__.AddSummaryTimeScreen(globalPillData)

        __main__.widget.addWidget(screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)

# ########### ชื่อยา ############
class PillNameScreen(QDialog):
    def __init__(self, pillData=None, pillNames=None, parent=None):
        super().__init__(parent)
        global globalPillData
        globalPillData = pillData if pillData is not None else {}
        self.pillNames = pillNames if pillNames is not None else []
        self.inputPillName = globalPillData.get("name", "")
        self.setupUi(self)

    def setupUi(self, background_confirm_pill_name):
        background_confirm_pill_name.setObjectName("background_confirm_pill_name")
        background_confirm_pill_name.resize(800, 480)
        background_confirm_pill_name.setStyleSheet("QWidget#background_confirm_pill_name { background-color: #97C7F9 }")

        self.no_channel = QtWidgets.QLabel(background_confirm_pill_name)
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 190, 70))
        font = QtGui.QFont()
        font.setFamily("JasmineUPC")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF; font: 75 36pt \"JasmineUPC\"; border-radius: 25px; color: #070021;")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")

        self.label_1 = QtWidgets.QLabel(background_confirm_pill_name)
        self.label_1.setGeometry(QtCore.QRect(245, 30, 350, 70))
        self.label_1.setStyleSheet("font: 34pt \"JasmineUPC\";")
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName("label_1")
        
        # Label to display the selected pill name
        self.label_pill_name = QtWidgets.QLabel(background_confirm_pill_name)
        self.label_pill_name.setGeometry(QtCore.QRect(222, 150, 350, 75))
        self.label_pill_name.setStyleSheet("font: 34pt \"JasmineUPC\";")
        self.label_pill_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pill_name.setObjectName("label_pill_name")
        

        # Set initial selection
        self.current_pill_index = 0
        self.label_pill_name.setText(self.pillNames[self.current_pill_index])

        # Left arrow button
        self.btn_left = QtWidgets.QPushButton(background_confirm_pill_name)
        self.btn_left.setGeometry(QtCore.QRect(100, 150, 100, 75))
        self.btn_left.setText("<")
        self.btn_left.setStyleSheet("font: 34pt \"JasmineUPC\";")
        self.btn_left.setObjectName("btn_left")

        # Right arrow button
        self.btn_right = QtWidgets.QPushButton(background_confirm_pill_name)
        self.btn_right.setGeometry(QtCore.QRect(600, 150, 100, 75))
        self.btn_right.setText(">")
        self.btn_right.setStyleSheet("font: 34pt \"JasmineUPC\";")
        self.btn_right.setObjectName("btn_right")

        # Connect buttons to functions
        self.btn_left.clicked.connect(self.navigate_left)
        self.btn_right.clicked.connect(self.navigate_right)

        self.button_correct_pill_name = QtWidgets.QToolButton(background_confirm_pill_name)
        self.button_correct_pill_name.setGeometry(QtCore.QRect(295, 375, 200, 90))
        self.button_correct_pill_name.setStyleSheet("QToolButton#button_correct_pill_name { font: 75 36pt \"JasmineUPC\"; background-color:#24BD73; color: #ffffff; border-radius:20px; } QToolButton#button_correct_pill_name:hover { font: 75 36pt \"JasmineUPC\"; background-color:#23B36D; color: #ffffff; border-radius:20px; }")
        self.button_correct_pill_name.setObjectName("button_correct_pill_name")
        self.button_correct_pill_name.clicked.connect(self.clickCorrectButton)


        self.retranslateUi(background_confirm_pill_name)
        QtCore.QMetaObject.connectSlotsByName(background_confirm_pill_name)
        
    def navigate_left(self):
        if self.current_pill_index > 0:
            self.current_pill_index -= 1
        else:
            self.current_pill_index = len(self.pillNames) - 1
        self.label_pill_name.setText(self.pillNames[self.current_pill_index])

    def navigate_right(self):
        if self.current_pill_index < len(self.pillNames) - 1:
            self.current_pill_index += 1
        else:
            self.current_pill_index = 0
        self.label_pill_name.setText(self.pillNames[self.current_pill_index])

    def retranslateUi(self, background_confirm_pill_name):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        channelID = "ช่องที่ " + str(globalPillData.get("id", 0) + 1)

        background_confirm_pill_name.setWindowTitle(_translate("background_confirm_pill_name", "Dialog"))
        self.no_channel.setText(_translate("background_confirm_pill_name", channelID))
        self.label_1.setText(_translate("background_confirm_pill_name", "กรุณาเลือกชื่อยาของท่าน"))
        self.button_correct_pill_name.setText(_translate("background_confirm_pill_name", "ถัดไป"))
        
    def clickCorrectButton(self):
        global globalPillData
        globalPillData["name"] = globalInputPillName

        total_pill_screen = PillSummaryScreen(globalPillData)
        __main__.widget.addWidget(total_pill_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)


# ########### ยาทั้งหมด ############
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


# ########### จำนวนยาต่อมื้อ ############
class AmountPillPerTimeScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    #======================= set min-max of amount pill per time screen =======================#
        self.slider_amount_pill_per_time.setMaximum(10)
        self.slider_amount_pill_per_time.setMinimum(0)
        self.slider_amount_pill_per_time.valueChanged.connect(self.updateSliderPillPerTime)
        self.button_next.clicked.connect(self.gotoInputTimesToTakePill)

    def setupUi(self, background_amount_pill_per_time):
        background_amount_pill_per_time.setObjectName("background_amount_pill_per_time")
        background_amount_pill_per_time.resize(800, 480)
        background_amount_pill_per_time.setStyleSheet("QWidget#background_amount_pill_per_time{\n"
"background-color: #97C7F9}")
        self.no_channel = QtWidgets.QLabel(background_amount_pill_per_time)
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 190, 70))
        font = QtGui.QFont()
        font.setFamily("JasmineUPC")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF;\n"
"font: 75 36pt \"JasmineUPC\";\n"
"border-radius: 25px;\n"
"color: #070021;\n"
"")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")
        self.text_question_amount_pill_per_time = QtWidgets.QLabel(background_amount_pill_per_time)
        self.text_question_amount_pill_per_time.setGeometry(QtCore.QRect(85, 105, 650, 70))
        self.text_question_amount_pill_per_time.setStyleSheet("font: 40pt \"JasmineUPC\";")
        self.text_question_amount_pill_per_time.setObjectName("text_question_amount_pill_per_time")
        self.lcdNumberPillPerTime = QtWidgets.QLCDNumber(background_amount_pill_per_time)
        self.lcdNumberPillPerTime.setGeometry(QtCore.QRect(210, 180, 370, 130))
        self.lcdNumberPillPerTime.setStyleSheet("background-color: #ffffff;")
        self.lcdNumberPillPerTime.setObjectName("lcdNumberPillPerTime")
        self.slider_amount_pill_per_time = QtWidgets.QSlider(background_amount_pill_per_time)
        self.slider_amount_pill_per_time.setGeometry(QtCore.QRect(100, 330, 600, 30))
        self.slider_amount_pill_per_time.setStyleSheet("QSlider{\n"
"border-radius: 10px ;\n"
"}\n"
"\n"
"QSlider::groove:horizontal{\n"
"border: 10px ;\n"
"height: 15px;\n"
"background: #1C84A9;\n"
"}\n"
"\n"
"QSlider::handle:horizontal{\n"
"background: #1C84A9;\n"
"border: 10px ;\n"
"width: 25px;\n"
"margin: -8px 0;\n"
"border-radius: 10px;\n"
"}\n"
"QSlider::add-page:horizontal{\n"
"background-color: white;\n"
"border: 10px;\n"
"}")
        self.slider_amount_pill_per_time.setSliderPosition(0)
        self.slider_amount_pill_per_time.setOrientation(QtCore.Qt.Horizontal)
        self.slider_amount_pill_per_time.setObjectName("slider_amount_pill_per_time")
        self.button_next = QtWidgets.QToolButton(background_amount_pill_per_time)
        self.button_next.setGeometry(QtCore.QRect(295, 375, 200, 90))
        self.button_next.setStyleSheet("QToolButton { font: 75 36pt \"JasmineUPC\"; background-color:#24BD73; color: #ffffff; border-radius:20px; }""QToolButton:hover { font: 75 36pt \"JasmineUPC\"; background-color:#23B36D; color: #ffffff; border-radius:20px; }")
        self.button_next.setObjectName("button_next")

        self.retranslateUi(background_amount_pill_per_time)
        QtCore.QMetaObject.connectSlotsByName(background_amount_pill_per_time)

    def retranslateUi(self, background_amount_pill_per_time):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        channelID = "ช่องที่ " + str(globalPillData["id"] + 1)

        background_amount_pill_per_time.setWindowTitle(_translate("background_amount_pill_per_time", "Dialog"))
        self.no_channel.setText(_translate("background_amount_pill_per_time", channelID))
        self.text_question_amount_pill_per_time.setText(_translate("background_amount_pill_per_time", "กรุณาระบุจำนวนยาที่ต้องทานในแต่ละมื้อ"))
        self.button_next.setText(_translate("background_amount_pill_per_time", "ถัดไป"))

    def updateSliderPillPerTime(self,amount_of_pill_per_time):
        self.lcdNumberPillPerTime.display(amount_of_pill_per_time)
        # print("[amount of pill per time] : ",amount_of_pill_per_time)
        self.amount_pill =  amount_of_pill_per_time
        #======================= add amount pill per time data to array object =======================#

    def gotoInputTimesToTakePill(self):
        if hasattr(self, 'amount_pill') :
            global globalPillData
            globalPillData["pillsPerTime"] = self.amount_pill

            input_times_to_take_pill_screen = PillSummaryScreen(globalPillData)
            __main__.widget.addWidget(input_times_to_take_pill_screen)
            __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)


# ########### เวลา ############
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

        screen = AmountPillPerTimeScreen(globalPillData, objIndex, False)

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
    
    def goToPillSummaryScreen(self):
        #================ go to add summary time screen ====================#
        global globalTimesToTakePillArr
        global globalPillData
        globalPillData["timeToTake"] = globalTimesToTakePillArr
        # print(json.dumps(globalPillData, indent=4))

        add_summary_time_screen = __main__.PillSummaryScreen(globalPillData)
        __main__.widget.removeWidget(self)
        __main__.widget.addWidget(add_summary_time_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)
        
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