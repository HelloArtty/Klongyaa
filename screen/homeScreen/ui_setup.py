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