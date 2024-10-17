import json
import sys

import __main__
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QWidget
from screen.totalPillsNPillPerTimeScreen.gen.gen_amount_pill_per_time_screen import *
from screen.totalPillsNPillPerTimeScreen.gen.gen_total_pills_screen import *
from screen.totalPillsNPillPerTimeScreen.shared.gen_mock_screen import *

globalPillData = {}

class TotalPillsScreen(QDialog):
    def __init__(self, pillData):
        super().__init__()
        global globalPillData
        globalPillData = pillData
        self.setupUi(self)
        #======================= set max-min of total pills =======================#
        self.slider_total_pills.setMaximum(99)
        self.slider_total_pills.setMinimum(0)
        self.slider_total_pills.valueChanged.connect(self.updateSliderTotalPills)
        self.button_save_total_pills.clicked.connect(self.goToAmountPillPerTimeScreen)
        
    def setupUi(self, background_total_pills):
        background_total_pills.setObjectName("background_total_pills")
        background_total_pills.resize(800, 480)
        background_total_pills.setStyleSheet("QWidget#background_total_pills { background-color: #97C7F9 }")

        # Initialize and set up QLabel for channel info
        self.no_channel = QtWidgets.QLabel(background_total_pills)
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

        # Initialize and set up QLabel for the instruction text
        self.text_question_inputting_total_pills = QtWidgets.QLabel(background_total_pills)
        self.text_question_inputting_total_pills.setGeometry(QtCore.QRect(85, 105, 650, 70))
        self.text_question_inputting_total_pills.setStyleSheet("font: 40pt \"JasmineUPC\";")
        self.text_question_inputting_total_pills.setObjectName("text_question_inputting_total_pills")

        # Initialize and set up QLCDNumber for displaying numeric values
        self.lcdNumber = QtWidgets.QLCDNumber(background_total_pills)
        self.lcdNumber.setGeometry(QtCore.QRect(210, 180, 370, 130))
        self.lcdNumber.setStyleSheet("background-color: #ffffff;")
        self.lcdNumber.setObjectName("lcdNumber")

        # Initialize and set up QSlider for adjusting values
        self.slider_total_pills = QtWidgets.QSlider(background_total_pills)
        self.slider_total_pills.setGeometry(QtCore.QRect(100, 330, 600, 30))
        self.slider_total_pills.setStyleSheet("QSlider { border-radius: 10px; }"
                                                "QSlider::groove:horizontal { border: 10px; height: 15px; background: #1C84A9; }"
                                                "QSlider::handle:horizontal { background: #1C84A9; border: 10px; width: 25px; margin: -8px 0; border-radius: 10px; }"
                                                "QSlider::add-page:horizontal { background-color: white; border: 10px; }")
        self.slider_total_pills.setSliderPosition(0)
        self.slider_total_pills.setOrientation(QtCore.Qt.Horizontal)
        self.slider_total_pills.setObjectName("slider_total_pills")

        self.button_save_total_pills = QtWidgets.QToolButton(background_total_pills)
        self.button_save_total_pills.setGeometry(QtCore.QRect(295, 375, 200, 90))
        self.button_save_total_pills.setStyleSheet("QToolButton { font: 75 36pt \"JasmineUPC\"; background-color:#24BD73; color: #ffffff; border-radius:20px; }"
                                                    "QToolButton:hover { font: 75 36pt \"JasmineUPC\"; background-color:#23B36D; color: #ffffff; border-radius:20px; }")
        self.button_save_total_pills.setObjectName("button_save_total_pills")
        self.button_save_total_pills.clicked.connect(self.goToAmountPillPerTimeScreen)

        # Set up translations and connections
        self.retranslateUi(background_total_pills)
        QtCore.QMetaObject.connectSlotsByName(background_total_pills)

    def retranslateUi(self, background_total_pills):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        channelID = "ช่องที่ " + str(globalPillData.get("channelId", 0) + 1)

        background_total_pills.setWindowTitle(_translate("background_total_pills", "Dialog"))
        self.no_channel.setText(_translate("background_total_pills", channelID))
        self.text_question_inputting_total_pills.setText(_translate("background_total_pills", "กรุณาระบุจำนวนเม็ดยาทั้งหมดที่จะบรรจุ"))
        self.button_save_total_pills.setText(_translate("background_total_pills", "ถัดไป"))

    def updateSliderTotalPills(self,count_of_total_pills):
        self.lcdNumber.display(count_of_total_pills)
        self.total_pills = count_of_total_pills
        
    def goToAmountPillPerTimeScreen(self):
        global globalPillData
        if not hasattr(self, 'total_pills') or self.total_pills is None:
            return

        if self.total_pills > 0:
            globalPillData["totalPills"] = self.total_pills
            pill_per_time_screen = AmountPillPerTimeScreen()
            __main__.widget.addWidget(pill_per_time_screen)
            __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "จำนวนเม็ดยาต้องมากกว่า 0")

        
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
        channelID = "ช่องที่ " + str(globalPillData["channelId"] + 1)

        background_amount_pill_per_time.setWindowTitle(_translate("background_amount_pill_per_time", "Dialog"))
        self.no_channel.setText(_translate("background_amount_pill_per_time", channelID))
        self.text_question_amount_pill_per_time.setText(_translate("background_amount_pill_per_time", "กรุณาระบุจำนวนยาที่ต้องทานในแต่ละมื้อ"))
        self.button_next.setText(_translate("background_amount_pill_per_time", "ถัดไป"))

    def updateSliderPillPerTime(self,amount_of_pill_per_time):
        self.lcdNumberPillPerTime.display(amount_of_pill_per_time)
        # print("[amount of pill per time] : ",amount_of_pill_per_time)
        self.amount_pill =  amount_of_pill_per_time

    def gotoInputTimesToTakePill(self):
        if hasattr(self, 'amount_pill') :

            global globalPillData
            globalPillData["pillsPerTime"] = self.amount_pill
            # print(json.dumps(globalPillData, indent=4))
            # print("\n ไปหน้าเพิ่มเวลาทานยา \n")

            input_times_to_take_pill_screen = __main__.InputTimeToTakePillScreen(globalPillData, -1, False)
            __main__.widget.removeWidget(self)
            __main__.widget.addWidget(input_times_to_take_pill_screen)
            __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)
            
