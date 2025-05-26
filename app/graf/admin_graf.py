from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AdminWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Административная панель")
        self.resize(850, 600)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(214, 209, 179))
        palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(0, 0, 0))
        self.setPalette(palette)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.setFont(font)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        user_form = QtWidgets.QHBoxLayout()
        user_form.setSpacing(20)

        login_group = QtWidgets.QWidget()
        login_layout = QtWidgets.QVBoxLayout()
        login_layout.setSpacing(5)
        login_label = QtWidgets.QLabel("Логин:")
        login_label.setStyleSheet("color: black; font-size: 12pt;")
        login_layout.addWidget(login_label)
        self.lineEdit_log_adm = QtWidgets.QLineEdit()
        self.lineEdit_log_adm.setStyleSheet("background-color: #f5f5f0; color: black; border: 1px solid #b08858; border-radius: 4px; padding: 5px; font-size: 11pt; min-height: 35px;")
        login_layout.addWidget(self.lineEdit_log_adm)
        login_group.setLayout(login_layout)
        user_form.addWidget(login_group)

        pass_group = QtWidgets.QWidget()
        pass_layout = QtWidgets.QVBoxLayout()
        pass_layout.setSpacing(5)
        pass_label = QtWidgets.QLabel("Пароль:")
        pass_label.setStyleSheet("color: black; font-size: 12pt;")
        pass_layout.addWidget(pass_label)
        self.lineEdit_pass_adm = QtWidgets.QLineEdit()
        self.lineEdit_pass_adm.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_pass_adm.setStyleSheet("background-color: #f5f5f0; color: black; border: 1px solid #b08858; border-radius: 4px; padding: 5px; font-size: 11pt; min-height: 35px;")
        pass_layout.addWidget(self.lineEdit_pass_adm)
        pass_group.setLayout(pass_layout)
        user_form.addWidget(pass_group)

        role_group = QtWidgets.QWidget()
        role_layout = QtWidgets.QVBoxLayout()
        role_layout.setSpacing(5)
        role_label = QtWidgets.QLabel("Роль:")
        role_label.setStyleSheet("color: black; font-size: 12pt;")
        role_layout.addWidget(role_label)
        self.lineEdit_role_adm = QtWidgets.QLineEdit()
        self.lineEdit_role_adm.setStyleSheet("background-color: #f5f5f0; color: black; border: 1px solid #b08858; border-radius: 4px; padding: 5px; font-size: 11pt; min-height: 35px;")
        role_layout.addWidget(self.lineEdit_role_adm)
        role_group.setLayout(role_layout)
        user_form.addWidget(role_group)

        main_layout.addLayout(user_form)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.setSpacing(30)

        self.btn_create_user = QtWidgets.QPushButton("Создать пользователя")
        self.btn_create_user.setStyleSheet("QPushButton { background-color: #794e28; color: white; border: none; padding: 8px 16px; border-radius: 4px; font-size: 12pt; min-width: 180px; } QPushButton:hover { background-color: #5a3a1e; }")
        self.btn_create_user.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.btn_del_user = QtWidgets.QPushButton("Удалить пользователя")
        self.btn_del_user.setStyleSheet("QPushButton { background-color: #794e28; color: white; border: none; padding: 8px 16px; border-radius: 4px; font-size: 12pt; min-width: 180px; } QPushButton:hover { background-color: #5a3a1e; }")
        self.btn_del_user.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_create_user)
        buttons_layout.addWidget(self.btn_del_user)
        buttons_layout.addStretch()

        main_layout.addLayout(buttons_layout)

        group = QtWidgets.QGroupBox("Список всех пользователей")
        group.setStyleSheet("QGroupBox { border: 1px solid #b08858; border-radius: 5px; margin-top: 10px; padding-top: 15px; font-size: 12pt; color: black; background-color: #e6e1d1; } QGroupBox::title { subcontrol-origin: margin; left: 10px; color: black; }")

        layout = QtWidgets.QVBoxLayout()

        user_table = QtWidgets.QTableWidget()
        user_table.setColumnCount(3)
        user_table.setHorizontalHeaderLabels(["Логин", "Роль", "Пароль"])
        user_table.setStyleSheet("QTableWidget { background-color: #f5f5f0; color: black; border: 1px solid #b08858; alternate-background-color: #e6e1d1; } QHeaderView::section { background-color: #d4c9a8; color: black; padding: 5px; border: none; }")
        user_table.horizontalHeader().setStretchLastSection(True)

        user_table.setRowCount(3)
        for i in range(3):
            user_table.setItem(i, 0, QtWidgets.QTableWidgetItem(f"user{i + 1}"))
            user_table.setItem(i, 1, QtWidgets.QTableWidgetItem("Пользователь"))

        layout.addWidget(user_table)
        group.setLayout(layout)
        main_layout.addWidget(group)

        self.setLayout(main_layout)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_AdminWindow()
    window.show()
    sys.exit(app.exec())