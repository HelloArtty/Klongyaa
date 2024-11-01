import json
import sys

import __main__
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QWidget

globalPillData = {}

#จำนวนยาทั้งหมด
class TotalPillsScreen(QDialog):
    def __init__(self, pillData):
        super().__init__()
        global globalPillData
        globalPillData = pillData
        self.setupUi(self)
        # ปุ่มบันทึกข้อมูล
        self.button_save_total_pills.clicked.connect(self.goToAmountPillPerTimeScreen)

    def setupUi(self, background_total_pills):
        background_total_pills.setObjectName("background_total_pills")
        background_total_pills.resize(800, 480)
        background_total_pills.setStyleSheet("QWidget#background_total_pills { background-color: #97C7F9 }")

        # Channel info
        self.no_channel = QtWidgets.QLabel(background_total_pills)
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 190, 70))
        font = QtGui.QFont()
        font.setFamily("TH Sarabun New")
        font.setPointSize(36)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF; font: 36pt \"TH Sarabun New\"; border-radius: 25px; color: #070021; font-weight: bold;")
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
        channelID = "ช่องที่ " + str(globalPillData.get("channelId") + 1)

        background_total_pills.setWindowTitle(_translate("background_total_pills", "Dialog"))
        self.no_channel.setText(_translate("background_total_pills", channelID))
        self.text_question_inputting_total_pills.setText(_translate("background_total_pills", "เม็ดยาทั้งหมดที่บรรจุ"))
        self.button_save_total_pills.setText(_translate("background_total_pills", "ถัดไป"))

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

    def goToAmountPillPerTimeScreen(self):
        global globalPillData
        total_pills_text = self.line_edit_total_pills.text()

        if total_pills_text.isdigit() and int(total_pills_text) > 0:
            globalPillData["totalPills"] = int(total_pills_text)
            pill_per_time_screen = AmountPillPerTimeScreen()
            __main__.widget.addWidget(pill_per_time_screen)
            __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "กรุณาระบุจำนวนเม็ดยาที่มากกว่า 0")

#จำนวนยาที่ต้องกินต่อมื้อ
class AmountPillPerTimeScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_next.clicked.connect(self.gotoInputTimesToTakePill)

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

        # ปุ่มบันทึก
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
        self.button_next.setText(_translate("background_amount_pill_per_time", "ถัดไป"))

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

    def gotoInputTimesToTakePill(self):
        if hasattr(self, 'line_edit_amount_pill_per_time') and self.line_edit_amount_pill_per_time.text().isdigit():
            global globalPillData
            globalPillData["pillsPerTime"] = int(self.line_edit_amount_pill_per_time.text())

            input_times_to_take_pill_screen = __main__.InputTimeToTakePillScreen(globalPillData, -1, False)
            __main__.widget.removeWidget(self)
            __main__.widget.addWidget(input_times_to_take_pill_screen)
            __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
