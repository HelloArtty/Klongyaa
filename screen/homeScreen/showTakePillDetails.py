# pill_details.py

import requests
from PyQt5 import QtCore, QtGui, QtWidgets


def showTakePillScreen(pill_channel_data, on_confirm_callback):
    # Create a QWidget for the full-screen view
    pill_details_screen = QtWidgets.QWidget()
    pill_details_screen.setFixedSize(800, 480)
    pill_details_screen.setStyleSheet("background-color: #FBFADD;")
    pill_details_screen.setWindowTitle("GUI - KLONG_YAA")

    # Main layout for the screen
    main_layout = QtWidgets.QVBoxLayout(pill_details_screen)

    # Show pill channel (use default value if not found)
    pill_channel = pill_channel_data.get("channelId", "ไม่ทราบช่อง")
    pill_channel_label = QtWidgets.QLabel(f"ช่องที่: {pill_channel+1}")
    pill_channel_label.setFont(QtGui.QFont("TH Sarabun New", 22))  # Adjust font size
    pill_channel_label.setAlignment(QtCore.Qt.AlignCenter)
    main_layout.addWidget(pill_channel_label)
    
    # Show pill name (use a default name if not found)
    pill_name = pill_channel_data.get("name", "ไม่ทราบชื่อยา")
    pill_name_label = QtWidgets.QLabel(pill_name)
    pill_name_label.setFont(QtGui.QFont("TH Sarabun New", 24))  # Adjust font size
    pill_name_label.setAlignment(QtCore.Qt.AlignCenter)
    main_layout.addWidget(pill_name_label)

    # Show pill amount (use default value if not found)
    pill_amount = pill_channel_data.get("pillsPerTime", 1)
    pill_amount_label = QtWidgets.QLabel(f"{pill_amount} เม็ด")
    pill_amount_label.setFont(QtGui.QFont("TH Sarabun New", 22))  # Adjust font size
    pill_amount_label.setAlignment(QtCore.Qt.AlignCenter)
    main_layout.addWidget(pill_amount_label)


    # Add a button for confirming pill intake
    confirm_button = QtWidgets.QPushButton("กินยาแล้ว")
    confirm_button.setFont(QtGui.QFont("TH Sarabun New", 18))
    confirm_button.setStyleSheet("background-color: #24BD73; color: white;")
    
    # Connect the button with the callback function
    confirm_button.clicked.connect(on_confirm_callback)
    main_layout.addWidget(confirm_button)

    return pill_details_screen

