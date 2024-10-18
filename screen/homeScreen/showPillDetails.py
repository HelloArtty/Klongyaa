# pill_details.py

import requests
from PyQt5 import QtCore, QtGui, QtWidgets


def showTakePillScreen(pill_channel_data):
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

    # Create a layout for images
    image_layout = QtWidgets.QGridLayout()  # Use QGridLayout to display images in a grid
    image_widget = QtWidgets.QWidget()
    image_widget.setGeometry(50, 200, 700, 200)
    image_widget.setLayout(image_layout)
    
    pillsPerTime = int(pill_channel_data['pillsPerTime'])
    for i in range(pillsPerTime):
        img_label = QtWidgets.QLabel()
        img_pixmap = QtGui.QPixmap()

        # Check if the image URL is present
        if 'img' in pill_channel_data and pill_channel_data['img']:
            print(pill_channel_data['img'])
            img_pixmap.loadFromData(requests.get(pill_channel_data.get('img')).content)
        else:
            # Load default icon if no image is provided
            img_pixmap.load("../Klongyaa/shared/images/pill.png")

        # img_label.setStyleSheet("background-color: #F8F37D;")
        img_label.setPixmap(img_pixmap.scaled(150, 150, QtCore.Qt.KeepAspectRatio))
        
        row = i // 5
        col = i % 5
        image_layout.addWidget(img_label, row, col)
        
    # Center the images layout
    image_layout.setAlignment(QtCore.Qt.AlignCenter)
    main_layout.addWidget(image_widget)

    # Return the pill details screen instead of showing it directly
    return pill_details_screen
