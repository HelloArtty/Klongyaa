import json
import sys
from datetime import datetime
from functools import partial

import __main__
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
                             QListWidget, QPushButton, QVBoxLayout, QWidget)

from shared.api.getMedicines import fetch_pill_names
from shared.main_success_save_screen import SuccessSaveScreen


class UpdatePillScreen(QDialog):
    def __init__(self, pill_channel_data, parent=None):
        super().__init__(parent)
        self.config = __main__.config
        global globalPillData
        self.pill_channel_data = pill_channel_data
        globalPillData = self.pill_channel_data
        # print("update:",globalPillData)
        
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

        # Channel label
        self.no_channel = QtWidgets.QLabel(background_update_screen)
        self.no_channel.setGeometry(QtCore.QRect(40, 10, 190, 70))
        self.no_channel.setStyleSheet("background-color: #C5E1FF; font: 75 36pt \"TH Sarabun New\"; font-weight: bold; border-radius: 25px; color: #070021;")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")
        
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
        self.button_edit_pill_name = self.createToolButton("edit2.png", self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.button_edit_pill_name, currentRow, 3, 1, 1)

        currentRow += 1

        # จำนวนยาทั้งหมด
        self.question_total_pills = QtWidgets.QLabel("จำนวนยาทั้งหมด", self.scrollAreaWidgetContents)
        self.question_total_pills.setMinimumSize(250, 35)
        font = QtGui.QFont("TH Sarabun New", 36)
        self.question_total_pills.setFont(font)
        self.question_total_pills.setStyleSheet("background-color: #C5E1FF; border-radius: 25px; color: #070021; font-weight: bold;")
        self.question_total_pills.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.question_total_pills.setContentsMargins(20, 0, 0, 0)
        self.gridLayout_2.addWidget(self.question_total_pills, currentRow, 0, 1, 1)

        # Create show_total_pills widget without condition
        self.show_total_pills = self.createLabel("", 200, 40, "font: 75 36pt \"TH Sarabun New\"; font-weight: bold; color: #070021; margin-right:50px;", self.scrollAreaWidgetContents)
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
        
        # Back button
        self.button_go_back = self.create_tool_button("ย้อนกลับ", background_update_screen, self.goBack, QtCore.QRect(145, 400, 220, 75))
        self.button_go_back.setEnabled(True)
        
        # Save button
        self.button_save_pill_summary = QtWidgets.QToolButton(background_update_screen)
        self.button_save_pill_summary.setGeometry(QtCore.QRect(445, 400, 220, 75))
        self.button_save_pill_summary.setStyleSheet("font: 36pt \"TH Sarabun New\"; font-weight: bold; background-color:#24BD73; color: #ffffff; border-radius:20px;")
        self.button_save_pill_summary.setObjectName("button_save_pill_summary")
        

        # Retranslate UI
        self.retranslateUi(background_update_screen)
        QtCore.QMetaObject.connectSlotsByName(background_update_screen)
        
    def retranslateUi(self, background_summary_screen):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        pillName = globalPillData["name"]
        pillsPerTime = str(globalPillData["pillsPerTime"]) + " เม็ด/มื้อ"
        channelID = "ช่องที่ " + str(globalPillData["channelId"] + 1)
        totalPills = f"{globalPillData['totalPills']} เม็ด" if globalPillData.get("totalPills", 0) > 0 else "ยาหมด"

        background_summary_screen.setWindowTitle(_translate("background_summary_screen", "Dialog"))
        self.no_channel.setText(_translate("background_summary_screen", channelID))
        self.text_header_summary_screen.setText(_translate("background_summary_screen", "ข้อมูลของยาที่ต้องทาน"))
        self.question_pill_name.setText(_translate("background_summary_screen", "ชื่อยา"))
        self.question_amount_pill.setText(_translate("background_summary_screen", "จำนวนยาที่ต้องทาน"))
        self.button_save_pill_summary.setText(_translate("background_summary_screen", "บันทึก"))
        self.button_go_back.setText(_translate("background_detail_screen", "ย้อนกลับ"))
        self.show_pill_name.setText(_translate("background_summary_screen", pillName))
        self.show_total_pills.setText(_translate("background_summary_screen", totalPills))
        self.show_amount_pill.setText(_translate("background_summary_screen", pillsPerTime))

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
    
    def create_tool_button(self, text, parent, click_action, geometry):
        button = QtWidgets.QToolButton(parent)
        button.setGeometry(geometry)
        button.setStyleSheet("QToolButton { font: 36pt \"TH Sarabun New\"; background-color:#DD5D5D; color: #ffffff; border-radius:20px; font-weight: bold; }")
        button.clicked.connect(click_action)
        return button
    
    def goBack(self):
        __main__.widget.addWidget(__main__.HomeScreen(__main__.pill_channel_datas, __main__.config))
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
        
    def savePillSummary(self):
        global globalPillData
        success_save_screen = SuccessSaveScreen(globalPillData)
        pill_id = globalPillData["id"]  # Get the ID from globalPillData
        # print("Pill ID:", pill_id)

        # Prepare the data to be sent in the request
        pill_data = {
            "channelIndex": str(globalPillData["channelId"]),
            "userID": __main__.config["userId"],
            "medicineID": globalPillData["pillId"],
            "amount": str(globalPillData["totalPills"]),
            "total": str(globalPillData["totalPills"]),
            "amountPerTime": globalPillData["pillsPerTime"],
            "time": globalPillData["timeToTake"],
        }

        # Construct the URL with the ID
        url = f"{__main__.config['url']}/user/updatePillChannel/{pill_id}"
        # Send the PUT request to update data
        res = requests.put(url, json=pill_data)
        # print("Json:", pill_data)

        # Check the response
        if res.status_code == 200:
            print("Update successful")
            __main__.refreshPillData(self.config)  # Refresh data after successful update
            __main__.widget.removeWidget(self)
            __main__.widget.addWidget(success_save_screen)
            __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
        else:
            print(f"Failed to update data. Status code: {res.status_code}, Response: {res.text}")

        
    def editDetail(self, edit_mode):
        global globalPillData
        # print(f"Edit mode: {edit_mode}")
        screen = None
        
        if edit_mode == "pill_name":
            pillNames, pillIDs, pillNamesEng = fetch_pill_names()
            screen = PillNameScreen(globalPillData, pillNames=pillNames, pillID=pillIDs ,pillNamesEng=pillNamesEng)
        elif edit_mode == "total_pills":
            screen = TotalPillsScreen(globalPillData)
        elif edit_mode == "amount_pill":
            screen = AmountPillScreen(globalPillData)
        elif edit_mode == "time":
            screen = AddSummaryTimeScreen(globalPillData)
        

        if screen is not None:
            __main__.widget.addWidget(screen)
            __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
            
# ########### ชื่อยา ############
class PillNameScreen(QDialog):
    def __init__(self, pillData=None, pillNames=None, pillID=None, pillNamesEng=None, parent=None):
        super().__init__(parent)
        global globalPillData
        globalPillData = pillData if pillData is not None else {}
        self.pillNames = pillNames if pillNames is not None else []
        self.pillID = pillID if pillID is not None else []
        self.pillNamesEng = pillNamesEng if pillNamesEng is not None else []
        
        # ใช้ฟังก์ชัน fetch_pill_names เพียงถ้าไม่ได้รับ pillNames หรือ pillID
        if not self.pillNames or not self.pillID:
            self.pillNames, self.pillID = fetch_pill_names()
        
        self.inputPillName = globalPillData.get("name", "")
        self.inputPillID = globalPillData.get("pillId", "")
        self.inputPillNameEng = globalPillData.get("medicalname", "")
        
        # กำหนดค่าตำแหน่งเริ่มต้นของ current_pill_index
        if self.inputPillName in self.pillNames:
            self.current_pill_index = self.pillNames.index(self.inputPillName)
        else:
            self.current_pill_index = 0  # ถ้าไม่มีชื่อยาให้เริ่มต้นที่ index 0
            
        self.setupUi(self)
        self.save_button_pillname.clicked.connect(self.savePillName)

    def setupUi(self, background_confirm_pill_name):
        self.setObjectName("background_confirm_pill_name")
        self.resize(800, 480)
        self.setStyleSheet("QWidget#background_confirm_pill_name { background-color: #97C7F9 }")
        
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
        
        # Label to display the selected pill name
        self.label_pill_name = QtWidgets.QLabel(background_confirm_pill_name)
        self.label_pill_name.setGeometry(QtCore.QRect(120, 150, 560, 100))
        self.label_pill_name.setStyleSheet("font: 30pt \"TH Sarabun New\"; background-color: white; border: 2px solid black; font-weight: bold;")
        self.label_pill_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pill_name.setObjectName("label_pill_name")
        
        self.label_pill_name_eng = QtWidgets.QLabel(background_confirm_pill_name)
        self.label_pill_name_eng.setGeometry(QtCore.QRect(120, 260, 560, 100))  # Adjust geometry as needed
        self.label_pill_name_eng.setStyleSheet("font: 26pt \"TH Sarabun New\"; background-color: white; border: 2px solid black; font-weight: bold;")
        self.label_pill_name_eng.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pill_name_eng.setObjectName("label_pill_name_eng")
        
        # Set initial selection
        self.current_pill_index = 0
        if isinstance(self.pillNames, list) and len(self.pillNames) > 0:
            self.label_pill_name.setText(self.pillNames[self.current_pill_index])
        elif isinstance(self.pillNames, dict):
            # แก้เป็นการเข้าถึง dictionary โดยตรง
            self.label_pill_name.setText(self.pillNames.get("name", ""))
            
            
        # # Set initial English pill name
        if isinstance(self.pillNamesEng, list) and len(self.pillNamesEng) > 0:
            self.label_pill_name_eng.setText(self.pillNamesEng[self.current_pill_index])
        elif isinstance(self.pillNamesEng, dict):
            self.label_pill_name_eng.setText(self.pillNamesEng.get("medicalname", ""))
        
        # Left arrow button
        self.btn_left = QtWidgets.QPushButton(background_confirm_pill_name)
        self.btn_left.setGeometry(QtCore.QRect(15, 185, 100, 75))
        self.btn_left.setText("<")
        self.btn_left.setStyleSheet("font: 36pt \"TH Sarabun New\"; font-weight: bold;")
        self.btn_left.setObjectName("btn_left")
        
        # Right arrow button
        self.btn_right = QtWidgets.QPushButton(background_confirm_pill_name)
        self.btn_right.setGeometry(QtCore.QRect(685, 185, 100, 75))
        self.btn_right.setText(">")
        self.btn_right.setStyleSheet("font: 36pt \"TH Sarabun New\"; font-weight: bold;")
        self.btn_right.setObjectName("btn_right")
        
        # Connect buttons to functions
        self.btn_left.clicked.connect(self.navigate_left)
        self.btn_right.clicked.connect(self.navigate_right)
        
        self.save_button_pillname = QtWidgets.QToolButton(background_confirm_pill_name)
        self.save_button_pillname.setGeometry(QtCore.QRect(295, 375, 200, 90))
        self.save_button_pillname.setMinimumSize(QtCore.QSize(100, 50))
        self.save_button_pillname.setStyleSheet("QToolButton#save_button_pillname { font: 75 36pt \"TH Sarabun New\";font-weight: bold; background-color:#24BD73; color: #ffffff; border-radius:20px; } QToolButton#save_button_pillname:hover { font: 75 36pt \"TH Sarabun New\";font-weight: bold; background-color:#23B36D; color: #ffffff; border-radius:20px; }")
        self.save_button_pillname.setObjectName("save_button_pillname")
        
        self.retranslateUi(background_confirm_pill_name)
        QtCore.QMetaObject.connectSlotsByName(background_confirm_pill_name)

    def update_pill_names(self):
        """Update both pill name labels when navigating."""
        self.label_pill_name.setText(self.pillNames[self.current_pill_index])
        self.label_pill_name_eng.setText(self.pillNamesEng[self.current_pill_index])
        self.inputPillID = self.pillID[self.current_pill_index]
        self.inputPillNameEng = self.pillNamesEng[self.current_pill_index]

    def navigate_left(self):
        if self.current_pill_index > 0:
            self.current_pill_index -= 1
        else:
            self.current_pill_index = len(self.pillNames) - 1
        self.update_pill_names()

    def navigate_right(self):
        if self.current_pill_index < len(self.pillNames) - 1:
            self.current_pill_index += 1
        else:
            self.current_pill_index = 0
        self.update_pill_names()

    def retranslateUi(self, background_confirm_pill_name):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        channelID = "ช่องที่ " + str(globalPillData.get("channelId", 0) + 1)

        background_confirm_pill_name.setWindowTitle(_translate("background_confirm_pill_name", "Dialog"))
        self.no_channel.setText(_translate("background_confirm_pill_name", channelID))
        self.label_1.setText(_translate("background_confirm_pill_name", "ใส่ชื่อยาของท่าน"))
        self.save_button_pillname.setText(_translate("background_confirm_pill_name", "บันทึก"))
        
    def savePillName(self):
        selected_pill_name = self.label_pill_name.text()
        if not selected_pill_name or selected_pill_name == "โปรดเลือกชื่อยา":
            # QtWidgets.QMessageBox.warning(self, "Warning", "Please select a valid pill name.")
            return

        global globalPillData
        globalPillData["name"] = selected_pill_name
        globalPillData["pillId"] = self.inputPillID
        globalPillData["medicalname"] = self.inputPillNameEng
        

        # print("globalPillData(PillUP):", globalPillData)
        
        # เปลี่ยนไปยังหน้าจอสรุป
        save_pillname_screen = UpdatePillScreen(globalPillData)
        __main__.widget.addWidget(save_pillname_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
        __main__.widget.removeWidget(self)


# ########### ยาทั้งหมด ############
class TotalPillsScreen(QDialog):
    def __init__(self, pillData=None, parent=None):
        super().__init__(parent)
        global globalPillData
        globalPillData = pillData if pillData is not None else {}
        self.setupUi(self)
        self.button_save_total_pills.clicked.connect(self.saveTotalPills)
        
    def setupUi(self, background_total_pills):
        background_total_pills.setObjectName("background_total_pills")
        background_total_pills.resize(800, 480)
        background_total_pills.setStyleSheet("QWidget#background_total_pills { background-color: #97C7F9 }")

        # Initialize and set up QLabel for channel info
        self.no_channel = QtWidgets.QLabel(background_total_pills)
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 190, 70))
        font = QtGui.QFont()
        font.setFamily("TH Sarabun New")
        font.setPointSize(36)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF; font: 75 36pt \"TH Sarabun New\"; border-radius: 25px; color: #070021; font-weight: bold;")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")

        # Instruction text
        self.text_question_inputting_total_pills = QtWidgets.QLabel(background_total_pills)
        self.text_question_inputting_total_pills.setGeometry(QtCore.QRect(245, 30, 450, 70))
        self.text_question_inputting_total_pills.setStyleSheet("font: 36pt \"TH Sarabun New\"; font-weight: bold;")
        self.text_question_inputting_total_pills.setAlignment(QtCore.Qt.AlignLeft)
        self.text_question_inputting_total_pills.setObjectName("text_question_inputting_total_pills")

        # QLineEdit for number input
        self.line_edit_total_pills = QtWidgets.QLineEdit(background_total_pills)
        self.line_edit_total_pills.setGeometry(QtCore.QRect(275, 115, 250, 70))
        self.line_edit_total_pills.setStyleSheet("background-color: #ffffff; font: 36pt \"TH Sarabun New\"; border-radius: 20px; font-weight: bold;")
        self.line_edit_total_pills.setAlignment(QtCore.Qt.AlignCenter)
        self.line_edit_total_pills.setValidator(QtGui.QIntValidator(0, 99))  # Limit input from 0 to 99
        self.line_edit_total_pills.setObjectName("line_edit_total_pills")

        # Numpad Layout
        self.numpad_layout = QtWidgets.QGridLayout()
        self.numpad_layout.setSpacing(8)  # เพิ่มระยะห่างระหว่างปุ่ม
        self.numpad_layout.setContentsMargins(310, 200, 200, 0)  # Set margins for better positioning

        # Create Numpad buttons (1-9)
        self.numpad_buttons = []
        for i in range(1,10):
            button = QtWidgets.QPushButton(str(i))
            button.setMinimumSize(55, 55)  # ปรับขนาดปุ่มให้เล็กลง
            button.setStyleSheet("font: 28pt \"TH Sarabun New\"; background-color: white; border-radius: 10px; font-weight: bold;")
            button.clicked.connect(self.numpad_button_clicked)
            row = (i - 1) // 3  # จัดปุ่ม 3 ปุ่มต่อแถว
            col = (i - 1) % 3   # จัดตำแหน่งปุ่มตามลำดับคอลัมน์
            self.numpad_layout.addWidget(button, row, col)
            self.numpad_buttons.append(button)

        # Button for 0 and backspace
        self.button_zero = QtWidgets.QPushButton("0")
        self.button_zero.setMinimumSize(55, 55)  # ปรับขนาดปุ่มให้เล็กลง
        self.button_zero.setStyleSheet("font: 28pt \"TH Sarabun New\"; background-color: white; border-radius: 10px; font-weight: bold;")
        self.button_zero.clicked.connect(self.numpad_button_clicked)

        # Button for backspace
        self.button_backspace = QtWidgets.QPushButton("ลบ")
        self.button_backspace.setMinimumSize(55, 55)  # ปรับขนาดปุ่มให้เล็กลง
        self.button_backspace.setStyleSheet("font: 28pt \"TH Sarabun New\"; background-color: white; border-radius: 10px; font-weight: bold;")
        self.button_backspace.clicked.connect(self.numpad_backspace)

        # Add 0 and Backspace to the last row
        self.numpad_layout.addWidget(self.button_zero, 3, 0, 1, 2)  # ปุ่ม 0 ในตำแหน่งกลางแถวสุดท้าย 2 ช่อง
        self.numpad_layout.addWidget(self.button_backspace, 3, 2)  # ปุ่มลบในตำแหน่งขวาสุดของแถวสุดท้าย

        # Add Numpad layout to background
        numpad_widget = QtWidgets.QWidget(background_total_pills)
        numpad_widget.setLayout(self.numpad_layout)

        # ปุ่มบันทึก
        self.button_save_total_pills = QtWidgets.QToolButton(background_total_pills)
        self.button_save_total_pills.setGeometry(QtCore.QRect(580, 375, 200, 90))
        self.button_save_total_pills.setStyleSheet("QToolButton { font: 75 36pt \"TH Sarabun New\"; background-color:#24BD73; color: #ffffff; border-radius:20px; font-weight: bold; }"
                                                    "QToolButton:hover { font: 75 36pt \"TH Sarabun New\"; background-color:#23B36D; color: #ffffff; border-radius:20px; font-weight: bold; }")
        self.button_save_total_pills.setObjectName("button_save_total_pills")

        self.retranslateUi(background_total_pills)
        QtCore.QMetaObject.connectSlotsByName(background_total_pills)

    def retranslateUi(self, background_total_pills):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        channelID = "ช่องที่ " + str(globalPillData["channelId"] + 1)
        
        background_total_pills.setWindowTitle(_translate("background_total_pills", "Dialog"))
        self.no_channel.setText(_translate("background_total_pills", channelID))
        self.text_question_inputting_total_pills.setText(_translate("background_total_pills", "เม็ดยาทั้งหมดที่บรรจุ"))
        self.button_save_total_pills.setText(_translate("background_total_pills", "บันทึก"))

    # Numpad button click event handler
    def numpad_button_clicked(self):
        sender = self.sender()
        current_value = self.line_edit_total_pills.text()
        new_value = current_value + sender.text()
        if len(new_value) <= 2:  # Ensure max 2 digits
            self.line_edit_total_pills.setText(new_value)

    # Backspace button click event handler
    def numpad_backspace(self):
        current_value = self.line_edit_total_pills.text()
        self.line_edit_total_pills.setText(current_value[:-1])

    def saveTotalPills(self):
        total_pills = self.line_edit_total_pills.text()
        if not total_pills:
            return

        global globalPillData
        globalPillData["totalPills"] = int(total_pills)
        # print("globalPillData(TotalUP):", globalPillData)
        
        # เปลี่ยนไปยังหน้าจอสรุป
        save_total_pills_screen = UpdatePillScreen(globalPillData)
        __main__.widget.addWidget(save_total_pills_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
        __main__.widget.removeWidget(self)


# ########### จำนวนยาต่อมื้อ ############
class AmountPillScreen(QDialog):
    def __init__(self, globalPillData):
        super().__init__()
        self.globalPillData = globalPillData
        self.setupUi(self)
        self.button_next.clicked.connect(self.saveTimesToTakePill)
        
    def setupUi(self, background_amount_pill_per_time):
        background_amount_pill_per_time.setObjectName("background_amount_pill_per_time")
        background_amount_pill_per_time.resize(800, 480)
        background_amount_pill_per_time.setStyleSheet("QWidget#background_amount_pill_per_time{\n"
"background-color: #97C7F9}")
        self.no_channel = QtWidgets.QLabel(background_amount_pill_per_time)
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 190, 70))
        font = QtGui.QFont()
        font.setFamily("TH Sarabun New")
        font.setPointSize(36)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF; font: 75 36pt \"TH Sarabun New\"; border-radius: 25px; color: #070021; font-weight: bold;")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")
        
        self.text_question_amount_pill_per_time = QtWidgets.QLabel(background_amount_pill_per_time)
        self.text_question_amount_pill_per_time.setGeometry(QtCore.QRect(245, 30, 450, 70))
        self.text_question_amount_pill_per_time.setStyleSheet("font: 36pt \"TH Sarabun New\" ; font-weight: bold;")
        self.text_question_amount_pill_per_time.setAlignment(QtCore.Qt.AlignLeft)
        self.text_question_amount_pill_per_time.setObjectName("text_question_amount_pill_per_time")
        
        self.line_edit_amount_pill_per_time = QtWidgets.QLineEdit(background_amount_pill_per_time)
        self.line_edit_amount_pill_per_time.setGeometry(QtCore.QRect(275, 115, 250, 70))
        self.line_edit_amount_pill_per_time.setStyleSheet("background-color: #ffffff; font: 36pt \"TH Sarabun New\"; border-radius: 20px; font-weight: bold;")
        self.line_edit_amount_pill_per_time.setAlignment(QtCore.Qt.AlignCenter)
        self.line_edit_amount_pill_per_time.setValidator(QtGui.QIntValidator(0, 10))  # Set limit from 0 to 10
        self.line_edit_amount_pill_per_time.setObjectName("line_edit_amount_pill_per_time")
        
        # Numpad Layout
        self.numpad_layout = QtWidgets.QGridLayout()
        self.numpad_layout.setSpacing(8)  # เพิ่มระยะห่างระหว่างปุ่ม
        self.numpad_layout.setContentsMargins(310, 200, 200, 0)  # Set margins for better positioning

        # Create Numpad buttons (1-9)
        self.numpad_buttons = []
        for i in range(1,10):
            button = QtWidgets.QPushButton(str(i))
            button.setMinimumSize(55, 55)  # ปรับขนาดปุ่มให้เล็กลง
            button.setStyleSheet("font: 28pt \"TH Sarabun New\"; background-color: white; border-radius: 10px; font-weight: bold;")
            button.clicked.connect(self.numpad_button_clicked)
            row = (i - 1) // 3  # จัดปุ่ม 3 ปุ่มต่อแถว
            col = (i - 1) % 3   # จัดตำแหน่งปุ่มตามลำดับคอลัมน์
            self.numpad_layout.addWidget(button, row, col)
            self.numpad_buttons.append(button)
            
        # Button for 0 and backspace
        self.button_zero = QtWidgets.QPushButton("0")
        self.button_zero.setMinimumSize(55, 55)  # ปรับขนาดปุ่มให้เล็กลง
        self.button_zero.setStyleSheet("font: 28pt \"TH Sarabun New\"; background-color: white; border-radius: 10px; font-weight: bold;")
        self.button_zero.clicked.connect(self.numpad_button_clicked)
        
        # Button for backspace
        self.button_backspace = QtWidgets.QPushButton("ลบ")
        self.button_backspace.setMinimumSize(55, 55)  # ปรับขนาดปุ่มให้เล็กลง
        self.button_backspace.setStyleSheet("font: 28pt \"TH Sarabun New\"; background-color: white; border-radius: 10px; font-weight: bold;")
        self.button_backspace.clicked.connect(self.numpad_backspace)
        
        # Add 0 and Backspace to the last row
        self.numpad_layout.addWidget(self.button_zero, 3, 0, 1, 2)  # ปุ่ม 0 ในตำแหน่งกลางแถวสุดท้าย 2 ช่อง
        self.numpad_layout.addWidget(self.button_backspace, 3, 2)  # ปุ่มลบในตำแหน่งขวาสุดของแถวสุดท้าย
        
        # Add Numpad layout to background
        numpad_widget = QtWidgets.QWidget(background_amount_pill_per_time)
        numpad_widget.setLayout(self.numpad_layout)
        
        self.button_next = QtWidgets.QToolButton(background_amount_pill_per_time)
        self.button_next.setGeometry(QtCore.QRect(580, 375, 200, 90))
        self.button_next.setStyleSheet("QToolButton { font: 75 36pt \"TH Sarabun New\"; font-weight: bold; background-color:#24BD73; color: #ffffff; border-radius:20px; }"
                                        "QToolButton:hover { font: 75 36pt \"TH Sarabun New\"; font-weight: bold; background-color:#23B36D; color: #ffffff; border-radius:20px; }")
        self.button_next.setObjectName("button_next")

        self.retranslateUi(background_amount_pill_per_time)
        QtCore.QMetaObject.connectSlotsByName(background_amount_pill_per_time)
    
    def retranslateUi(self, background_amount_pill_per_time):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        channelID = "ช่องที่ " + str(globalPillData["channelId"] + 1)

        background_amount_pill_per_time.setWindowTitle(_translate("background_amount_pill_per_time", "Dialog"))
        self.no_channel.setText(_translate("background_amount_pill_per_time", channelID))
        self.text_question_amount_pill_per_time.setText(_translate("background_amount_pill_per_time", "จำนวนยาที่ต้องกินต่อครั้ง"))
        self.button_next.setText(_translate("background_amount_pill_per_time", "บันทึก"))

        # Numpad button click event handler
    
    def numpad_button_clicked(self):
        sender = self.sender()
        current_value = self.line_edit_amount_pill_per_time.text()
        new_value = current_value + sender.text()
        if len(new_value) <= 2:  # Ensure max 2 digits
            self.line_edit_amount_pill_per_time.setText(new_value)

    # Backspace button click event handler
    def numpad_backspace(self):
        current_value = self.line_edit_amount_pill_per_time.text()
        self.line_edit_amount_pill_per_time.setText(current_value[:-1])

    def saveTimesToTakePill(self):
        amount_pill_per_time = self.line_edit_amount_pill_per_time.text()
        if not amount_pill_per_time:
            return

        global globalPillData
        globalPillData["pillsPerTime"] = int(amount_pill_per_time)
        # print("globalPillData(AmountUP):", globalPillData)
        
        # เปลี่ยนไปยังหน้าจอสรุป
        save_amount_pill_screen = UpdatePillScreen(globalPillData)
        __main__.widget.addWidget(save_amount_pill_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
        __main__.widget.removeWidget(self)


########### หน้ารวมเวลา ############
class AddSummaryTimeScreen(QDialog):
    def __init__(self, pillData):
        super().__init__()
        global globalTimesToTakePillArr
        global globalPillData
        globalTimesToTakePillArr = pillData['timeToTake']
        globalPillData = pillData
        self.timesToTakesPillArr = globalTimesToTakePillArr
        self.setupUi(self)
        self.success_button.clicked.connect(self.saveTimeToTake)

    def setupUi(self, background_confirm_times_to_take_pill):
        background_confirm_times_to_take_pill.setObjectName("background_confirm_times_to_take_pill")
        background_confirm_times_to_take_pill.resize(800, 480)
        background_confirm_times_to_take_pill.setStyleSheet("QWidget#background_confirm_times_to_take_pill{\n""background-color: #97C7F9}")
        self.no_channel = QtWidgets.QLabel(background_confirm_times_to_take_pill)
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 190, 70))
        font = QtGui.QFont()
        font.setFamily("TH Sarabun New")
        font.setPointSize(36)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF; font: 36pt \"TH Sarabun New\"; font-weight: bold; border-radius: 25px; color: #070021; ")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")
        
        self.header_text = QtWidgets.QLabel(background_confirm_times_to_take_pill)
        self.header_text.setGeometry(QtCore.QRect(245, 30, 450, 70))
        self.header_text.setStyleSheet("font: 36pt \"TH Sarabun New\"; font-weight: bold;")
        self.header_text.setAlignment(QtCore.Qt.AlignLeft)
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
        self.add_time_button.clicked.connect(self.gotoInputTimeToTakePillScreen)
        self.add_time_button.setObjectName("add_time_button")
        
        for idx, time in enumerate(self.timesToTakesPillArr) :
            objIndex = self.timesToTakesPillArr.index(time)

            timeToTakePillLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            timeToTakePillLabel.setMinimumSize(QtCore.QSize(250, 0))
            timeToTakePillLabel.setMaximumSize(QtCore.QSize(250, 16777215))
            timeToTakePillLabel.setStyleSheet("background-color: none;\n""font: 30pt \"TH Sarabun New\";\n""font-weight: bold; border-radius: 25px;\n""color: #070021;\n""background-color: #C5E1FF;")
            timeToTakePillLabel.setAlignment(QtCore.Qt.AlignCenter)
            timeToTakePillLabel.setText("เวลาที่ " + str(objIndex + 1))
            timeToTakePillLabel.setObjectName("question_time_no" + str(objIndex))
            self.gridLayout.addWidget(timeToTakePillLabel, 9+objIndex, 0, 1, 1)

            timeToTakePillData = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            timeToTakePillData.setStyleSheet("font: 36pt \"TH Sarabun New\";\n""font-weight: bold; color: #070021;\n""")
            timeToTakePillData.setText(time)
            timeToTakePillData.setObjectName("show_time_" + str(objIndex))
            self.gridLayout.addWidget(timeToTakePillData, 9+objIndex, 1, 1, 1)

            timeToTakePillEditButton = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
            timeToTakePillEditButton.setIconSize(QtCore.QSize(68, 68))
            timeToTakePillEditButton.setIcon(QtGui.QIcon('../Klongyaa/shared/images/edit2.png'))
            timeToTakePillEditButton.setStyleSheet("background-color : rgb(255, 74, 74); border-radius: 35px;")
    
            timeToTakePillEditButton.setObjectName("button_edit_time_" + str(objIndex))
            
            timeToTakePillEditButton.clicked.connect(partial(self.editTimeToTakePill, idx))

            timeToTakePillEditButton.setText( "🖉")
            self.gridLayout.addWidget(timeToTakePillEditButton, 9+objIndex, 2, 1, 1)


        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.success_button = QtWidgets.QToolButton(background_confirm_times_to_take_pill)
        self.success_button.setGeometry(QtCore.QRect(295, 375, 200, 90))
        self.success_button.setMinimumSize(QtCore.QSize(100, 50))
        self.success_button.setStyleSheet("QToolButton#success_button {\n"" font-weight: bold;  font:  36pt \"TH Sarabun New\";\n""    background-color:#24BD73;\n""    color: #ffffff;\n""    border-radius:20px;\n""    width: 170px;\n""    height: 100px;\n""}\n""QToolButton#success_button:hover {\n""   font-weight: bold; font: 75 36pt \"TH Sarabun New\";\n""    background-color:#23B36D;\n""    color: #ffffff;\n""    border-radius:20px;\n""    width: 170px;\n""    height:100px;\n""}")
        self.success_button.setObjectName("success_button")

        self.retranslateUi(background_confirm_times_to_take_pill)
        QtCore.QMetaObject.connectSlotsByName(background_confirm_times_to_take_pill)

    def retranslateUi(self, background_confirm_times_to_take_pill):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        channelID = "ช่องที่ " + str(globalPillData["channelId"] + 1)

        background_confirm_times_to_take_pill.setWindowTitle(_translate("background_confirm_times_to_take_pill", "Dialog"))
        self.no_channel.setText(_translate("background_confirm_times_to_take_pill", channelID))
        self.header_text.setText(_translate("background_confirm_times_to_take_pill", "เวลาที่ต้องทานยา"))
        self.success_button.setText(_translate("background_confirm_times_to_take_pill", "บันทึก"))

    
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
        
    def gotoInputTimeToTakePillScreen(self):
        global globalPillData
        screen = InputTimeToTakePillScreen(globalPillData, None, False)
        __main__.widget.removeWidget(self)
        __main__.widget.addWidget(screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
        
    
    def saveTimeToTake(self):
        global globalTimesToTakePillArr
        global globalPillData
        globalPillData["timeToTake"] = globalTimesToTakePillArr
        
        success_button = UpdatePillScreen(globalPillData)
        __main__.widget.addWidget(success_button)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
        __main__.widget.removeWidget(self)


# ########### แก้ไชเวลา ############
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
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 190, 70))
        font = QtGui.QFont()
        font.setFamily("TH Sarabun New")
        font.setPointSize(36)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF; font: 75 36pt \"TH Sarabun New\"; font-weight: bold; border-radius: 25px; color: #070021; ")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")
        
        self.question_input_times_to_take_pill = QtWidgets.QLabel(background_input_times_to_take_pill)
        self.question_input_times_to_take_pill.setGeometry(QtCore.QRect(245, 30, 450, 70))
        self.question_input_times_to_take_pill.setStyleSheet("font: 36pt \"TH Sarabun New\"; font-weight: bold;")
        self.question_input_times_to_take_pill.setAlignment(QtCore.Qt.AlignLeft)
        self.question_input_times_to_take_pill.setObjectName("question_input_times_to_take_pill")

        # Time Frame
        self.time_frame = QtWidgets.QFrame(background_input_times_to_take_pill)
        self.time_frame.setGeometry(QtCore.QRect(75, 120, 650, 265))
        self.time_frame.setStyleSheet("background-color:#97C7F9; border: none")

        # Hour Frame
        self.hour_frame = QtWidgets.QFrame(self.time_frame)
        self.hour_frame.setGeometry(QtCore.QRect(50, 10, 250, 240))
        self.hour_frame.setStyleSheet("background-color:#97C7F9; border: none")

        # Minute Frame
        self.minute_frame = QtWidgets.QFrame(self.time_frame)
        self.minute_frame.setGeometry(QtCore.QRect(350, 10, 250, 240))
        self.minute_frame.setStyleSheet("background-color:#97C7F9; border: none")

        # Colon Label (for ':')
        self.colon_label = QtWidgets.QLabel(":", self.time_frame)
        self.colon_label.setFont(QtGui.QFont("TH Sarabun New", 96, QtGui.QFont.Bold))
        self.colon_label.setStyleSheet("color: black; background-color:#97C7F9;")
        self.colon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.colon_label.setGeometry(QtCore.QRect(300, 58, 50, 125))  # Adjust size and position
        self.colon_label.setObjectName("colon_label")

        # Hour Display
        self.hour_display = QtWidgets.QLabel(f"{self.selected_hour:02d}", self.hour_frame)
        self.hour_display.setFont(QtGui.QFont("TH Sarabun New", 96, QtGui.QFont.Bold))
        self.hour_display.setStyleSheet("color: black; background-color:#97C7F9; padding: 10px; font-weight: bold;")
        self.hour_display.setAlignment(QtCore.Qt.AlignCenter)
        self.hour_display.setGeometry(QtCore.QRect(0, 58, 250, 125))

        # Minute Display
        self.minute_display = QtWidgets.QLabel(f"{self.selected_minute:02d}", self.minute_frame)
        self.minute_display.setFont(QtGui.QFont("TH Sarabun New", 96, QtGui.QFont.Bold))
        self.minute_display.setStyleSheet("color: black; background-color:#97C7F9; padding: 10px; font-weight: bold;")
        self.minute_display.setAlignment(QtCore.Qt.AlignCenter)
        self.minute_display.setGeometry(QtCore.QRect(0, 58, 250, 125))

        # Up Hour Button
        self.up_hour_button = QtWidgets.QPushButton("▲", self.hour_frame)
        self.up_hour_button.setFont(QtGui.QFont("TH Sarabun New", 36))
        self.up_hour_button.setStyleSheet("background-color: #97C7F9; font-weight: bold; border-radius: 4px;")
        self.up_hour_button.setGeometry(QtCore.QRect(0, 0, 250, 65))

        # Down Hour Button
        self.down_hour_button = QtWidgets.QPushButton("▼", self.hour_frame)
        self.down_hour_button.setFont(QtGui.QFont("TH Sarabun New", 36))
        self.down_hour_button.setStyleSheet("background-color: #97C7F9; font-weight: bold; border-radius: 4px;")
        self.down_hour_button.setGeometry(QtCore.QRect(0, 175, 250, 65))

        # Up Minute Button
        self.up_minute_button = QtWidgets.QPushButton("▲", self.minute_frame)
        self.up_minute_button.setFont(QtGui.QFont("TH Sarabun New", 36))
        self.up_minute_button.setStyleSheet("background-color: #97C7F9; font-weight: bold; border-radius: 4px;")
        self.up_minute_button.setGeometry(QtCore.QRect(0, 0, 250, 65))

        # Down Minute Button
        self.down_minute_button = QtWidgets.QPushButton("▼", self.minute_frame)
        self.down_minute_button.setFont(QtGui.QFont("TH Sarabun New", 36))
        self.down_minute_button.setStyleSheet("background-color: #97C7F9; font-weight: bold; border-radius: 4px;")
        self.down_minute_button.setGeometry(QtCore.QRect(0, 175, 250, 65))

        # Correct button (green)
        self.button_correct_pill_name = QtWidgets.QToolButton(background_input_times_to_take_pill)
        self.button_correct_pill_name.setGeometry(QtCore.QRect(295, 375, 200, 90))
        self.button_correct_pill_name.setStyleSheet("""
    QToolButton#button_correct_pill_name {
        font: 36pt "TH Sarabun New";
        font-weight: bold;
        background-color: #24BD73;
        color: #ffffff;
        border-radius: 20px;
    }
    QToolButton#button_correct_pill_name:hover {
        font: 36pt "TH Sarabun New";
        font-weight: bold;
        background-color: #23B36D;
        color: #ffffff;
        border-radius: 20px;
    }
""")
        self.button_correct_pill_name.setObjectName("button_correct_pill_name")
        self.button_correct_pill_name.clicked.connect(self.goToAddSummaryTimeScreen)
        
        self.retranslateUi(background_input_times_to_take_pill)
        QtCore.QMetaObject.connectSlotsByName(background_input_times_to_take_pill)

    def retranslateUi(self, background_input_times_to_take_pill):
        _translate = QtCore.QCoreApplication.translate
        global globalPillData
        
        channelID = "ช่องที่ " + str(globalPillData["channelId"] + 1)
        background_input_times_to_take_pill.setWindowTitle(_translate("background_input_times_to_take_pill", "Dialog"))
        self.no_channel.setText(_translate("background_input_times_to_take_pill", channelID))
        self.question_input_times_to_take_pill.setText(_translate("background_input_times_to_take_pill", "เพิ่มเวลาทานยา"))
        self.button_correct_pill_name.setText(_translate("background_total_pills", "ถัดไป"))
    
    def connect_signals(self):
        self.up_hour_button.clicked.connect(lambda: self.change_time("hour", 1))
        self.down_hour_button.clicked.connect(lambda: self.change_time("hour", -1))
        self.up_minute_button.clicked.connect(lambda: self.change_time("minute", 5))
        self.down_minute_button.clicked.connect(lambda: self.change_time("minute", -5))
        
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
        # print(json.dumps(globalPillData, indent=4))
        add_summary_time_screen = AddSummaryTimeScreen(globalPillData)
        __main__.widget.addWidget(add_summary_time_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)


