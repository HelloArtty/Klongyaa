import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QStackedWidget, QInputDialog, QMessageBox
from shared.data.light_list import lightList
from shared.data.mock.config import config
import speech_recognition as sr
from screen.pillSummaryScreen.main_pillSummaryScreen import PillSummaryScreen
from screen.inputTimesToTakePill.main_inputTimesToTakePill import *
import requests

# Screen UI
from screen.homeScreen.main_homeScreen import HomeScreen

config_path = "/home/klongyaa1/Desktop/GUI-Klongyaa-seniorProject/shared/data/mock/config.py"

haveToTake = []

# Function for speech recognition
def speech_recog_function():
    mic = sr.Microphone(device_index=2)
    recog = sr.Recognizer()

    with mic as source:
        audio = recog.listen(source)
        text = recog.recognize_google(audio, language="th")
    
    return text



def save_userId(userId):
    global config_path
    with open(config_path, 'r') as file:
        lines = file.readlines()
    with open(config_path, 'w') as file:
        for line in lines:
            if line.strip().startswith('"userId"'):
                file.write(f'    "userId": "{userId}",\n')
            else:
                file.write(line)

def show_confirmation_dialog(user_id):
    dialog = QtWidgets.QDialog()
    dialog.setWindowTitle("Confirm")
    dialog.resize(800, 480)
    dialog.setStyleSheet("background-color : #97C7F9 ")

    layout = QtWidgets.QVBoxLayout()

    # สร้าง QLabel สำหรับข้อความยืนยัน
    label = QtWidgets.QLabel(f"รหัสของคุณคือ<br><font color='red'>{user_id}</font><br>กรุณาตรวจสอบให้เรียบร้อยก่อนกดยืนยัน")
    label.setStyleSheet("font-size: 34px; font-weight: bold; margin-bottom: 20px; text-align: center;")
    label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(label)
    

    # สร้าง QDialogButtonBox พร้อมปุ่ม Ok และ Cancel
    buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
    buttonBox.setStyleSheet("QPushButton { font-size: 18px; padding: 10px; }")
    layout.addWidget(buttonBox)

    buttonBox.accepted.connect(dialog.accept)
    buttonBox.rejected.connect(dialog.reject)

    dialog.setLayout(layout)

    return dialog.exec_()

def show_error_dialog(message):
    dialog = QtWidgets.QDialog()
    dialog.setWindowTitle("Error")
    dialog.resize(800, 480)
    dialog.setStyleSheet("background-color : #97C7F9 ")

    layout = QtWidgets.QVBoxLayout()

    label = QtWidgets.QLabel(message)
    label.setStyleSheet("font-size: 34px; font-weight: bold; margin-bottom: 20px; text-align: center; color: red;")
    label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(label)

    buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
    buttonBox.setStyleSheet("QPushButton { font-size: 16px; padding: 10px; }")
    layout.addWidget(buttonBox)

    buttonBox.accepted.connect(dialog.accept)

    dialog.setLayout(layout)

    dialog.exec_()

def check_and_update_user_id():
    while not config['userId']:  # ตรวจสอบว่าค่า userId ใน config มีค่าอยู่หรือไม่ ถ้าไม่มีก็จะวนลูป
        dialog = QtWidgets.QDialog()  # สร้าง QDialog สำหรับรับค่า userId
        dialog.setWindowTitle("User ID")  # ตั้งชื่อหน้าต่างเป็น "User ID"
        dialog.resize(800, 480)  # ตั้งขนาดหน้าต่างเป็น 800x480
        dialog.setStyleSheet("background-color : #97C7F9 ")

        layout = QtWidgets.QVBoxLayout()  # สร้าง QVBoxLayout สำหรับจัดวาง widget ในแนวตั้ง

        # สร้าง QLabel สำหรับข้อความ "กรุณากรอกรหัสของคุณ"
        label = QtWidgets.QLabel("กรุณากรอกรหัสของคุณ")
        # ตั้งค่ารูปแบบของข้อความ
        label.setStyleSheet("font-size: 34px; font-weight: bold; margin-bottom: 20px; text-align: center;")
        label.setAlignment(QtCore.Qt.AlignCenter)  # จัดข้อความให้อยู่ตรงกลาง
        edit = QtWidgets.QLineEdit()  # สร้าง QLineEdit สำหรับให้ผู้ใช้กรอก userId
        edit.setStyleSheet("font-size: 16px; padding: 10px; background-color : lightgray")  # ตั้งค่ารูปแบบของ QLineEdit
        edit.setFixedSize(780, 40)  # ตั้งขนาด QLineEdit เป็น 780x40
        layout.addWidget(label)  # เพิ่ม QLabel ลงใน layout
        layout.addWidget(edit)  # เพิ่ม QLineEdit ลงใน layout

        # สร้าง QDialogButtonBox พร้อมปุ่ม Ok
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        # ตั้งค่ารูปแบบของปุ่ม
        buttonBox.setStyleSheet("QPushButton { font-size: 16px; padding: 10px; }")
        buttonBox.setFixedSize(780, 40)  # ตั้งขนาดของปุ่มเป็น 780x40
        layout.addWidget(buttonBox)  # เพิ่ม QDialogButtonBox ลงใน layout

        buttonBox.accepted.connect(dialog.accept)  # เชื่อมสัญญาณ accepted ของปุ่ม Ok กับฟังก์ชัน accept ของ dialog
        buttonBox.rejected.connect(dialog.reject)  # เชื่อมสัญญาณ rejected ของปุ่ม Ok กับฟังก์ชัน reject ของ dialog

        dialog.setLayout(layout)  # ตั้ง layout ให้กับ dialog

        if dialog.exec_() == QtWidgets.QDialog.Accepted:  # ถ้าผู้ใช้กดปุ่ม Ok ใน dialog
            user_id = edit.text()  # รับค่าจาก QLineEdit
            if user_id:  # ถ้ามีค่าที่กรอก
                # แสดงกล่องข้อความเพื่อยืนยันการกรอก userId
                if show_confirmation_dialog(user_id) == QtWidgets.QDialog.Accepted:  # ถ้าผู้ใช้กดปุ่ม Ok
                    save_userId(user_id)  # เรียกฟังก์ชัน save_userId เพื่อบันทึก userId
                    config['userId'] = user_id  # ตั้งค่า userId ใน config ให้เป็นค่าที่กรอก
                else:
                    continue  # ถ้าผู้ใช้กดปุ่ม Cancel จะกลับไปให้กรอกใหม่อีกครั้ง
            elif user_id == "":  # ถ้าไม่ได้กรอกค่าอะไร
                show_error_dialog("User ID cannot be empty!")  # แสดงข้อความแจ้งเตือนว่า userId ไม่สามารถเป็นค่าว่างได้
            else:
                show_error_dialog("User ID is required!")  # แสดงข้อความแจ้งเตือนว่า userId เป็นสิ่งจำเป็น


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    check_and_update_user_id()

    pill_channel_datas = {
        "0": {},
        "1": {},
        "2": {},
        "3": {},
        "4": {}, 
        "5": {}, 
        "6": {}, 
        "7": {}
    }
    res = requests.get(config["url"] + "/pill-data/getHardwarePillChannelDatas/" + config["userId"])
    print(config["url"])
    print(config["userId"])
    print(config["isFirstUse"])
    print(res)
    
    for pill in res.json()['pill_channel_datas']:
        times = []
        for time in pill['take_times']:
            times.append(time.replace('.', ':'))
        idStr = str(int(pill['channel_id']) )
        pill_channel_datas[idStr]['id'] = int(idStr)
        pill_channel_datas[idStr]['name'] = pill['pill_name']
        pill_channel_datas[idStr]['totalPills'] = pill['total']
        pill_channel_datas[idStr]['pillsPerTime'] = pill['pillsPerTime']
        pill_channel_datas[idStr]['timeToTake'] = times

    print(pill_channel_datas)
    defaultfont = QtGui.QFont('Arial', 8)
    defaultfont.setPixelSize(8)
    QtWidgets.QApplication.setStyle("Windows")
    QtWidgets.QApplication.setFont(defaultfont)
    screen = HomeScreen(pill_channel_datas, config)
    widget = QStackedWidget()
    widget.setWindowTitle("GUI - KLONG_YAA")
    widget.addWidget(screen)
    widget.setFixedWidth(800)
    widget.setFixedHeight(480)
    widget.show()
    sys.exit(app.exec_())

    
