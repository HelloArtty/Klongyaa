import json
import sys
from functools import partial

import __main__
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog

from shared.api.getMedicines import fetch_pill_names
from shared.main_success_save_screen import SuccessSaveScreen

class UpdatePillScreen(QDialog):
    def __init__(self, pill_channel_data):
        super().__init__()
        global globalPillData
        self.pill_channel_data = pill_channel_data
        globalPillData = self.pill_channel_data
        print("update:",globalPillData)
        
        self.inputPillName = globalPillData.get("name", "")
        self.inputPillID = globalPillData.get("pillId", "")
        self.setupUi(self)
        self.button_save_pill_summary.clicked.connect(self.savePillSummary)
        
        self.button_edit_pill_name.clicked.connect(self.editPillName)
        self.button_edit_amount_pill.clicked.connect(self.editAmountPill)
        if globalPillData["totalPills"] > 0 :
            self.button_edit_total_pills.clicked.connect(self.editTotalPills)
        self.button_edit_time.clicked.connect(self.editTime)
        
    def editPillName(self):
        self.editDetail("pill_name")

    def editAmountPill(self):
        self.editDetail("amount_pill")

    def editTotalPills(self):
        self.editDetail("total_pills")

    def editTime(self):
        self.editDetail("time")

        
        
    def setupUi(self, background_update_screen):
        global globalPillData
        globalPillData = self.pill_channel_data
        currentRow = 0

        # Setup background
        background_update_screen.setObjectName("background_update_screen")
        background_update_screen.resize(800, 480)
        background_update_screen.setStyleSheet("QWidget#background_update_screen{ background-color: #97C7F9 }")

        # Header label
        self.text_header_summary_screen = QtWidgets.QLabel(background_update_screen)
        self.text_header_summary_screen.setGeometry(QtCore.QRect(290, 20, 375, 60))
        self.text_header_summary_screen.setStyleSheet("font: 36pt \"TH Sarabun New\"; font-weight: bold;")
        self.text_header_summary_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.text_header_summary_screen.setObjectName("text_header_summary_screen")

        # Scroll area setup
        self.scroll_area = QtWidgets.QScrollArea(background_update_screen)
        self.scroll_area.setGeometry(QtCore.QRect(10, 90, 780, 300))
        self.scroll_area.setMinimumSize(QtCore.QSize(0, 300))
        self.scroll_area.setStyleSheet("background-color:rgb(156, 183, 255); border-color:rgb(156, 183, 255);")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")

        # Scroll area contents
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 829, 316))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")

        # ชื่อยา
        self.question_pill_name = QtWidgets.QLabel("Pill Name", self.scrollAreaWidgetContents)
        self.question_pill_name.setMinimumSize(250, 35)
        font = QtGui.QFont("TH Sarabun New", 36)
        self.question_pill_name.setFont(font)
        self.question_pill_name.setStyleSheet("background-color: #C5E1FF; ;border-radius: 25px; color: #070021; font-weight: bold;")
        self.question_pill_name.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter )
        self.question_pill_name.setContentsMargins(20, 0, 0, 0) 
        self.gridLayout_2.addWidget(self.question_pill_name, currentRow, 0, 1, 1)
        
        # รายละเอียดชื่อยา
        self.show_pill_name = self.createLabel("", 200, 40, "font: 36pt \"TH Sarabun New\"; font-weight: bold; color: #070021; border: none; margin-right:50px;", self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.show_pill_name, currentRow, 1, 1, 1)
        # แก้ไข
        self.button_edit_pill_name = self.createToolButton("edit2.png", self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.button_edit_pill_name, currentRow, 3, 1, 1)

        currentRow += 1

        # จำนวนยาทั้งหมด
        if globalPillData["totalPills"] > 0:
            self.question_total_pills = QtWidgets.QLabel("จำนวนยาทั้งหมด", self.scrollAreaWidgetContents)
            self.question_total_pills.setMinimumSize(250, 35)  # กำหนดขนาดขั้นต่ำ
            font = QtGui.QFont("TH Sarabun New", 36)  # กำหนดฟอนต์
            self.question_total_pills.setFont(font)  # ตั้งค่าให้กับ QLabel
            self.question_total_pills.setStyleSheet("background-color: #C5E1FF; border-radius: 25px; color: #070021; font-weight: bold;")  # ตั้งค่ารูปแบบ
            self.question_total_pills.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)  # จัดเรียงชิดซ้ายและกลางแนวตั้ง
            self.question_total_pills.setContentsMargins(20, 0, 0, 0)  # ตั้งค่าระยะห่าง
            self.gridLayout_2.addWidget(self.question_total_pills, currentRow, 0, 1, 1)  # เพิ่มเข้าไปใน layout
            self.show_total_pills = self.createLabel(f"{globalPillData['totalPills']} เม็ด", 200, 40, "font: 75 36pt \"TH Sarabun New\"; font-weight: bold; color: #070021; margin-right:50px;", self.scrollAreaWidgetContents)
            self.gridLayout_2.addWidget(self.show_total_pills, currentRow, 1, 1, 1)
            self.button_edit_total_pills = self.createToolButton("edit2.png", self.scrollAreaWidgetContents)
            self.gridLayout_2.addWidget(self.button_edit_total_pills, currentRow, 3, 1, 1)

            currentRow += 1

        # จำนวนยาที่ต้องทานต่อครั้ง
        self.question_amount_pill = QtWidgets.QLabel("จำนวนยา", self.scrollAreaWidgetContents)
        self.question_amount_pill.setMinimumSize(350, 35)  # กำหนดขนาดขั้นต่ำ
        font = QtGui.QFont("TH Sarabun New", 36)  # กำหนดฟอนต์
        self.question_amount_pill.setFont(font)  # ตั้งค่าให้กับ QLabel
        self.question_amount_pill.setStyleSheet("background-color: #C5E1FF; border-radius: 25px; color: #070021; font-weight: bold;")  # ตั้งค่ารูปแบบ
        self.question_amount_pill.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)  # จัดเรียงชิดซ้ายและกลางแนวตั้ง
        self.question_amount_pill.setContentsMargins(20, 0, 0, 0)  # ตั้งค่าระยะห่าง
        self.gridLayout_2.addWidget(self.question_amount_pill, currentRow, 0, 1, 1)  # เพิ่มเข้าไปใน layout
        self.show_amount_pill = self.createLabel("", 200, 40, "font: 36pt \"TH Sarabun New\"; color: #070021; margin-right:50px; font-weight: bold;", self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.show_amount_pill, currentRow, 1, 1, 1)
        self.button_edit_amount_pill = self.createToolButton("edit2.png", self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.button_edit_amount_pill, currentRow, 3, 1, 1)

        currentRow += 1

        # เวลาที่ต้องทานยา
        for index, time in enumerate(globalPillData["timeToTake"]):
            # สร้าง Label สำหรับเวลาทานยา
            timeToTakePillLabel = self.createLabel(
                f"เวลาที่ {index + 1}", 250, 40,
                "background-color: #C5E1FF; border-radius: 25px; color: #070021; font: 36pt \"TH Sarabun New\"; font-weight: bold;",
                self.scrollAreaWidgetContents
            )
            timeToTakePillLabel.setFont(QtGui.QFont("TH Sarabun New", 36))  # ตั้งค่าฟอนต์
            timeToTakePillLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            timeToTakePillLabel.setContentsMargins(10, 0, 0, 0)  # ระยะห่างด้านใน
            self.gridLayout_2.addWidget(timeToTakePillLabel, currentRow + index, 0, 1, 1)

            # สร้าง Label สำหรับข้อมูลเวลา
            timeToTakePillData = self.createLabel(
                f"{time} น.", 200, 40,
                "font: 36pt \"TH Sarabun New\"; color: #070021; font-weight: bold;",
                self.scrollAreaWidgetContents
            )
            self.gridLayout_2.addWidget(timeToTakePillData, currentRow + index, 1, 1, 1)

        # สร้างปุ่มแก้ไขในแถวแรกสุด
        self.button_edit_time = self.createToolButton("edit2.png", self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.button_edit_time, currentRow, 3, 1, 1)  # ปรับตำแหน่งให้อยู่ในแถวแรก
        self.button_edit_time.setEnabled(True)  # เปิดใช้งานปุ่มแรก

        # ฟังก์ชันสร้างปุ่มแก้ไขที่ไม่มีรูปภาพ
        def createDisabledEditButton(parent):
            button = QtWidgets.QPushButton(parent)
            button.setFixedSize(68, 68)  # ตั้งค่าขนาดของปุ่ม
            button.setStyleSheet("""
                background-color: rgb(156, 183, 255);  /* สีพื้นหลัง */
                border: none;                           /* ลบกรอบ */
            """)
            button.setEnabled(False)  # ปิดการใช้งานปุ่ม
            return button

        # สร้างปุ่มแก้ไขในแถวถัดไป แต่ปิดการใช้งาน
        for index in range(1, len(globalPillData["timeToTake"])):
            edit_button_disabled = createDisabledEditButton(self.scrollAreaWidgetContents)
            self.gridLayout_2.addWidget(edit_button_disabled, currentRow + index, 3, 1, 1)
            
        currentRow += len(globalPillData["timeToTake"])
        self.scroll_area.setWidget(self.scrollAreaWidgetContents)
        
        # Save button
        self.button_save_pill_summary = QtWidgets.QToolButton(background_update_screen)
        self.button_save_pill_summary.setGeometry(QtCore.QRect(280, 400, 220, 75))
        self.button_save_pill_summary.setStyleSheet("font: 36pt \"TH Sarabun New\"; font-weight: bold; background-color:#24BD73; color: #ffffff; border-radius:20px;")
        self.button_save_pill_summary.setObjectName("button_save_pill_summary")

        # Channel label
        self.no_channel = QtWidgets.QLabel(background_update_screen)
        self.no_channel.setGeometry(QtCore.QRect(40, 10, 190, 70))
        self.no_channel.setStyleSheet("background-color: #C5E1FF; font: 75 36pt \"TH Sarabun New\"; font-weight: bold; border-radius: 25px; color: #070021;")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")

        # Retranslate UI
        self.retranslateUi(background_update_screen)
        QtCore.QMetaObject.connectSlotsByName(background_update_screen)
        
    def retranslateUi(self, background_summary_screen):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        pillName = globalPillData["name"]
        pillsPerTime = str(globalPillData["pillsPerTime"]) + " เม็ด/มื้อ"
        channelID = "ช่องที่ " + str(globalPillData["channelId"] + 1)
        
        background_summary_screen.setWindowTitle(_translate("background_summary_screen", "Dialog"))
        self.no_channel.setText(_translate("background_summary_screen", channelID))
        self.text_header_summary_screen.setText(_translate("background_summary_screen", "ข้อมูลของยาที่ต้องทาน"))
        self.question_pill_name.setText(_translate("background_summary_screen", "ชื่อยา"))
        self.show_pill_name.setText(_translate("background_summary_screen", pillName))
        self.question_amount_pill.setText(_translate("background_summary_screen", "จำนวนยาที่ต้องทาน"))
        self.show_amount_pill.setText(_translate("background_summary_screen", pillsPerTime))
        self.button_save_pill_summary.setText(_translate("background_summary_screen", "บันทึก"))
        
    def createLabel(self, text, minWidth, minHeight, style, parent):
        label = QtWidgets.QLabel(parent)
        label.setMinimumSize(QtCore.QSize(minWidth, minHeight))
        label.setStyleSheet(style)
        label.setText(text)
        return label
    
    def createToolButton(self, iconPath, parent):
        button = QtWidgets.QToolButton(parent)
        button.setIconSize(QtCore.QSize(68, 68))
        button.setIcon(QtGui.QIcon(f'../Klongyaa/shared/images/{iconPath}'))
        button.setStyleSheet("background-color: rgb(255, 74, 74); border-radius: 35px;")
        return button
    
    def savePillSummary(self,id):
        global globalPillData
        id = globalPillData["id"]
        success_save_screen = SuccessSaveScreen(globalPillData)
        pill_data = {
            "channelIndex": str(globalPillData["channelId"]),
            "userID": __main__.config["userId"],
            "medicineID": globalPillData["pillId"],
            "amount": str(globalPillData["totalPills"]),
            "total": str(globalPillData["totalPills"]),
            "amountPerTime": globalPillData["pillsPerTime"],
            "time": globalPillData["timeToTake"],
        }

        res = requests.post(__main__.config["url"] + "/user/updatePillChannel" + id, json=pill_data)

        if res.status_code == 200:
            print("โอเค")
            __main__.refreshPillData()  # ส่งสัญญาณเมื่อข้อมูลถูกบันทึกสำเร็จ

        __main__.widget.removeWidget(self)
        __main__.widget.addWidget(success_save_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
        
    def editDetail(self, edit_mode):
        global globalPillData
        # print(f"Edit mode: {edit_mode}")
        screen = None
        
        if edit_mode == "pill_name":
            pillNames, pillIDs, pillNamesEng = fetch_pill_names()
            screen = PillNameScreen()
        

        if screen is not None:
            __main__.widget.addWidget(screen)
            __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
            
            
            
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys

class PillNameScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pill Name Screen")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        # Main layout
        layout = QVBoxLayout()

        # Title label
        self.titleLabel = QLabel("Pill Names")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(self.titleLabel)

        # Pill name list
        self.pillList = QListWidget()
        self.pillList.addItem("Pill 1")
        self.pillList.addItem("Pill 2")
        self.pillList.addItem("Pill 3")
        self.pillList.addItem("Pill 4")
        layout.addWidget(self.pillList)

        # Button layout
        buttonLayout = QHBoxLayout()

        # Add button
        self.addButton = QPushButton("Add Pill")
        self.addButton.setFont(QFont("Arial", 10, QFont.Bold))
        self.addButton.clicked.connect(self.add_pill)
        buttonLayout.addWidget(self.addButton)

        # Remove button
        self.removeButton = QPushButton("Remove Selected")
        self.removeButton.setFont(QFont("Arial", 10, QFont.Bold))
        self.removeButton.clicked.connect(self.remove_selected_pill)
        buttonLayout.addWidget(self.removeButton)

        # Add buttons to main layout
        layout.addLayout(buttonLayout)

        # Set layout
        self.setLayout(layout)

    def add_pill(self):
        # Logic to add a new pill (placeholder)
        self.pillList.addItem("New Pill")

    def remove_selected_pill(self):
        # Logic to remove selected pill
        selected_item = self.pillList.currentRow()
        if selected_item >= 0:
            self.pillList.takeItem(selected_item)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PillNameScreen()
    window.show()
    sys.exit(app.exec_())
