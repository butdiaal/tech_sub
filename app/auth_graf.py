from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AuthForm(object):
    def setupUi(self, AuthForm):
        AuthForm.setObjectName("AuthForm")
        AuthForm.resize(398, 300)

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

        AuthForm.setPalette(palette)

        font = QtGui.QFont()
        font.setFamily("XO Tahion")
        AuthForm.setFont(font)

        self.pushButton_auth_in = QtWidgets.QPushButton(parent=AuthForm)
        self.pushButton_auth_in.setGeometry(QtCore.QRect(120, 200, 161, 41))
        self.pushButton_auth_in.setObjectName("pushButton_auth_in")
        self.pushButton_auth_in.setStyleSheet("""
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

        self.pushButton_reg_in_auth = QtWidgets.QPushButton(parent=AuthForm)
        self.pushButton_reg_in_auth.setGeometry(QtCore.QRect(120, 250, 161, 41))
        self.pushButton_reg_in_auth.setObjectName("pushButton_reg_in_auth")
        self.pushButton_reg_in_auth.setStyleSheet("""
            QPushButton {
                background-color: #B0884C;
                color: white;
                border-radius: 5px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #794E2B;
            }
        """)

        self.label_auth = QtWidgets.QLabel(parent=AuthForm)
        self.label_auth.setGeometry(QtCore.QRect(120, 20, 161, 31))
        self.label_auth.setObjectName("label_auth")

        self.lineEdit_auth_login = QtWidgets.QLineEdit(parent=AuthForm)
        self.lineEdit_auth_login.setGeometry(QtCore.QRect(20, 80, 361, 35))
        self.lineEdit_auth_login.setObjectName("lineEdit_auth_login")
        self.lineEdit_auth_login.setStyleSheet("""
            QLineEdit {
                background-color: #F5F0E1;
                border: 1px solid #794E2B;
                border-radius: 3px;
                padding: 5px;
            }
        """)

        self.lineEdit_aut_pass = QtWidgets.QLineEdit(parent=AuthForm)
        self.lineEdit_aut_pass.setGeometry(QtCore.QRect(20, 150, 361, 35))
        self.lineEdit_aut_pass.setObjectName("lineEdit_aut_pass")
        self.lineEdit_aut_pass.setStyleSheet("""
            QLineEdit {
                background-color: #F5F0E1;
                border: 1px solid #794E2B;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        self.lineEdit_aut_pass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.label_auth_login = QtWidgets.QLabel(parent=AuthForm)
        self.label_auth_login.setGeometry(QtCore.QRect(20, 60, 121, 21))
        self.label_auth_login.setObjectName("label_auth_login")

        self.label_auth_pass = QtWidgets.QLabel(parent=AuthForm)
        self.label_auth_pass.setGeometry(QtCore.QRect(20, 130, 101, 16))
        self.label_auth_pass.setObjectName("label_auth_pass")

        self.retranslateUi(AuthForm)
        QtCore.QMetaObject.connectSlotsByName(AuthForm)

    def retranslateUi(self, AuthForm):
        _translate = QtCore.QCoreApplication.translate
        AuthForm.setWindowTitle(_translate("AuthForm", "Авторизация"))
        self.pushButton_auth_in.setText(_translate("AuthForm", "Войти"))
        self.pushButton_reg_in_auth.setText(_translate("AuthForm", "Зарегистрироваться"))
        self.label_auth.setText(_translate("AuthForm",
                                           "<html><head/><body><p><span style=\" font-size:16pt; font-weight:700;\">Авторизация</span></p></body></html>"))
        self.label_auth_login.setText(_translate("AuthForm",
                                                 "<html><head/><body><p><span style=\" font-size:10pt;\">Введите логин:</span></p></body></html>"))
        self.label_auth_pass.setText(_translate("AuthForm",
                                                "<html><head/><body><p><span style=\" font-size:10pt;\">Введите пароль:</span></p></body></html>"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    AuthForm = QtWidgets.QWidget()
    ui = Ui_AuthForm()
    ui.setupUi(AuthForm)
    AuthForm.show()
    sys.exit(app.exec())
