import json

import __main__
import requests
from PyQt5 import QtCore, QtGui, QtWidgets

from screen.updatePillScreen.main_update import UpdatePillScreen
from shared.api.getPillchanneldata import fetch_pill_channel_data


class DetailScreen(QtWidgets.QDialog):
        
    def __init__(self, channelId):
        super().__init__()
        self.channelId = channelId
        self.pill_channel_data = fetch_pill_channel_data(self.channelId)
        print(self.pill_channel_data)
        self.setupUi(self)

    def setupUi(self, background_detail_screen):
        background_detail_screen.setObjectName("background_detail_screen")
        background_detail_screen.resize(800, 480)
        background_detail_screen.setStyleSheet("QWidget#background_detail_screen { background-color: #97C7F9; }")

        # Header label
        self.text_header_summary_screen = QtWidgets.QLabel(background_detail_screen)
        self.text_header_summary_screen.setGeometry(QtCore.QRect(260, 20, 370, 60))
        self.text_header_summary_screen.setStyleSheet("font: 36pt \"TH Sarabun New\"; font-weight: bold;")
        self.text_header_summary_screen.setAlignment(QtCore.Qt.AlignCenter)
        
        # Scroll area for pill data
        self.scroll_area = QtWidgets.QScrollArea(background_detail_screen)
        self.scroll_area.setGeometry(QtCore.QRect(10, 90, 780, 300))
        self.scroll_area.setStyleSheet("background-color:rgb(156, 183, 255); border-color:rgb(156, 183, 255);")
        self.scroll_area.setWidgetResizable(True)
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)

        # Pill name
        self.label_pill_name = self.create_label("ชื่อยา", self.scrollAreaWidgetContents)
        self.data_pill_name = self.create_data_label(self.pill_channel_data['name'], self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.label_pill_name, 0, 0)
        self.gridLayout_2.addWidget(self.data_pill_name, 0, 1)
        
        # Total pills data
        self.label_total_pills = self.create_label("จำนวนยาทั้งหมด", self.scrollAreaWidgetContents)
        self.data_total_pills = self.create_data_label(f"{self.pill_channel_data['totalPills']} เม็ด", self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.label_total_pills, 5, 0)
        self.gridLayout_2.addWidget(self.data_total_pills, 5, 1)

        # Pills per dose data
        self.label_amount_pill = self.create_label("จำนวนยาที่ต้องทาน", self.scrollAreaWidgetContents)
        self.data_amount_pill = self.create_data_label(f"{self.pill_channel_data['pillsPerTime']} เม็ด/มื้อ", self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.label_amount_pill, 8, 0)
        self.gridLayout_2.addWidget(self.data_amount_pill, 8, 1)

        # Display time to take the pill
        for index, time in enumerate(self.pill_channel_data["timeToTake"]):
            time_label = self.create_label(f"เวลาที่ {index + 1}", self.scrollAreaWidgetContents)
            time_data = self.create_data_label(f"{time} น.", self.scrollAreaWidgetContents)
            self.gridLayout_2.addWidget(time_label, index + 12, 0)
            self.gridLayout_2.addWidget(time_data, index + 12, 1)

        self.scroll_area.setWidget(self.scrollAreaWidgetContents)

        # Back button
        self.button_go_back = self.create_tool_button("ย้อนกลับ", background_detail_screen, self.goBack, QtCore.QRect(145, 400, 220, 75))
        
        # Edit button
        self.button_edit_pill = QtWidgets.QToolButton(background_detail_screen)
        self.button_edit_pill.setGeometry(QtCore.QRect(700, 20, 70, 70))
        self.button_edit_pill.setIconSize(QtCore.QSize(70, 70))
        self.button_edit_pill.setIcon(QtGui.QIcon('../Klongyaa/shared/images/edit2.png'))
        self.button_edit_pill.setStyleSheet("background-color : rgb(255, 74, 74); border-radius: 35px; font: 36pt \"TH Sarabun New\"; font-weight: bold;")
        self.button_edit_pill.clicked.connect(self.goToEditPage)
        self.button_edit_pill.setObjectName("button_edit_pill")

        # Delete button
        self.button_delete_pill_channel = self.create_tool_button("ลบ", background_detail_screen, self.deletePillData, QtCore.QRect(445, 400, 220, 75))
        self.button_delete_pill_channel.setStyleSheet("QToolButton { font: 36pt  \"TH Sarabun New\"; background-color:#DD5D5D; color: #ffffff; border-radius:20px; font-weight: bold;}")

        # Channel label
        self.no_channel = QtWidgets.QLabel(background_detail_screen)
        self.no_channel.setGeometry(QtCore.QRect(40, 10, 190, 70))
        self.no_channel.setFont(QtGui.QFont("TH Sarabun New", 36))
        self.no_channel.setStyleSheet("background-color: #C5E1FF; font: 36pt \"TH Sarabun New\"; border-radius: 25px; color: #070021; font-weight: bold")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        
        self.retranslateUi(background_detail_screen)
        QtCore.QMetaObject.connectSlotsByName(background_detail_screen)

    def retranslateUi(self, background_detail_screen):
        _translate = QtCore.QCoreApplication.translate
        headerText = f"ข้อมูลยาช่องที่ {self.pill_channel_data['channelId'] + 1}"
        self.text_header_summary_screen.setText(_translate("background_detail_screen", headerText))
        self.no_channel.setText(_translate("background_detail_screen", f"ช่องที่ {self.pill_channel_data['channelId'] + 1}"))
        self.button_go_back.setText(_translate("background_detail_screen", "ย้อนกลับ"))
        self.button_delete_pill_channel.setText(_translate("background_detail_screen", "ลบ"))

    def create_label(self, text, parent):
        label = QtWidgets.QLabel(text, parent)
        label.setMinimumSize(250, 35)
        label.setMaximumSize(400, 100)
        label.setStyleSheet("background-color: #C5E1FF; font: 36pt \"TH Sarabun New\"; border-radius: 25px; color: #070021; font-weight: bold;")
        label.setAlignment(QtCore.Qt.AlignCenter)
        return label

    def create_data_label(self, text, parent):
        label = QtWidgets.QLabel(text, parent)
        label.setMinimumSize(350, 60)
        label.setStyleSheet("font: 36pt \"TH Sarabun New\"; color: #070021; font-weight: bold;")
        return label

    def create_tool_button(self, text, parent, click_action, geometry):
        button = QtWidgets.QToolButton(parent)
        button.setGeometry(geometry)
        button.setStyleSheet("QToolButton { font: 36pt \"TH Sarabun New\"; background-color:#24BD73; color: #ffffff; border-radius:20px; font-weight: bold; }")
        button.clicked.connect(click_action)
        return button

    def deletePillData(self):
        url = f"{__main__.config['url']}/user/deletePillChannel/{self.pill_channel_data['id']}"
        res = requests.delete(url)
        if res.status_code == 200:
            __main__.pill_channel_datas[str(self.pill_channel_data["channelId"])] = {}
            __main__.widget.addWidget(__main__.HomeScreen(__main__.pill_channel_datas, __main__.config))
            __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)

    def goBack(self):
        __main__.widget.addWidget(__main__.HomeScreen(__main__.pill_channel_datas, __main__.config))
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)

    def goToEditPage(self):
        update_screen = UpdatePillScreen(self.pill_channel_data)
        __main__.widget.addWidget(update_screen)
        __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    detailScreen = DetailScreen(channelId=1)
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(detailScreen)
    widget.setWindowTitle("GUI - KLONG_YAA")
    widget.show()
    sys.exit(app.exec_())
