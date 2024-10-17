from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets


def setupUi(self, UIHomeScreen, pill_channel_buttons, pill_channel_datas, config):
    width_height_of_channel = [
        [0, 0, 400, 120],#1
        [400, 0, 400, 120],#2
        [0, 120, 400, 120],#3
        [400, 120, 400, 120], #4
        [0, 240, 400, 120],#5
        [400, 240, 400, 120],#6
        [0, 360, 400, 120],#7
        [400, 360, 400, 120] #8
    ]
    UIHomeScreen.setObjectName("UIHomeScreen")
    UIHomeScreen.resize(800, 480)

    # Set data to every channel of pill
    for index in range(8):
        pill_channel_btn = QtWidgets.QPushButton(UIHomeScreen)
        pill_channel_btn.clicked.connect(partial(self.gotoPillDetailScreen, index, pill_channel_datas[str(index)]))
        pill_channel_btn.setGeometry(QtCore.QRect(
            width_height_of_channel[index][0], 
            width_height_of_channel[index][1], 
            width_height_of_channel[index][2], 
            width_height_of_channel[index][3]
        ))

        # If have data in that slot
        if pill_channel_datas.get(str(index)) and len(pill_channel_datas[str(index)]) != 0:
            font = QtGui.QFont()
            font.setPointSize(18)
            pill_channel_btn.setFont(font)
            channel_text = "ช่องที่ " + str(index + 1) + " \n" + pill_channel_datas[str(index)]["name"]
            pill_channel_btn.setText(channel_text)
            pill_channel_btn.setStyleSheet("background-color : #F8F37D")
        else:
            # If don't have data in that slot
            icon_path = QtCore.QDir.current().absoluteFilePath("../shared/images/plus_icon.png")
            pill_channel_btn.setIcon(QtGui.QIcon(icon_path))
            pill_channel_btn.setIconSize(QtCore.QSize(45, 45))
            pill_channel_btn.setStyleSheet("background-color : #97C7F9")

        pill_channel_buttons.append(pill_channel_btn)

    #เดี๋ยวมาแก้
    print("status = ", config["isFirstUse"])
    if config["isFirstUse"]:
        self.frame = QtWidgets.QFrame(UIHomeScreen)
        self.frame.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.frame.setStyleSheet("background-color: white; border-radius: 20px")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.frame_2 = QtWidgets.QFrame(UIHomeScreen)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(80, 240, 321, 81))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("1. กดไปที่ช่องที่ 1")

        for i in range(6, 0, -1):
            pill_channel_buttons[i].raise_()

        self.frame.raise_()
        self.frame_2.raise_()
        pill_channel_buttons[0].raise_()