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

    # Show pill name
    pill_name_label = QtWidgets.QLabel(pill_channel_data["name"])
    pill_name_label.setFont(QtGui.QFont("Arial", 24))  # Adjust font size
    pill_name_label.setGeometry(50, 50, 700, 50)
    pill_name_label.setAlignment(QtCore.Qt.AlignCenter)
    main_layout.addWidget(pill_name_label)

    # Show pill amount
    pill_amount_label = QtWidgets.QLabel(f"{pill_channel_data['pillsPerTime']} เม็ด")
    pill_amount_label.setFont(QtGui.QFont("Arial", 22))  # Adjust font size
    pill_amount_label.setGeometry(50, 120, 700, 50)
    pill_amount_label.setAlignment(QtCore.Qt.AlignCenter)
    main_layout.addWidget(pill_amount_label)

    # Add a button for confirming pill intake
    confirm_button = QtWidgets.QPushButton("กินยาแล้ว")
    confirm_button.setFont(QtGui.QFont("Arial", 18))
    confirm_button.setStyleSheet("background-color: #4CAF50; color: white;")
    
    # Connect the button with the callback function
    confirm_button.clicked.connect(on_confirm_callback)
    
    main_layout.addWidget(confirm_button)

    return pill_details_screen

