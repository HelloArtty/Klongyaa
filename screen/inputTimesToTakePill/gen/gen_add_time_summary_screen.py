# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'screen\inputTimesToTakePill\ui\add_time_summary_screen.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_background_confirm_times_to_take_pill(object):
    def setupUi(self, background_confirm_times_to_take_pill):
        background_confirm_times_to_take_pill.setObjectName("background_confirm_times_to_take_pill")
        background_confirm_times_to_take_pill.resize(1024, 600)
        background_confirm_times_to_take_pill.setStyleSheet("QWidget#background_confirm_times_to_take_pill{\n"
"background-color: #97C7F9}")
        self.no_channel = QtWidgets.QLabel(background_confirm_times_to_take_pill)
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 191, 71))
        font = QtGui.QFont()
        font.setFamily("JasmineUPC")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF;\n"
"font: 75 36pt \"JasmineUPC\";\n"
"border-radius: 25px;\n"
"color: #070021;\n"
"")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")
        self.header_text = QtWidgets.QLabel(background_confirm_times_to_take_pill)
        self.header_text.setGeometry(QtCore.QRect(350, 30, 331, 201))
        self.header_text.setStyleSheet("font: 34pt \"JasmineUPC\";")
        self.header_text.setAlignment(QtCore.Qt.AlignCenter)
        self.header_text.setObjectName("header_text")
        self.scrollArea = QtWidgets.QScrollArea(background_confirm_times_to_take_pill)
        self.scrollArea.setGeometry(QtCore.QRect(80, 180, 871, 271))
        self.scrollArea.setStyleSheet("background-color:rgb(156, 183, 255);\n"
"border-color:rgb(156, 183, 255);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 869, 269))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.show_time_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.show_time_2.setStyleSheet("font: 75 34pt \"JasmineUPC\";\n"
"color: #070021;\n"
"")
        self.show_time_2.setObjectName("show_time_2")
        self.gridLayout.addWidget(self.show_time_2, 10, 1, 1, 1)
        self.show_time = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.show_time.setStyleSheet("font: 75 34pt \"JasmineUPC\";\n"
"color: #070021;\n"
"")
        self.show_time.setObjectName("show_time")
        self.gridLayout.addWidget(self.show_time, 9, 1, 1, 1)
        self.question_time_no1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.question_time_no1.setMinimumSize(QtCore.QSize(250, 0))
        self.question_time_no1.setMaximumSize(QtCore.QSize(250, 16777215))
        self.question_time_no1.setStyleSheet("background-color: none;\n"
"font: 75 30pt \"JasmineUPC\";\n"
"border-radius: 25px;\n"
"color: #070021;\n"
"background-color: #C5E1FF;")
        self.question_time_no1.setAlignment(QtCore.Qt.AlignCenter)
        self.question_time_no1.setObjectName("question_time_no1")
        self.gridLayout.addWidget(self.question_time_no1, 9, 0, 1, 1)
        self.button_edit_time_2 = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
        self.button_edit_time_2.setMinimumSize(QtCore.QSize(70, 70))
        self.button_edit_time_2.setStyleSheet("QToolButton#button_edit_time_2 {\n"
"   font-size: 40px;\n"
"  background-color: rgb(255, 74, 74);\n"
"  border-radius: 35px;\n"
"  color: white;\n"
"}\n"
"QToolButton#button_edit_time_2 {\n"
"    font-size: 40px;\n"
"  background-color: rgb(255, 50, 50);\n"
"  border-radius: 35px;\n"
"  color: white;\n"
"}")
        self.button_edit_time_2.setObjectName("button_edit_time_2")
        self.gridLayout.addWidget(self.button_edit_time_2, 10, 2, 1, 1)
        self.question_time_no2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.question_time_no2.setMinimumSize(QtCore.QSize(250, 0))
        self.question_time_no2.setMaximumSize(QtCore.QSize(250, 16777215))
        self.question_time_no2.setStyleSheet("background-color: none;\n"
"font: 75 30pt \"JasmineUPC\";\n"
"border-radius: 25px;\n"
"color: #070021;\n"
"background-color: #C5E1FF;")
        self.question_time_no2.setAlignment(QtCore.Qt.AlignCenter)
        self.question_time_no2.setObjectName("question_time_no2")
        self.gridLayout.addWidget(self.question_time_no2, 10, 0, 1, 1)
        self.button_edit_time = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
        self.button_edit_time.setMinimumSize(QtCore.QSize(70, 70))
        self.button_edit_time.setStyleSheet("QToolButton#button_edit_time {\n"
"   font-size: 40px;\n"
"  background-color: rgb(255, 74, 74);\n"
"  border-radius: 35px;\n"
"  color: white;\n"
"}\n"
"QToolButton#button_edit_time {\n"
"    font-size: 40px;\n"
"  background-color: rgb(255, 50, 50);\n"
"  border-radius: 35px;\n"
"  color: white;\n"
"}")
        self.button_edit_time.setObjectName("button_edit_time")
        self.gridLayout.addWidget(self.button_edit_time, 9, 2, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.success_button = QtWidgets.QToolButton(background_confirm_times_to_take_pill)
        self.success_button.setGeometry(QtCore.QRect(400, 470, 231, 103))
        self.success_button.setMinimumSize(QtCore.QSize(100, 50))
        self.success_button.setStyleSheet("QToolButton#success_button {\n"
"       font: 75 36pt \"JasmineUPC\";\n"
"    background-color:#24BD73;\n"
"    color: #ffffff;\n"
"    border-radius:20px;\n"
"    width: 170px;\n"
"    height: 100px;\n"
"}\n"
"QToolButton#success_button:hover {\n"
"    font: 75 36pt \"JasmineUPC\";\n"
"    background-color:#23B36D;\n"
"    color: #ffffff;\n"
"    border-radius:20px;\n"
"    width: 170px;\n"
"    height:100px;\n"
"}")
        self.success_button.setObjectName("success_button")
        self.add_time_button = QtWidgets.QToolButton(background_confirm_times_to_take_pill)
        self.add_time_button.setGeometry(QtCore.QRect(930, 20, 70, 70))
        self.add_time_button.setMinimumSize(QtCore.QSize(70, 70))
        self.add_time_button.setStyleSheet("QToolButton#add_time_button {\n"
"   font-size: 40px;\n"
"    background-color:#24BD73;\n"
"  border-radius: 35px;\n"
"  color: white;\n"
"}\n"
"QToolButton#add_time_button {\n"
"    font-size: 40px;\n"
"    background-color:#24BD73;\n"
"  border-radius: 35px;\n"
"  color: white;\n"
"}")
        self.add_time_button.setObjectName("add_time_button")

        self.retranslateUi(background_confirm_times_to_take_pill)
        QtCore.QMetaObject.connectSlotsByName(background_confirm_times_to_take_pill)

    def retranslateUi(self, background_confirm_times_to_take_pill):
        _translate = QtCore.QCoreApplication.translate
        background_confirm_times_to_take_pill.setWindowTitle(_translate("background_confirm_times_to_take_pill", "Dialog"))
        self.no_channel.setText(_translate("background_confirm_times_to_take_pill", "ช่องที่ 1"))
        self.header_text.setText(_translate("background_confirm_times_to_take_pill", "เวลาที่ต้องทานยา"))
        self.show_time_2.setText(_translate("background_confirm_times_to_take_pill", "12.00 น."))
        self.show_time.setText(_translate("background_confirm_times_to_take_pill", "12.00 น."))
        self.question_time_no1.setText(_translate("background_confirm_times_to_take_pill", "เวลาที่ 1"))
        self.button_edit_time_2.setText(_translate("background_confirm_times_to_take_pill", "🖉"))
        self.question_time_no2.setText(_translate("background_confirm_times_to_take_pill", "เวลาที่ 2"))
        self.button_edit_time.setText(_translate("background_confirm_times_to_take_pill", "🖉"))
        self.success_button.setText(_translate("background_confirm_times_to_take_pill", "เสร็จสิ้น"))
        self.add_time_button.setText(_translate("background_confirm_times_to_take_pill", "+"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    background_confirm_times_to_take_pill = QtWidgets.QDialog()
    ui = Ui_background_confirm_times_to_take_pill()
    ui.setupUi(background_confirm_times_to_take_pill)
    background_confirm_times_to_take_pill.show()
    sys.exit(app.exec_())
