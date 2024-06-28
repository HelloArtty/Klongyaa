import sys
import requests
import speech_recognition as sr
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QStackedWidget, QDialog, QDialogButtonBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
from screen.homeScreen.main_homeScreen import HomeScreen
from shared.data.mock.config import config

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
    dialog = QDialog()
    dialog.setWindowTitle("Confirm")
    dialog.resize(800, 480)
    dialog.setStyleSheet("background-color : #97C7F9 ")

    layout = QVBoxLayout()

    label = QLabel(f"รหัสของคุณคือ<br><font color='red'>{user_id}</font><br>กรุณาตรวจสอบให้เรียบร้อยก่อนกดยืนยัน")
    label.setStyleSheet("font-size: 34px; font-weight: bold; margin-bottom: 20px; text-align: center;")
    label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(label)

    buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttonBox.setStyleSheet("QPushButton { font-size: 18px; padding: 10px; }")
    layout.addWidget(buttonBox)

    buttonBox.accepted.connect(dialog.accept)
    buttonBox.rejected.connect(dialog.reject)

    dialog.setLayout(layout)

    return dialog.exec_()

def show_error_dialog(message):
    dialog = QDialog()
    dialog.setWindowTitle("Error")
    dialog.resize(800, 480)
    dialog.setStyleSheet("background-color : #97C7F9 ")

    layout = QVBoxLayout()

    label = QLabel(message)
    label.setStyleSheet("font-size: 34px; font-weight: bold; margin-bottom: 20px; text-align: center; color: red;")
    label.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(label)

    buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
    buttonBox.setStyleSheet("QPushButton { font-size: 16px; padding: 10px; }")
    layout.addWidget(buttonBox)

    buttonBox.accepted.connect(dialog.accept)

    dialog.setLayout(layout)

    dialog.exec_()

# def check_and_update_user_id():
#     global config

#     while not config['userId']:
#         dialog = QDialog()
#         dialog.setWindowTitle("User ID")
#         dialog.resize(800, 480)
#         dialog.setStyleSheet("background-color : #97C7F9 ")

#         layout = QVBoxLayout()

#         label = QLabel("กรุณากรอกรหัสของคุณ")
#         label.setStyleSheet("font-size: 34px; font-weight: bold; margin-bottom: 20px; text-align: center;")
#         label.setAlignment(QtCore.Qt.AlignCenter)
#         layout.addWidget(label)

#         edit = QLineEdit()
#         edit.setStyleSheet("font-size: 16px; padding: 10px; background-color : lightgray")
#         edit.setFixedSize(780, 40)
#         layout.addWidget(edit)

#         keyboard_layout = QGridLayout()
#         layout.addLayout(keyboard_layout)

#         # Create buttons for letters A-Z
#         letters = [
#             ('A', 1, 0), ('B', 1, 1), ('C', 1, 2), ('D', 1, 3), ('E', 1, 4),
#             ('F', 1, 5), ('G', 1, 6), ('H', 1, 7), ('I', 1, 8), ('J', 1, 9),
#             ('K', 2, 0), ('L', 2, 1), ('M', 2, 2), ('N', 2, 3), ('O', 2, 4),
#             ('P', 2, 5), ('Q', 2, 6), ('R', 2, 7), ('S', 2, 8), ('T', 2, 9),
#             ('U', 3, 0), ('V', 3, 1), ('W', 3, 2), ('X', 3, 3), ('Y', 3, 4), ('Z', 3, 5)
#         ]

#         # Create buttons for numbers 0-9
#         numbers = [
#             ('0', 4, 0), ('1', 4, 1), ('2', 4, 2), ('3', 4, 3), ('4', 4, 4),
#             ('5', 4, 5), ('6', 4, 6), ('7', 4, 7), ('8', 4, 8), ('9', 4, 9)
#         ]

#         # Function to handle button clicks
#         def on_button_click(text):
#             current_text = edit.text()
#             edit.setText(current_text + text)

#         # Add buttons for letters
#         for text, row, col in letters:
#             button = QPushButton(text)
#             button.setStyleSheet("font-size: 16px; padding: 10px;")
#             button.clicked.connect(lambda _, t=text: on_button_click(t))
#             keyboard_layout.addWidget(button, row, col, 1, 1)

#         # Add buttons for numbers
#         for text, row, col in numbers:
#             button = QPushButton(text)
#             button.setStyleSheet("font-size: 16px; padding: 10px;")
#             button.clicked.connect(lambda _, t=text: on_button_click(t))
#             keyboard_layout.addWidget(button, row, col, 1, 1)

#         buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
#         buttonBox.setStyleSheet("QPushButton { font-size: 16px; padding: 10px; }")
#         layout.addWidget(buttonBox)

#         buttonBox.accepted.connect(dialog.accept)
#         buttonBox.rejected.connect(dialog.reject)

#         dialog.setLayout(layout)

#         if dialog.exec_() == QDialog.Accepted:
#             user_id = edit.text()
#             if user_id:
#                 if show_confirmation_dialog(user_id) == QDialog.Accepted:
#                     save_userId(user_id)
#                     config['userId'] = user_id
#                 else:
#                     continue
#             elif user_id == "":
#                 show_error_dialog("User ID cannot be empty!")
#             else:
#                 show_error_dialog("User ID is required!")

def check_and_update_user_id():
    global config

    while not config['userId']:
        dialog = QDialog()
        dialog.setWindowTitle("User ID")
        dialog.resize(800, 480)
        dialog.setStyleSheet("background-color : #97C7F9 ")

        layout = QVBoxLayout()

        label = QLabel("กรุณากรอกรหัสของคุณ")
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
            ('f', 1, 5), ('g', 1, 6), ('h', 1, 7), ('i', 1, 8), ('j', 1, 9),
            ('k', 2, 0), ('l', 2, 1), ('m', 2, 2), ('n', 2, 3), ('o', 2, 4),
            ('p', 2, 5), ('q', 2, 6), ('r', 2, 7), ('s', 2, 8), ('t', 2, 9),
            ('u', 3, 0), ('v', 3, 1), ('w', 3, 2), ('x', 3, 3), ('y', 3, 4), ('z', 3, 5)
        ]

        # Create buttons for numbers 0-9
        numbers = [
            ('0', 4, 0), ('1', 4, 1), ('2', 4, 2), ('3', 4, 3), ('4', 4, 4),
            ('5', 4, 5), ('6', 4, 6), ('7', 4, 7), ('8', 4, 8), ('9', 4, 9)
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
        keyboard_layout.addWidget(shift_button, 0, 10, 1, 2)

        # Add delete button
        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet("font-size: 16px; padding: 10px;")
        delete_button.clicked.connect(on_delete_click)
        keyboard_layout.addWidget(delete_button, 3, 6, 1, 1)

        # Add buttons for numbers
        for text, row, col in numbers:
            button = QPushButton(text)
            button.setStyleSheet("font-size: 16px; padding: 10px;")
            button.clicked.connect(lambda _, t=text: on_button_click(t))
            keyboard_layout.addWidget(button, row, col, 1, 1)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.setStyleSheet("QPushButton { font-size: 16px; padding: 10px; }")
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)

        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            user_id = edit.text()
            if user_id:
                if show_confirmation_dialog(user_id) == QDialog.Accepted:
                    save_userId(user_id)
                    config['userId'] = user_id
                else:
                    continue
            elif user_id == "":
                show_error_dialog("User ID cannot be empty!")
            else:
                show_error_dialog("User ID is required!")
                
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
