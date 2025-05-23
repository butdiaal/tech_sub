from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_RegForm(object):
    def setupUi(self, RegForm):
        RegForm.setObjectName("RegForm")
        RegForm.resize(400, 400)

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(37, 15, 11))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.WindowText, brush)

        brush = QtGui.QBrush(QtGui.QColor(214, 209, 178))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)

        brush = QtGui.QBrush(QtGui.QColor(121, 78, 43))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush)

        brush = QtGui.QBrush(QtGui.QColor(176, 136, 76))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush)

        brush = QtGui.QBrush(QtGui.QColor(214, 209, 178))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)

        RegForm.setPalette(palette)

        font = QtGui.QFont()
        font.setFamily("XO Tahion")
        RegForm.setFont(font)

        self.label_reg = QtWidgets.QLabel(parent=RegForm)
        self.label_reg.setGeometry(QtCore.QRect(120, 20, 161, 31))
        self.label_reg.setObjectName("label_reg")

        self.label_reg_login = QtWidgets.QLabel(parent=RegForm)
        self.label_reg_login.setGeometry(QtCore.QRect(20, 70, 121, 21))
        self.label_reg_login.setObjectName("label_reg_login")

        self.lineEdit_reg_login = QtWidgets.QLineEdit(parent=RegForm)
        self.lineEdit_reg_login.setGeometry(QtCore.QRect(20, 90, 361, 35))
        self.lineEdit_reg_login.setObjectName("lineEdit_reg_login")
        self.lineEdit_reg_login.setStyleSheet("""
            QLineEdit {
                background-color: #F5F0E1;
                border: 1px solid #794E2B;
                border-radius: 3px;
                padding: 5px;
            }
        """)

        self.label_reg_number = QtWidgets.QLabel(parent=RegForm)
        self.label_reg_number.setGeometry(QtCore.QRect(20, 140, 161, 21))
        self.label_reg_number.setObjectName("label_reg_number")

        self.lineEdit_reg_number = QtWidgets.QLineEdit(parent=RegForm)
        self.lineEdit_reg_number.setGeometry(QtCore.QRect(20, 160, 361, 35))
        self.lineEdit_reg_number.setObjectName("lineEdit_reg_number")
        self.lineEdit_reg_number.setStyleSheet("""
            QLineEdit {
                background-color: #F5F0E1;
                border: 1px solid #794E2B;
                border-radius: 3px;
                padding: 5px;
            }
        """)

        self.label_reg_pass = QtWidgets.QLabel(parent=RegForm)
        self.label_reg_pass.setGeometry(QtCore.QRect(20, 210, 101, 16))
        self.label_reg_pass.setObjectName("label_reg_pass")

        self.lineEdit_reg_pass = QtWidgets.QLineEdit(parent=RegForm)
        self.lineEdit_reg_pass.setGeometry(QtCore.QRect(20, 230, 361, 35))
        self.lineEdit_reg_pass.setObjectName("lineEdit_reg_pass")
        self.lineEdit_reg_pass.setStyleSheet("""
            QLineEdit {
                background-color: #F5F0E1;
                border: 1px solid #794E2B;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        self.lineEdit_reg_pass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.pushButton_reg_in = QtWidgets.QPushButton(parent=RegForm)
        self.pushButton_reg_in.setGeometry(QtCore.QRect(120, 290, 161, 41))
        self.pushButton_reg_in.setObjectName("pushButton_reg_in")
        self.pushButton_reg_in.setStyleSheet("""
            QPushButton {
                background-color: #794E2B;
                color: white;
                border-radius: 5px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #B0884C;
            }
        """)

        self.pushButton_reg_in_auth = QtWidgets.QPushButton(parent=RegForm)
        self.pushButton_reg_in_auth.setGeometry(QtCore.QRect(120, 340, 161, 41))
        self.pushButton_reg_in_auth.setObjectName("pushButton_reg_in_auth")
        self.pushButton_reg_in_auth.setStyleSheet("""
            QPushButton {
                background-color: #794E2B;
                color: white;
                border-radius: 5px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #B0884C;
            }
        """)

        self.retranslateUi(RegForm)
        QtCore.QMetaObject.connectSlotsByName(RegForm)

    def retranslateUi(self, RegForm):
        _translate = QtCore.QCoreApplication.translate
        RegForm.setWindowTitle(_translate("RegForm", "Регистрация"))
        self.label_reg.setText(_translate("RegForm", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:700;\">Регистрация</span></p></body></html>"))
        self.label_reg_login.setText(_translate("RegForm", "<html><head/><body><p><span style=\" font-size:10pt;\">Введите логин:</span></p></body></html>"))
        self.label_reg_number.setText(_translate("RegForm", "<html><head/><body><p><span style=\" font-size:10pt;\">Введите номер телефона:</span></p></body></html>"))
        self.label_reg_pass.setText(_translate("RegForm", "<html><head/><body><p><span style=\" font-size:10pt;\">Введите пароль:</span></p></body></html>"))
        self.pushButton_reg_in.setText(_translate("RegForm", "Зарегистрироваться"))
        self.pushButton_reg_in_auth.setText(_translate("RegForm", "Авторизоваться"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RegForm = QtWidgets.QWidget()
    ui = Ui_RegForm()
    ui.setupUi(RegForm)
    RegForm.show()
    sys.exit(app.exec())