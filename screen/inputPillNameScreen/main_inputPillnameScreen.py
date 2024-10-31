import json
import os
import sys

import __main__
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QWidget

sys.path.append(os.path.abspath('../klongyaa/Klongyaa'))

from screen.totalPillsNPillPerTimeScreen.main_totalPillsNPertimeScreen import \
    TotalPillsScreen

# Initialize global variables
globalPillData = {}
globalInputPillName = ""

def resetGlobalData():
    global globalPillData
    global globalInputPillName

    globalInputPillName = ""
    globalPillData = {}

class PillNameScreen(QDialog):
    def __init__(self, pillData=None, pillNames=None, pillID=None, pillNamesEng=None, parent=None):
        super().__init__(parent)
        global globalPillData
        globalPillData = pillData if pillData is not None else {}
        self.pillNames = pillNames if pillNames is not None else []
        self.pillID = pillID if pillID is not None else []
        self.pillNamesEng = pillNamesEng if pillNamesEng is not None else []
        
        self.inputPillName = globalPillData.get("name", "")
        self.inputPillID = globalPillData.get("pillId", "")
        self.inputPillNameEng = globalPillData.get("medicalname", "")
        
        self.setupUi(self)
        
    def setupUi(self, background_confirm_pill_name):
        background_confirm_pill_name.setObjectName("background_confirm_pill_name")
        background_confirm_pill_name.resize(800, 480)
        background_confirm_pill_name.setStyleSheet("QWidget#background_confirm_pill_name { background-color: #97C7F9 }")

        self.no_channel = QtWidgets.QLabel(background_confirm_pill_name)
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 190, 70))
        font = QtGui.QFont()
        font.setFamily("TH Sarabun New")
        font.setPointSize(36)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF; font: 36pt \"TH Sarabun New\"; font-weight: bold; border-radius: 25px; color: #070021; ")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")

        self.label_1 = QtWidgets.QLabel(background_confirm_pill_name)
        self.label_1.setGeometry(QtCore.QRect(245, 30, 450, 70))
        self.label_1.setStyleSheet("font: 36pt \"TH Sarabun New\"; font-weight: bold;")
        self.label_1.setAlignment(QtCore.Qt.AlignLeft)
        self.label_1.setObjectName("label_1")
        
        #แก้
        # Label to display the selected pill name
        self.label_pill_name = QtWidgets.QLabel(background_confirm_pill_name)
        self.label_pill_name.setGeometry(QtCore.QRect(120, 150, 560, 150))
        self.label_pill_name.setStyleSheet("font: 30pt \"TH Sarabun New\"; background-color: white; border: 2px solid black; font-weight: bold;")
        self.label_pill_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pill_name.setObjectName("label_pill_name")
        
        
        # Set initial selection
        self.current_pill_index = 0
        if isinstance(self.pillNames, list) and len(self.pillNames) > 0:
            self.label_pill_name.setText(self.pillNames[self.current_pill_index])
        elif isinstance(self.pillNames, dict):
            # แก้เป็นการเข้าถึง dictionary โดยตรง
            self.label_pill_name.setText(self.pillNames.get("name", ""))
            

        # Left arrow button
        self.btn_left = QtWidgets.QPushButton(background_confirm_pill_name)
        self.btn_left.setGeometry(QtCore.QRect(15, 185, 100, 75))
        self.btn_left.setText("<")
        self.btn_left.setStyleSheet("font: 36pt \"TH Sarabun New\"; background-color: white; font-weight: bold; ")
        self.btn_left.setObjectName("btn_left")

        # Right arrow button
        self.btn_right = QtWidgets.QPushButton(background_confirm_pill_name)
        self.btn_right.setGeometry(QtCore.QRect(685, 185, 100, 75))
        self.btn_right.setText(">")
        self.btn_right.setStyleSheet("font: 36pt \"TH Sarabun New\"; background-color: white; font-weight: bold;")
        self.btn_right.setObjectName("btn_right")

        # Connect buttons to functions
        self.btn_left.clicked.connect(self.navigate_left)
        self.btn_right.clicked.connect(self.navigate_right)

        self.button_correct_pill_name = QtWidgets.QToolButton(background_confirm_pill_name)
        self.button_correct_pill_name.setGeometry(QtCore.QRect(295, 375, 200, 90))
        self.button_correct_pill_name.setStyleSheet("QToolButton#button_correct_pill_name { font: 75 36pt \"TH Sarabun New\"; background-color:#24BD73; color: #ffffff; border-radius:20px; font-weight: bold; } QToolButton#button_correct_pill_name:hover { font: 75 36pt \"TH Sarabun New\"; background-color:#23B36D; color: #ffffff; border-radius:20px; font-weight: bold; }")
        self.button_correct_pill_name.setObjectName("button_correct_pill_name")
        self.button_correct_pill_name.clicked.connect(self.goToMainTotalPillsNPertimeScreen)

        self.retranslateUi(background_confirm_pill_name)
        QtCore.QMetaObject.connectSlotsByName(background_confirm_pill_name)
        
    def navigate_left(self):
        if self.current_pill_index > 0:
            self.current_pill_index -= 1
        else:
            self.current_pill_index = len(self.pillNames) - 1
        self.label_pill_name.setText(self.pillNames[self.current_pill_index])
        self.inputPillID = self.pillID[self.current_pill_index]
        self.inputPillNameEng = self.pillNamesEng[self.current_pill_index]

    def navigate_right(self):
        if self.current_pill_index < len(self.pillNames) - 1:
            self.current_pill_index += 1
        else:
            self.current_pill_index = 0
        self.label_pill_name.setText(self.pillNames[self.current_pill_index])
        self.inputPillID = self.pillID[self.current_pill_index]
        self.inputPillNameEng = self.pillNamesEng[self.current_pill_index]
        
    def retranslateUi(self, background_confirm_pill_name):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        channelID = "ช่องที่ " + str(globalPillData.get("channelId", 0) + 1)

        background_confirm_pill_name.setWindowTitle(_translate("background_confirm_pill_name", "Dialog"))
        self.no_channel.setText(_translate("background_confirm_pill_name", channelID))
        self.label_1.setText(_translate("background_confirm_pill_name", "ใส่ชื่อยาของท่าน"))
        self.button_correct_pill_name.setText(_translate("background_confirm_pill_name", "ถัดไป"))

    def goToMainTotalPillsNPertimeScreen(self):
        selected_pill_name = self.label_pill_name.text()
        if not selected_pill_name or selected_pill_name == "โปรดเลือกชื่อยา":
            # QtWidgets.QMessageBox.warning(self, "Warning", "Please select a pill name.")
            return
        
        global globalPillData
        globalPillData["name"] = selected_pill_name
        globalPillData["pillId"] = self.inputPillID
        globalPillData["medicalname"] = self.inputPillNameEng
        total_pills_screen = TotalPillsScreen(pillData=globalPillData)
        # print(json.dumps(globalPillData, indent=4))
        # print("\n ไปหน้าเพิ่มจำนวนยาทั้งหมดและจำนวนยาที่ต้องกินต่อมื้อ \n")
        __main__.widget.addWidget(total_pills_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = QtWidgets.QStackedWidget()
    main_window.setWindowTitle("GUI - KLONG_YAA")
    pill_name_screen = PillNameScreen()
    main_window.addWidget(pill_name_screen)
    main_window.setFixedWidth(800)
    main_window.setFixedHeight(480)
    main_window.show()
    sys.exit(app.exec_())

