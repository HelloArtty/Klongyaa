import json
import sys
from functools import partial

import __main__
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog

from shared.main_success_save_screen import SuccessSaveScreen

globalPillData = {}
globalInputPillName = ""
mockNum = 0

class PillSummaryScreen(QDialog):
    def __init__(self, pillData=None, pillNames=None, pillID=None, parent=None):
        super().__init__(parent)
        global globalPillData
        globalPillData = pillData if pillData is not None else {}
        self.pillNames = pillNames if pillNames is not None else []
        self.pillID = pillID if pillID is not None else []
        self.inputPillName = globalPillData.get("name", "")
        self.inputPillID = globalPillData.get("pillId", "")
        self.setupUi(self)
        self.button_save_pill_summary.clicked.connect(self.savePillSummary)
        # print(f"ข้อมูลยา = {globalPillData}")
        
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

    #หน้าสรุป
    def setupUi(self, background_summary_screen):
        global globalPillData
        currentRow = 0

        # Setup background
        background_summary_screen.setObjectName("background_summary_screen")
        background_summary_screen.resize(800, 480)
        background_summary_screen.setStyleSheet("QWidget#background_summary_screen{ background-color: #97C7F9 }")

        # Header label
        self.text_header_summary_screen = QtWidgets.QLabel(background_summary_screen)
        self.text_header_summary_screen.setGeometry(QtCore.QRect(290, 20, 375, 60))
        self.text_header_summary_screen.setStyleSheet("font: 75 34pt \"JasmineUPC\";")
        self.text_header_summary_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.text_header_summary_screen.setObjectName("text_header_summary_screen")

        # Scroll area setup
        self.scroll_area = QtWidgets.QScrollArea(background_summary_screen)
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

        # Pill name section
        # ชื่อยา
        self.question_pill_name = QtWidgets.QLabel("Pill Name", self.scrollAreaWidgetContents)
        self.question_pill_name.setMinimumSize(250, 35)
        font = QtGui.QFont("JasmineUPC", 30)
        self.question_pill_name.setFont(font)
        self.question_pill_name.setStyleSheet("background-color: #C5E1FF; ;border-radius: 25px; color: #070021;")
        self.question_pill_name.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter )
        self.question_pill_name.setContentsMargins(20, 0, 0, 0) 
        self.gridLayout_2.addWidget(self.question_pill_name, currentRow, 0, 1, 1)
        # รายละเอียดชื่อยา
        self.show_pill_name = self.createLabel("", 200, 40, "font: 75 32pt \"JasmineUPC\"; color: #070021; border: none; margin-right:50px;", self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.show_pill_name, currentRow, 1, 1, 1)
        # แก้ไข
        self.button_edit_pill_name = self.createToolButton("edit2.png", self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.button_edit_pill_name, currentRow, 3, 1, 1)

        currentRow += 1

        # Total pills section
        if globalPillData["totalPills"] > 0:
            self.question_total_pills = QtWidgets.QLabel("จำนวนยาทั้งหมด", self.scrollAreaWidgetContents)
            self.question_total_pills.setMinimumSize(250, 35)  # กำหนดขนาดขั้นต่ำ
            font = QtGui.QFont("JasmineUPC", 30)  # กำหนดฟอนต์
            self.question_total_pills.setFont(font)  # ตั้งค่าให้กับ QLabel
            self.question_total_pills.setStyleSheet("background-color: #C5E1FF; border-radius: 25px; color: #070021;")  # ตั้งค่ารูปแบบ
            self.question_total_pills.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)  # จัดเรียงชิดซ้ายและกลางแนวตั้ง
            self.question_total_pills.setContentsMargins(20, 0, 0, 0)  # ตั้งค่าระยะห่าง
            self.gridLayout_2.addWidget(self.question_total_pills, currentRow, 0, 1, 1)  # เพิ่มเข้าไปใน layout
            self.show_total_pills = self.createLabel(f"{globalPillData['totalPills']} เม็ด", 200, 40, "font: 75 34pt \"JasmineUPC\"; color: #070021; margin-right:50px;", self.scrollAreaWidgetContents)
            self.gridLayout_2.addWidget(self.show_total_pills, currentRow, 1, 1, 1)
            self.button_edit_total_pills = self.createToolButton("edit2.png", self.scrollAreaWidgetContents)
            self.gridLayout_2.addWidget(self.button_edit_total_pills, currentRow, 3, 1, 1)

            currentRow += 1

        # Amount per dose section
        self.question_amount_pill = QtWidgets.QLabel("จำนวนยา", self.scrollAreaWidgetContents)
        self.question_amount_pill.setMinimumSize(350, 35)  # กำหนดขนาดขั้นต่ำ
        font = QtGui.QFont("JasmineUPC", 30)  # กำหนดฟอนต์
        self.question_amount_pill.setFont(font)  # ตั้งค่าให้กับ QLabel
        self.question_amount_pill.setStyleSheet("background-color: #C5E1FF; border-radius: 25px; color: #070021;")  # ตั้งค่ารูปแบบ
        self.question_amount_pill.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)  # จัดเรียงชิดซ้ายและกลางแนวตั้ง
        self.question_amount_pill.setContentsMargins(20, 0, 0, 0)  # ตั้งค่าระยะห่าง
        self.gridLayout_2.addWidget(self.question_amount_pill, currentRow, 0, 1, 1)  # เพิ่มเข้าไปใน layout
        self.show_amount_pill = self.createLabel("", 200, 40, "font: 75 34pt \"JasmineUPC\"; color: #070021; margin-right:50px;", self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.show_amount_pill, currentRow, 1, 1, 1)
        self.button_edit_amount_pill = self.createToolButton("edit2.png", self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.button_edit_amount_pill, currentRow, 3, 1, 1)

        currentRow += 1

        # Times section
        for index, time in enumerate(globalPillData["timeToTake"]):
            # สร้าง Label สำหรับเวลาทานยา
            timeToTakePillLabel = self.createLabel(
                f"เวลาที่ {index + 1}", 250, 40,
                "background-color: #C5E1FF; border-radius: 25px; color: #070021;",
                self.scrollAreaWidgetContents
            )
            timeToTakePillLabel.setFont(QtGui.QFont("JasmineUPC", 30))  # ตั้งค่าฟอนต์
            timeToTakePillLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            timeToTakePillLabel.setContentsMargins(10, 0, 0, 0)  # ระยะห่างด้านใน
            self.gridLayout_2.addWidget(timeToTakePillLabel, currentRow + index, 0, 1, 1)

            # สร้าง Label สำหรับข้อมูลเวลา
            timeToTakePillData = self.createLabel(
                f"{time} น.", 200, 40,
                "font: 75 34pt \"JasmineUPC\"; color: #070021;",
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
        self.button_save_pill_summary = QtWidgets.QToolButton(background_summary_screen)
        self.button_save_pill_summary.setGeometry(QtCore.QRect(280, 400, 220, 75))
        self.button_save_pill_summary.setStyleSheet("font: 75 36pt \"JasmineUPC\"; background-color:#24BD73; color: #ffffff; border-radius:20px;")
        self.button_save_pill_summary.setObjectName("button_save_pill_summary")

        # Channel label
        self.no_channel = QtWidgets.QLabel(background_summary_screen)
        self.no_channel.setGeometry(QtCore.QRect(40, 10, 190, 70))
        self.no_channel.setStyleSheet("background-color: #C5E1FF; font: 75 36pt \"JasmineUPC\"; border-radius: 25px; color: #070021;")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")

        # Retranslate UI
        self.retranslateUi(background_summary_screen)
        QtCore.QMetaObject.connectSlotsByName(background_summary_screen)

    # Helper methods
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
    
    def savePillSummary(self):
        global globalPillData
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

        res = requests.post(__main__.config["url"] + "/user/addPillChannel", json=pill_data)

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
            screen = PillNameScreen(globalPillData, self.pillNames) 
        elif edit_mode == "total_pills":
            screen = TotalPillsScreen()
            screen.pillData = globalPillData
        elif edit_mode == "amount_pill":
            screen = AmountPillPerTimeScreen()
            screen.pillData = globalPillData
            screen.amount_pill = globalPillData["pillsPerTime"]
        elif edit_mode == "time":
            screen = __main__.AddSummaryTimeScreen(globalPillData)

        if screen is not None:
            __main__.widget.addWidget(screen)
            __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
        # else:
        #     print(f"Error: No screen initialized for edit mode '{edit_mode}'")


# ########### ชื่อยา ############
class PillNameScreen(QDialog):
    pill_name_entered_signal = pyqtSignal(str)
    
    def __init__(self, pillData=None, pillNames=None, pillID=None, parent=None):
        super().__init__(parent)
        global globalPillData
        globalPillData = pillData if pillData is not None else {}
        self.pillNames = pillNames if pillNames is not None else []
        self.pillID = pillID if pillID is not None else []
        self.inputPillName = globalPillData.get("name", "")
        self.inputPillID = globalPillData.get("pillId", "")
        self.setupUi(self)
        self.save_button_pillname.clicked.connect(self.savePillName)
        

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
        if isinstance(self.pillNames, list) and len(self.pillNames) > 0:
            self.label_pill_name.setText(self.pillNames[self.current_pill_index])
        elif isinstance(self.pillNames, dict):
            # แก้เป็นการเข้าถึง dictionary โดยตรง
            self.label_pill_name.setText(self.pillNames.get("name", ""))
        
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
        
        self.save_button_pillname = QtWidgets.QToolButton(background_confirm_pill_name)
        self.save_button_pillname.setGeometry(QtCore.QRect(295, 375, 200, 90))
        self.save_button_pillname.setMinimumSize(QtCore.QSize(100, 50))
        self.save_button_pillname.setStyleSheet("QToolButton#save_button_pillname { font: 75 36pt \"JasmineUPC\"; background-color:#24BD73; color: #ffffff; border-radius:20px; } QToolButton#save_button_pillname:hover { font: 75 36pt \"JasmineUPC\"; background-color:#23B36D; color: #ffffff; border-radius:20px; }")
        self.save_button_pillname.setObjectName("save_button_pillname")
        
        self.retranslateUi(background_confirm_pill_name)
        QtCore.QMetaObject.connectSlotsByName(background_confirm_pill_name)

    def navigate_left(self):
        if not self.pillNames:
            return
        self.current_pill_index = (self.current_pill_index - 1) % len(self.pillNames)
        self.update_display()

    def navigate_right(self):
        if not self.pillNames:
            return
        self.current_pill_index = (self.current_pill_index + 1) % len(self.pillNames)
        self.update_display()

    def update_display(self):
        self.label_pill_name.setText(self.pillNames[self.current_pill_index])
        if self.current_pill_index < len(self.pillID):
            self.inputPillID = self.pillID[self.current_pill_index]
        else:
            print("Error: current_pill_index is out of range for pillID")

        print(f"Current index: {self.current_pill_index}, Pill Names Length: {len(self.pillNames)}, Pill IDs Length: {len(self.pillID)}")

    def retranslateUi(self, background_confirm_pill_name):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        channelID = "ช่องที่ " + str(globalPillData.get("channelId", 0) + 1)

        background_confirm_pill_name.setWindowTitle(_translate("background_confirm_pill_name", "Dialog"))
        self.no_channel.setText(_translate("background_confirm_pill_name", channelID))
        self.label_1.setText(_translate("background_confirm_pill_name", "กรุณาเลือกชื่อยาของท่าน"))
        self.save_button_pillname.setText(_translate("background_confirm_pill_name", "บันทึก"))
        
    def savePillName(self):
        selected_pill_name = self.label_pill_name.text()
        if not selected_pill_name or selected_pill_name == "โปรดเลือกชื่อยา":
            # QtWidgets.QMessageBox.warning(self, "Warning", "Please select a valid pill name.")
            return

        global globalPillData
        globalPillData["name"] = selected_pill_name
        globalPillData["pillId"] = self.inputPillID
        # Save the data to the appropriate location
        # For example, you might save it to a file or a database
        # print(json.dumps(globalPillData, indent=4))
        # print("\n บันทึกชื่อยาเรียบร้อยแล้ว \n")
    
        # เปลี่ยนไปยังหน้าจอสรุป
        save_pillname_screen = PillSummaryScreen(globalPillData, self.pillNames)
        __main__.widget.addWidget(save_pillname_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)


# ########### ยาทั้งหมด ############
class TotalPillsScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.pillData = None
        self.setupUi(self)
        #======================= set max-min of total pills =======================#
        self.slider_total_pills.setMaximum(99)
        self.slider_total_pills.setMinimum(0)
        self.slider_total_pills.valueChanged.connect(self.updateSliderTotalPills)
        self.button_save_total_pills.clicked.connect(lambda:self.saveTotalPills())
        
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
        self.button_save_total_pills.clicked.connect(self.saveTotalPills)

        # Set up translations and connections
        self.retranslateUi(background_total_pills)
        QtCore.QMetaObject.connectSlotsByName(background_total_pills)

    def retranslateUi(self, background_total_pills):
        _translate = QtCore.QCoreApplication.translate

        global globalPillData
        channelID = "ช่องที่ " + str(globalPillData["channelId"] + 1)
        
        background_total_pills.setWindowTitle(_translate("background_total_pills", "Dialog"))
        self.no_channel.setText(_translate("background_total_pills", channelID))
        self.text_question_inputting_total_pills.setText(_translate("background_total_pills", "กรุณาระบุจำนวนเม็ดยาทั้งหมดที่บรรจุ"))
        self.button_save_total_pills.setText(_translate("background_total_pills", "บันทึก"))

    def updateSliderTotalPills(self,count_of_total_pills):
        self.lcdNumber.display(count_of_total_pills)
        self.total_pills = count_of_total_pills

    def saveTotalPills(self):
        if hasattr(self, 'total_pills'):
            global globalPillData
            globalPillData["totalPills"] = self.total_pills

            screen = PillSummaryScreen(globalPillData, self.total_pills)
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
        self.button_next.clicked.connect(self.saveTimesToTakePill)

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

    def saveTimesToTakePill(self):
        if hasattr(self, 'amount_pill') :
            global globalPillData
            globalPillData["pillsPerTime"] = self.amount_pill

            screen = PillSummaryScreen(globalPillData,self.amount_pill)
            __main__.widget.addWidget(screen)
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
        self.success_button.setStyleSheet("QToolButton#success_button {\n""       font: 75 36pt \"JasmineUPC\";\n""    background-color:#24BD73;\n""    color: #ffffff;\n""    border-radius:20px;\n""    width: 170px;\n""    height: 100px;\n""}\n""QToolButton#success_button:hover {\n""    font: 75 36pt \"JasmineUPC\";\n""    background-color:#23B36D;\n""    color: #ffffff;\n""    border-radius:20px;\n""    width: 170px;\n""    height:100px;\n""}")
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
        global globalTimesToTakePillArr
        global globalPillData
        globalPillData["timeToTake"] = globalTimesToTakePillArr

        add_summary_time_screen = __main__.PillSummaryScreen(globalPillData)
        __main__.widget.removeWidget(self)
        __main__.widget.addWidget(add_summary_time_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)


globalTimesToTakePillArr = []
mockTime = 12


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pill_names = []
    screen = PillSummaryScreen({}, pill_names)
    widget = QtWidgets.QStackedWidget()
    widget.setWindowTitle("GUI - KLONG_YAA")
    widget.addWidget(screen)
    widget.setFixedWidth(800)
    widget.setFixedHeight(480)
    widget.show()
    sys.exit(app.exec_())
try:
    sys.exit(app.exec_())
except:
    print("Exiting")