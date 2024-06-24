from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_confirm_pill_name(object):
    def setupUi(self, background_confirm_pill_name):
        background_confirm_pill_name.setObjectName("background_confirm_pill_name")
        background_confirm_pill_name.resize(800, 480)  # Adjusted to 800x480 resolution
        background_confirm_pill_name.setStyleSheet("QWidget#background_confirm_pill_name{\n"
                                                   "background-color: #97C7F9}")

        self.no_channel = QtWidgets.QLabel(background_confirm_pill_name)
        self.no_channel.setGeometry(QtCore.QRect(40, 30, 190, 70))  # Adjusted position and size
        font = QtGui.QFont()
        font.setFamily("JasmineUPC")
        font.setPointSize(24)
        font.setBold(True)
        self.no_channel.setFont(font)
        self.no_channel.setStyleSheet("background-color: #C5E1FF;\n"
                                      "border-radius: 15px;\n"
                                      "color: #070021;\n"
                                      "padding: 10px;")
        self.no_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.no_channel.setObjectName("no_channel")

        self.label_1 = QtWidgets.QLabel(background_confirm_pill_name)
        self.label_1.setGeometry(QtCore.QRect(315, 120, 170, 80))  # Adjusted position and size
        font.setPointSize(28)
        self.label_1.setFont(font)
        self.label_1.setStyleSheet("font: 28pt \"JasmineUPC\";")
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName("label_1")

        self.show_pill_name = QtWidgets.QLabel(background_confirm_pill_name)
        self.show_pill_name.setGeometry(QtCore.QRect(120, 220, 560, 80))  # Adjusted position and size
        font.setPointSize(36)
        self.show_pill_name.setFont(font)
        self.show_pill_name.setStyleSheet("font: 36pt \"JasmineUPC\";")
        self.show_pill_name.setAlignment(QtCore.Qt.AlignCenter)
        self.show_pill_name.setObjectName("show_pill_name")

        self.button_correct_pill_name = QtWidgets.QPushButton(background_confirm_pill_name)
        self.button_correct_pill_name.setGeometry(QtCore.QRect(100, 340, 250, 90))  # Adjusted position and size
        font.setPointSize(24)
        self.button_correct_pill_name.setFont(font)
        self.button_correct_pill_name.setStyleSheet("QPushButton {\n"
                                                     "    font: 24pt \"JasmineUPC\";\n"
                                                     "    background-color: #24BD73;\n"
                                                     "    color: #ffffff;\n"
                                                     "    border-radius: 20px;\n"
                                                     "}\n"
                                                     "QPushButton:hover {\n"
                                                     "    background-color: #23B36D;\n"
                                                     "}")

        self.button_correct_pill_name.setObjectName("button_correct_pill_name")

        self.button_incorrect_pill_name = QtWidgets.QPushButton(background_confirm_pill_name)
        self.button_incorrect_pill_name.setGeometry(QtCore.QRect(440, 340, 250, 90))  # Adjusted position and size
        self.button_incorrect_pill_name.setFont(font)
        self.button_incorrect_pill_name.setStyleSheet("QPushButton {\n"
                                                       "    font: 24pt \"JasmineUPC\";\n"
                                                       "    background-color: #DD5D5D;\n"
                                                       "    border-radius: 20px;\n"
                                                       "    color: white;\n"
                                                       "}\n"
                                                       "QPushButton:hover {\n"
                                                       "    background-color: rgb(255, 50, 50);\n"
                                                       "}")

        self.button_incorrect_pill_name.setObjectName("button_incorrect_pill_name")

        self.retranslateUi(background_confirm_pill_name)
        QtCore.QMetaObject.connectSlotsByName(background_confirm_pill_name)

    def retranslateUi(self, background_confirm_pill_name):
        _translate = QtCore.QCoreApplication.translate
        background_confirm_pill_name.setWindowTitle(_translate("background_confirm_pill_name", "Dialog"))
        self.no_channel.setText(_translate("background_confirm_pill_name", "ช่องที่ 1"))
        self.label_1.setText(_translate("background_confirm_pill_name", "ชื่อยา"))
        self.show_pill_name.setText(_translate("background_confirm_pill_name", "ยาพาราแซลมอน"))
        self.button_correct_pill_name.setText(_translate("background_confirm_pill_name", "ถูกต้อง"))
        self.button_incorrect_pill_name.setText(_translate("background_confirm_pill_name", "ไม่ถูกต้อง"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    background_confirm_pill_name = QtWidgets.QDialog()
    ui = Ui_confirm_pill_name()
    ui.setupUi(background_confirm_pill_name)
    background_confirm_pill_name.show()
    sys.exit(app.exec_())
