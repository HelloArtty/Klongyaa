from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UIHomeScreen(object):
    def setupUi(self, UIHomeScreen):
        UIHomeScreen.setObjectName("UIHomeScreen")
        UIHomeScreen.setEnabled(True)
        UIHomeScreen.resize(800, 480)  # Adjusted to fit within 800x480 pixels

        # Button positions based on the provided coordinates
        positions = [
            [0, 0, 265, 157],    # Button 1
            [266, 0, 265, 157],  # Button 2
            [533, 0, 265, 157],  # Button 3
            [0, 160, 398, 157],  # Button 4
            [400, 160, 398, 157],# Button 5
            [0, 320, 265, 157],  # Button 6
            [266, 320, 265, 157],# Button 7
            [533, 320, 265, 157] # Button 8
        ]

        # Create buttons dynamically based on positions
        self.buttons = []
        for idx, pos in enumerate(positions):
            button = QtWidgets.QPushButton(UIHomeScreen)
            button.setGeometry(QtCore.QRect(pos[0], pos[1], pos[2], pos[3]))
            button.setObjectName(f"pill_channel_btn_{idx}")
            button.setStyleSheet("")
            self.buttons.append(button)

        # Translate UI
        self.retranslateUi(UIHomeScreen)
        QtCore.QMetaObject.connectSlotsByName(UIHomeScreen)

    def retranslateUi(self, UIHomeScreen):
        _translate = QtCore.QCoreApplication.translate
        UIHomeScreen.setWindowTitle(_translate("UIHomeScreen", "Dialog"))
        # Set text for buttons if needed
        # self.buttons[0].setText(_translate("UIHomeScreen", "Button 1"))
        # self.buttons[1].setText(_translate("UIHomeScreen", "Button 2"))
        # ...


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UIHomeScreen = QtWidgets.QDialog()
    ui = Ui_UIHomeScreen()
    ui.setupUi(UIHomeScreen)
    UIHomeScreen.show()
    sys.exit(app.exec_())
