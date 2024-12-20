import sys

# from screen.homeScreen.main_homeScreen import HomeScreen
import __main__
import shared.images.success_icon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QDialog, QWidget


class SuccessSaveScreen(QDialog):
    def __init__(self, pillData):
        super().__init__()
        self.pillData = pillData
        self.setupUi(self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.stopDelay)
        self.timer.start(1000)


    def stopDelay(self):
        self.timer.stop()
        channelID = self.pillData["channelId"]
        allPillDatas = __main__.pill_channel_datas
        allPillDatas[str(channelID)] = self.pillData
        config = __main__.config

        if config["isFirstUse"] :
            config["isFirstUse"] = False
            
        __main__.widget.removeWidget(self)
        __main__.widget.addWidget(__main__.HomeScreen(allPillDatas, config))
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex()+1)

    def setupUi(self, background_success_save_screen):
        background_success_save_screen.setObjectName("background_success_save_screen")
        background_success_save_screen.resize(800, 480)
        background_success_save_screen.setStyleSheet("QWidget#background_success_save_screen{\n"
"background-color: #97C7F9}")
        self.frame_of_loading = QtWidgets.QFrame(background_success_save_screen)
        self.frame_of_loading.setGeometry(QtCore.QRect(40, 40, 720, 400))
        self.frame_of_loading.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius:40px")
        self.frame_of_loading.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_of_loading.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_of_loading.setObjectName("frame_of_loading")
        self.label = QtWidgets.QLabel(self.frame_of_loading)
        self.label.setGeometry(QtCore.QRect(235, 20, 250, 250))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/newPrefix/success_icon.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame_of_loading)
        self.label_2.setGeometry(QtCore.QRect(90, 280, 540, 100))
        self.label_2.setStyleSheet("font: 38pt \"JasmineUPC\";")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(background_success_save_screen)
        QtCore.QMetaObject.connectSlotsByName(background_success_save_screen)

    def retranslateUi(self, background_success_save_screen):
        _translate = QtCore.QCoreApplication.translate
        background_success_save_screen.setWindowTitle(_translate("background_success_save_screen", "Dialog"))
        self.label_2.setText(_translate("background_success_save_screen", "บันทึกข้อมูลสำเร็จ"))
