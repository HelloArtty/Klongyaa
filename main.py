import json
import sys

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox,
                             QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QStackedWidget, QVBoxLayout)

from screen.homeScreen.main_homeScreen import HomeScreen
from screen.inputTimesToTakePill.main_inputTimesToTakePill import *
# from screen.pillSummaryScreen.main_pillSummaryScreen import PillSummaryScreen
# from shared.data.light_list import lightList
from shared.data.mock.config import config

config_path = "../Klongyaa/shared/data/mock/config.py"

haveToTake = []

def save_userId(user_info):
    global config_path
    with open(config_path, 'r') as file:
        lines = file.readlines()
    with open(config_path, 'w') as file:
        for line in lines:
            if line.strip().startswith('"userId"'):
                file.write(f'    "userId": "{user_info["id"]}",\n')
            elif line.strip().startswith('"lineId"'):
                file.write(f'    "lineId": "{user_info["lineID"]}",\n')
            elif line.strip().startswith('"email"'):
                file.write(f'    "email": "{user_info["email"]}",\n')
            elif line.strip().startswith('"username"'):
                file.write(f'    "username": "{user_info["username"]}",\n')
            else:
                file.write(line)

def show_confirmation_dialog(email):
    dialog = QDialog()
    dialog.setWindowTitle("KLONGYAA")
    dialog.setWindowIcon(QtGui.QIcon('../Klongyaa/shared/images/icon_k.png'))
    dialog.resize(800, 480)
    dialog.setStyleSheet("background-color : #97C7F9 ")

    layout = QVBoxLayout()

    label = QLabel(f"อีเมลของคุณคือ<br><font color='red'>{email}</font><br>กรุณาตรวจสอบให้เรียบร้อยก่อนกดยืนยัน")
    label.setStyleSheet("font-size: 34px; font-weight: bold; text-align: center;")
    label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(label)

    buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttonBox.setStyleSheet(
        '''
        QPushButton {
            font: 75 36pt "JasmineUPC";
            font-size: 24px;
            padding: 10px;
            color: #ffffff;
            border-radius: 5px;
            width: 150px;
            height: 40px;
        }
        QPushButton:hover {
            background-color: #24BD73;
        }
        QPushButton:enabled {
            background-color: #23B36D;
            border: 2px solid #2E8B57;
        }
        QPushButton#button_incorrect_pill_name {
            background-color: #DD5D5D;
            border-radius: 20px;
        }
        QPushButton#button_incorrect_pill_name:hover {
            background-color: rgb(255, 50, 50);
            border-radius: 20px;
        }
        '''
    )

    # Get the Ok and Cancel buttons
    ok_button = buttonBox.button(QDialogButtonBox.Ok)
    ok_button.setText("ยืนยัน")
    ok_button.setMinimumWidth(150)

    cancel_button = buttonBox.button(QDialogButtonBox.Cancel)
    cancel_button.setText("ย้อนกลับ")
    cancel_button.setMinimumWidth(150)
    cancel_button.setStyleSheet(
        '''
        QPushButton {
            font: 75 36pt "JasmineUPC";
            font-size: 24px;
            padding: 10px;
            color: #ffffff;
            border-radius: 5px;
            width: 150px;
            height: 40px;
            background-color: #DD5D5D;
            border: 2px solid #B22222;
        }
        QPushButton:hover {
            background-color: #FF3232;
        }
        '''
    )

    layout.addWidget(buttonBox, alignment=QtCore.Qt.AlignCenter)

    # Connect signals before exec_
    buttonBox.accepted.connect(dialog.accept)
    buttonBox.rejected.connect(dialog.reject)

    dialog.setLayout(layout)

    result = dialog.exec_()
    return result

def show_error_dialog(message):
    dialog = QDialog()
    dialog.setWindowTitle("KLONGYAA")
    dialog.setWindowIcon(QtGui.QIcon('../Klongyaa/shared/images/icon_k.png'))
    dialog.resize(800, 480)
    dialog.setStyleSheet("background-color: #97C7F9;")

    layout = QVBoxLayout()
    message = "กรุณากรอกข้อมูลเพื่อดำเนินการต่อ"
    label = QLabel(message)
    label.setStyleSheet("font-size: 34px; font-weight: bold; margin-bottom: 20px; text-align: center; color: red;")
    label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(label)

    buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
    buttonBox.setStyleSheet(
        '''
        QPushButton {
            font: 75 36pt "JasmineUPC";
            font-size: 24px;
            padding: 10px;
            background-color: #23B36D;
            color: #ffffff;
            border-radius: 5px;
            border: 2px solid #2E8B57;
            min-width: 150px;
            min-height: 40px;
        }
        QPushButton:hover {
            background-color: #24BD73;
        }
        '''
    )
    ok_button = buttonBox.button(QDialogButtonBox.Ok)
    ok_button.setText("ตกลง")
    layout.addWidget(buttonBox, alignment=QtCore.Qt.AlignCenter)  # จัดหน้าตา buttonBox ไว้ตรงกลาง
    buttonBox.accepted.connect(dialog.accept)
    dialog.setLayout(layout)
    dialog.exec_()

def get_line_id_from_backend(username):
    print(username)
    try:
        url = config["url"] + "/user/pillboxLogin/" + str(username)
        response = requests.get(url)
        print(f"Response object: {response}")
        if response.status_code == 200:
            data = response.json()
            print(f"Data received: {data} \n")
            
            # Return the required information as a dictionary
            result = {
                'id': data.get('id'),
                'email': data.get('email'),
                'username': data.get('username'),
                'lineID': data.get('lineID')
            }
            return result
        else:
            print(f"Error: Unable to fetch id, status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def check_and_update_user_id():
    global config

    while not config['userId']:
        dialog = QDialog()
        dialog.setWindowTitle("KLONGYAA")
        dialog.setWindowIcon(QtGui.QIcon('../Klongyaa/shared/images/icon_k.png'))
        dialog.resize(800, 480)
        dialog.setStyleSheet("background-color : #97C7F9 ")

        layout = QVBoxLayout()

        label = QLabel("กรุณากรอกชื่อผู้ใช้ของคุณ")
        label.setStyleSheet("font-size: 34px; font-weight: bold; margin-bottom: 20px; text-align: center;")
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        edit = QLineEdit()
        edit.setStyleSheet("font-size: 16px; padding: 10px; background-color : lightgray")
        edit.setFixedSize(780, 40)
        layout.addWidget(edit)

        keyboard_layout = QGridLayout()
        layout.addLayout(keyboard_layout)

        # Create buttons for letters A-Z
        letters = [
            ('a', 1, 0), ('b', 1, 1), ('c', 1, 2), ('d', 1, 3), ('e', 1, 4),
            ('f', 1, 5), ('g', 1, 6), ('h', 1, 7),
            ('i', 2, 0), ('j', 2, 1), ('k', 2, 2), ('l', 2, 3), ('m', 2, 4),
            ('n', 2, 5), ('o', 2, 6), ('p', 2, 7), ('q', 2, 8),
            ('r', 3, 0), ('s', 3, 1), ('t', 3, 2), ('u', 3, 3), ('v', 3, 4),
            ('w', 3, 5), ('x', 3, 6), ('y', 3, 7), ('z', 3, 8)
        ]              

        # Create buttons for numbers 0-9
        numbers = [
            ('7', 1, 10), ('8', 1, 11), ('9', 1, 12),
            ('4', 2, 10), ('5', 2, 11), ('6', 2, 12),
            ('1', 3, 10), ('2', 3, 11), ('3', 3, 12),
            ('0', 3, 9)
        ]

        # Function to handle button clicks
        def on_button_click(text):
            current_text = edit.text()
            edit.setText(current_text + text)

        # Function to handle shift button click
        shift_pressed = False

        def on_shift_click():
            nonlocal shift_pressed
            shift_pressed = not shift_pressed
            # Change letter buttons to uppercase if shift is pressed
            for button, (text, row, col) in letter_buttons.items():
                button.setText(text.upper() if shift_pressed else text)

        # Function to handle delete button click
        def on_delete_click():
            edit.backspace()

        # Add buttons for letters
        letter_buttons = {}
        for text, row, col in letters:
            button = QPushButton(text)
            button.setStyleSheet("font-size: 16px; padding: 10px;")
            button.clicked.connect(lambda _, t=text: on_button_click(t.upper() if shift_pressed else t))
            keyboard_layout.addWidget(button, row, col, 1, 1)
            letter_buttons[button] = (text, row, col)

        # Add shift button
        shift_button = QPushButton("Shift")
        shift_button.setStyleSheet("font-size: 16px; padding: 10px;")
        shift_button.clicked.connect(on_shift_click)
        keyboard_layout.addWidget(shift_button, 2, 9, 1, 1)

        # Add delete button
        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet("font-size: 16px; padding: 10px;")
        delete_button.clicked.connect(on_delete_click)
        keyboard_layout.addWidget(delete_button, 1, 8, 1, 2)

        # Add buttons for numbers
        for text, row, col in numbers:
            button = QPushButton(text)
            button.setStyleSheet("font-size: 16px; padding: 10px;")
            button.clicked.connect(lambda _, t=text: on_button_click(t))
            keyboard_layout.addWidget(button, row, col, 1, 1)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.setStyleSheet(
        '''
        QPushButton {
            font: 75 36pt "JasmineUPC";
            font-size: 24px;
            padding: 10px;
            background-color: #23B36D;
            color: #ffffff;
            border-radius: 5px;
            border: 2px solid #2E8B57;
            width: 80px;
            height: 30px;
        }
        QPushButton:hover {
            background-color: #24BD73;
        }
        '''
        )

        ok_button = buttonBox.button(QDialogButtonBox.Ok)
        ok_button.setText("ต่อไป")
        ok_button.setMinimumWidth(150)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)

        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            username = edit.text()
            if username:
                user_info = get_line_id_from_backend(username)
                if user_info:
                    if show_confirmation_dialog(user_info['email']) == QDialog.Accepted:
                        save_userId(user_info)
                        config['userId'] = user_info['id']
                        config['lineId'] = user_info['lineID']
                        config['email'] = user_info['email']
                        config['username'] = user_info['username']
                    else:
                        continue
                else:
                    show_error_dialog("ไม่สามารถรับข้อมูลจากระบบได้!")
            else:
                show_error_dialog("กรุณากรอกชื่อผู้ใช้!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    check_and_update_user_id()
    
    # ตั้งค่าเริ่มต้นให้กับ pill_channel_datas
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
    
    # ฟังก์ชันสำหรับอัปเดต pill_channel_datas
    def refreshPillData(config):
        url = config["url"] + "/user/hardwareGetPillChannels/" + config["userId"]
        res = requests.get(url)

        if res.status_code == 200:
            json_response = res.json()
            if isinstance(json_response, list):
                for pill in json_response:
                    id_str = str(int(pill.get('channelIndex', 0)))
                    pill_channel_datas[id_str] = {
                        'id': pill.get('id', ''),
                        'channelId': int(id_str),
                        'pillId': pill.get('medicine', {}).get('id', ''),
                        'name': pill.get('medicine', {}).get('name', ''),
                        'medicalname': pill.get('medicine', {}).get('medicalname', ''),
                        'totalPills': pill.get('total', 0),
                        'pillsPerTime': pill.get('amountPerTime', 0),
                        'timeToTake': [time.get('time', '').replace('.', ':') for time in pill.get('times', [])],
                        'img': pill.get('medicine', {}).get('img', '')
                    }
            # print(f"Updated Pill Channel Data: {json.dumps(pill_channel_datas, indent=4)}")
        else:
            print(f"Error updating pill data: {res.status_code}")

    # เรียกใช้ refreshPillData เพื่ออัปเดต pill_channel_datas
    refreshPillData(config)

    # แสดงผลลัพธ์
    # print(f"Pill Channel Data: {json.dumps(pill_channel_datas, indent=4)}")
    QtWidgets.QApplication.setFont(QtGui.QFont('TH Sarabun New', 36, QtGui.QFont.Bold))
    QtWidgets.QApplication.setStyle("Windows")
    screen = HomeScreen(pill_channel_datas, config)
    widget = QStackedWidget()
    widget.setWindowTitle("KLONGYAA")
    widget.setWindowIcon(QtGui.QIcon('../Klongyaa/shared/images/icon_k.png'))
    widget.addWidget(screen)
    widget.setFixedWidth(800)
    widget.setFixedHeight(480)
    # widget.showFullScreen()
    widget.show()
    sys.exit(app.exec_())
