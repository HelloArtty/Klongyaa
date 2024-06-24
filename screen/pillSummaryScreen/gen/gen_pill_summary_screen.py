from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_pill_summary_screen(object):
    def setupUi(self, background_summary_screen):
        background_summary_screen.setObjectName("background_summary_screen")
        background_summary_screen.resize(800, 480)
        background_summary_screen.setStyleSheet("QWidget#background_summary_screen{\n"
                                                "background-color: #97C7F9}")
        self.text_header_summary_screen = QtWidgets.QLabel(background_summary_screen)
        self.text_header_summary_screen.setGeometry(QtCore.QRect(290, 20, 375, 60))
        self.text_header_summary_screen.setStyleSheet("font: 75 34pt \"JasmineUPC\";\n"
                                                      "")
        self.text_header_summary_screen.setScaledContents(False)
        self.text_header_summary_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.text_header_summary_screen.setWordWrap(False)
        self.text_header_summary_screen.setIndent(50)
        self.text_header_summary_screen.setObjectName("text_header_summary_screen")
        self.scroll_area = QtWidgets.QScrollArea(background_summary_screen)
        self.scroll_area.setGeometry(QtCore.QRect(60, 90, 700, 300))
        self.scroll_area.setMinimumSize(QtCore.QSize(0, 300))
        self.scroll_area.setStyleSheet("background-color:rgb(156, 183, 255);\n"
                                       "border-color:rgb(156, 183, 255);\n"
                                       "\n"
                                       "")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 700, 300))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.show_total_pills = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.show_total_pills.setEnabled(True)
        self.show_total_pills.setMinimumSize(QtCore.QSize(200, 40))
        self.show_total_pills.setStyleSheet("font: 75 24pt \"JasmineUPC\";\n"
                                            "color: #070021;\n"
                                            "margin-right:20px")
        self.show_total_pills.setObjectName("show_total_pills")
        self.gridLayout_2.addWidget(self.show_total_pills, 5, 1, 1, 1)

        self.show_pill_name = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.show_pill_name.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_pill_name.sizePolicy().hasHeightForWidth())
        self.show_pill_name.setSizePolicy(sizePolicy)
        self.show_pill_name.setMinimumSize(QtCore.QSize(200, 40))
        self.show_pill_name.setStyleSheet("font: 75 24pt \"JasmineUPC\";\n"
                                          "color: #070021;\n"
                                          "border: none;\n"
                                          "margin-right:20px")
        self.show_pill_name.setObjectName("show_pill_name")
        self.gridLayout_2.addWidget(self.show_pill_name, 0, 1, 1, 1)

        self.show_amount_pill = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_amount_pill.sizePolicy().hasHeightForWidth())
        self.show_amount_pill.setSizePolicy(sizePolicy)
        self.show_amount_pill.setMinimumSize(QtCore.QSize(200, 40))
        self.show_amount_pill.setStyleSheet("font: 75 24pt \"JasmineUPC\";\n"
                                            "color: #070021;\n"
                                            "margin-right:20px")
        self.show_amount_pill.setObjectName("show_amount_pill")
        self.gridLayout_2.addWidget(self.show_amount_pill, 8, 1, 1, 1)

        self.show_time = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.show_time.setMinimumSize(QtCore.QSize(200, 40))
        self.show_time.setStyleSheet("font: 75 24pt \"JasmineUPC\";\n"
                                     "color: #070021;\n"
                                     "")
        self.show_time.setObjectName("show_time")
        self.gridLayout_2.addWidget(self.show_time, 12, 1, 1, 1)

        self.button_edit_time = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
        self.button_edit_time.setMinimumSize(QtCore.QSize(50, 50))
        self.button_edit_time.setStyleSheet("QToolButton#button_edit_time {\n"
                                            "   font-size: 24px;\n"
                                            "  background-color: rgb(255, 74, 74);\n"
                                            "  border-radius: 25px;\n"
                                            "  color: white;\n"
                                            "}\n"
                                            "QToolButton#button_edit_time:hover {\n"
                                            "    font-size: 24px;\n"
                                            "  background-color: rgb(255, 50, 50);\n"
                                            "  border-radius: 25px;\n"
                                            "  color: white;\n"
                                            "}")
        self.button_edit_time.setObjectName("button_edit_time")
        self.gridLayout_2.addWidget(self.button_edit_time, 12, 3, 1, 1)

        self.button_edit_pill_name = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
        self.button_edit_pill_name.setMinimumSize(QtCore.QSize(50, 50))
        self.button_edit_pill_name.setStyleSheet("QToolButton#button_edit_pill_name  {\n"
                                                 "   font-size: 24px;\n"
                                                 "  background-color: rgb(255, 74, 74);\n"
                                                 "  border-radius: 25px;\n"
                                                 "  color: white;\n"
                                                 "}\n"
                                                 "QToolButton#button_edit_pill_name :hover {\n"
                                                 " font-size: 24px;\n"
                                                 "  background-color: rgb(255, 50, 50);\n"
                                                 "  border-radius:25px;\n"
                                                 "  color: white;\n"
                                                 "}")
        self.button_edit_pill_name.setObjectName("button_edit_pill_name")
        self.gridLayout_2.addWidget(self.button_edit_pill_name, 0, 3, 1, 1)

        self.button_edit_total_pills = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
        self.button_edit_total_pills.setMinimumSize(QtCore.QSize(50, 50))
        self.button_edit_total_pills.setStyleSheet("QToolButton#button_edit_total_pills {\n"
                                                   "   font-size: 24px;\n"
                                                   "  background-color: rgb(255, 74, 74);\n"
                                                   "  border-radius: 25px;\n"
                                                   "  color: white;\n"
                                                   "}\n"
                                                   "QToolButton#button_edit_total_pills:hover {\n"
                                                   "    font-size: 24px;\n"
                                                   "  background-color: rgb(255, 50, 50);\n"
                                                   "  border-radius: 25px;\n"
                                                   "  color: white;\n"
                                                   "}")
        self.button_edit_total_pills.setObjectName("button_edit_total_pills")
        self.gridLayout_2.addWidget(self.button_edit_total_pills, 5, 3, 1, 1)

        self.button_edit_amount_pill = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
        self.button_edit_amount_pill.setMinimumSize(QtCore.QSize(50, 50))
        self.button_edit_amount_pill.setStyleSheet("QToolButton#button_edit_amount_pill {\n"
                                                   "   font-size: 24px;\n"
                                                   "  background-color: rgb(255, 74, 74);\n"
                                                   "  border-radius: 25px;\n"
                                                   "  color: white;\n"
                                                   "}\n"
                                                   "QToolButton#button_edit_amount_pill:hover {\n"
                                                   "    font-size: 24px;\n"
                                                   "  background-color: rgb(255, 50, 50);\n"
                                                   "  border-radius: 25px;\n"
                                                   "  color: white;\n"
                                                   "}")
        self.button_edit_amount_pill.setObjectName("button_edit_amount_pill")
        self.gridLayout_2.addWidget(self.button_edit_amount_pill, 8, 3, 1, 1)

        self.question_pill_name = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.question_pill_name.sizePolicy().hasHeightForWidth())
        self.question_pill_name.setSizePolicy(sizePolicy)
        self.question_pill_name.setMinimumSize(QtCore.QSize(120, 40))
        self.question_pill_name.setStyleSheet("font: 75 24pt \"JasmineUPC\";\n"
                                              "color: #070021;\n"
                                              "border: none;\n"
                                              "margin-right:20px")
        self.question_pill_name.setObjectName("question_pill_name")
        self.gridLayout_2.addWidget(self.question_pill_name, 0, 0, 1, 1)

        self.question_total_pills = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.question_total_pills.setMinimumSize(QtCore.QSize(120, 40))
        self.question_total_pills.setStyleSheet("font: 75 24pt \"JasmineUPC\";\n"
                                                "color: #070021;\n"
                                                "")
        self.question_total_pills.setObjectName("question_total_pills")
        self.gridLayout_2.addWidget(self.question_total_pills, 5, 0, 1, 1)

        self.question_time = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.question_time.setMinimumSize(QtCore.QSize(120, 40))
        self.question_time.setStyleSheet("font: 75 24pt \"JasmineUPC\";\n"
                                         "color: #070021;\n"
                                         "")
        self.question_time.setObjectName("question_time")
        self.gridLayout_2.addWidget(self.question_time, 12, 0, 1, 1)

        self.question_amount_pill = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.question_amount_pill.setMinimumSize(QtCore.QSize(120, 40))
        self.question_amount_pill.setStyleSheet("font: 75 24pt \"JasmineUPC\";\n"
                                                "color: #070021;\n"
                                                "")
        self.question_amount_pill.setObjectName("question_amount_pill")
        self.gridLayout_2.addWidget(self.question_amount_pill, 8, 0, 1, 1)

        self.scroll_area.setWidget(self.scrollAreaWidgetContents)

        self.button_back_summary_screen = QtWidgets.QPushButton(background_summary_screen)
        self.button_back_summary_screen.setGeometry(QtCore.QRect(60, 420, 93, 41))
        self.button_back_summary_screen.setStyleSheet("font: 75 24pt \"JasmineUPC\";\n"
                                                      "background-color: #CAFFBF;\n"
                                                      "color: #070021;")
        self.button_back_summary_screen.setObjectName("button_back_summary_screen")

        self.button_confirm_summary_screen = QtWidgets.QPushButton(background_summary_screen)
        self.button_confirm_summary_screen.setGeometry(QtCore.QRect(670, 420, 93, 41))
        self.button_confirm_summary_screen.setStyleSheet("font: 75 24pt \"JasmineUPC\";\n"
                                                         "background-color: #CAFFBF;\n"
                                                         "color: #070021;")
        self.button_confirm_summary_screen.setObjectName("button_confirm_summary_screen")

        self.retranslateUi(background_summary_screen)
        QtCore.QMetaObject.connectSlotsByName(background_summary_screen)

    def retranslateUi(self, background_summary_screen):
        _translate = QtCore.QCoreApplication.translate
        background_summary_screen.setWindowTitle(_translate("background_summary_screen", "Form"))
        self.text_header_summary_screen.setText(_translate("background_summary_screen", "SUMMARY SCREEN"))
        self.show_total_pills.setText(_translate("background_summary_screen", "TextLabel"))
        self.show_pill_name.setText(_translate("background_summary_screen", "TextLabel"))
        self.show_amount_pill.setText(_translate("background_summary_screen", "TextLabel"))
        self.show_time.setText(_translate("background_summary_screen", "TextLabel"))
        self.button_edit_time.setText(_translate("background_summary_screen", "🖉"))
        self.button_edit_pill_name.setText(_translate("background_summary_screen", "🖉"))
        self.button_edit_total_pills.setText(_translate("background_summary_screen", "🖉"))
        self.button_edit_amount_pill.setText(_translate("background_summary_screen", "🖉"))
        self.question_pill_name.setText(_translate("background_summary_screen", "Pill Name"))
        self.question_total_pills.setText(_translate("background_summary_screen", "Total Pills"))
        self.question_time.setText(_translate("background_summary_screen", "Time"))
        self.question_amount_pill.setText(_translate("background_summary_screen", "Amount"))
        self.button_back_summary_screen.setText(_translate("background_summary_screen", "BACK"))
        self.button_confirm_summary_screen.setText(_translate("background_summary_screen", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    background_summary_screen = QtWidgets.QDialog()
    ui = Ui_pill_summary_screen()
    ui.setupUi(background_summary_screen)
    background_summary_screen.show()
    sys.exit(app.exec_())

