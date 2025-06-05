import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import (QMessageBox, QTabWidget, QVBoxLayout,
                             QHBoxLayout, QGroupBox, QTableWidgetItem)
import database.db as db


class AdminWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Административная панель")
        self.resize(900, 600)

        # Установка цветовой палитры
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

        self.setPalette(palette)

        # Установка шрифта
        font = QtGui.QFont()
        font.setFamily("XO Tahion")
        self.setFont(font)

        # Текущий выбранный пользователь/сотрудник
        self.current_id = None
        self.current_table = None

        # Основной layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Создаем вкладки
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #794E2B;
                border-radius: 3px;
                background: #F5F0E1;
            }
            QTabBar::tab {
                background: #D6D1B0;
                color: #25170B;
                padding: 8px 16px;
                border: 1px solid #794E2B;
                border-bottom: none;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
            }
            QTabBar::tab:selected {
                background: #F5F0E1;
                border-bottom: 2px solid #794E2B;
            }
            QTabBar::tab:hover {
                background: #B0884C;
                color: white;
            }
        """)
        main_layout.addWidget(self.tab_widget)

        # Вкладка пользователей
        self.tab_users = QtWidgets.QWidget()
        self.tab_employees = QtWidgets.QWidget()

        self.tab_widget.addTab(self.tab_users, "Пользователи")
        self.tab_widget.addTab(self.tab_employees, "Сотрудники")

        # Инициализация интерфейса для каждой вкладки
        self.init_user_tab()
        self.init_employee_tab()
        self.update_users_table()
        self.update_employees_table()

    def init_user_tab(self):
        """Инициализация вкладки пользователей"""
        layout = QVBoxLayout(self.tab_users)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Группа для полей ввода пользователей
        user_input_group = QGroupBox("Редактирование пользователя")
        user_input_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #794E2B;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
                color: #25170B;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
                color: #25170B;
            }
        """)
        user_input_layout = QVBoxLayout()
        user_input_layout.setSpacing(10)

        # Поля ввода (только логин и пароль)
        self.user_login_edit = QtWidgets.QLineEdit()
        self.user_pass_edit = QtWidgets.QLineEdit()

        for edit in [self.user_login_edit, self.user_pass_edit]:
            edit.setStyleSheet("""
                QLineEdit {
                    background-color: #F5F0E1;
                    border: 1px solid #794E2B;
                    border-radius: 3px;
                    padding: 8px;
                    color: #25170B;
                }
            """)

        # Кнопки для пользователей
        self.user_create_btn = QtWidgets.QPushButton("Создать пользователя")
        self.user_save_btn = QtWidgets.QPushButton("Сохранить изменения")
        self.user_delete_btn = QtWidgets.QPushButton("Удалить пользователя")

        for btn in [self.user_create_btn, self.user_save_btn, self.user_delete_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #794E2B;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #B0884C;
                }
                QPushButton:disabled {
                    background-color: #D6D1B0;
                    color: #7A7A7A;
                }
            """)


        # Добавляем элементы
        user_fields = QHBoxLayout()
        user_fields.setSpacing(10)

        login_label = QtWidgets.QLabel("Логин:")
        pass_label = QtWidgets.QLabel("Пароль:")
        for label in [login_label, pass_label]:
            label.setStyleSheet("color: #25170B;")

        user_fields.addWidget(login_label)
        user_fields.addWidget(self.user_login_edit)
        user_fields.addWidget(pass_label)
        user_fields.addWidget(self.user_pass_edit)

        user_buttons = QHBoxLayout()
        user_buttons.setSpacing(10)
        user_buttons.addWidget(self.user_create_btn)
        user_buttons.addWidget(self.user_save_btn)
        user_buttons.addWidget(self.user_delete_btn)

        user_input_layout.addLayout(user_fields)
        user_input_layout.addLayout(user_buttons)
        user_input_group.setLayout(user_input_layout)

        # Таблица пользователей (3 колонки: ID, Логин, Пароль)
        self.users_table = QtWidgets.QTableWidget()
        self.users_table.setColumnCount(3)
        self.users_table.setHorizontalHeaderLabels(["ID", "Логин", "Пароль"])
        self.users_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.users_table.cellClicked.connect(self.load_user_data)
        self.users_table.setStyleSheet("""
            QTableWidget {
                background-color: #F5F0E1;
                border: 1px solid #794E2B;
                gridline-color: #D6D1B0;
                color: #25170B;
            }
            QHeaderView::section {
                background-color: #B0884C;
                color: white;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #794E2B;
                color: white;
            }
        """)

        # Добавляем в layout
        layout.addWidget(user_input_group)
        layout.addWidget(self.users_table)

        # Подключение сигналов
        self.user_create_btn.clicked.connect(self.create_user)
        self.user_save_btn.clicked.connect(self.save_user_changes)
        self.user_delete_btn.clicked.connect(self.delete_user)

    def init_employee_tab(self):
        """Инициализация вкладки сотрудников"""
        layout = QVBoxLayout(self.tab_employees)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Группа для полей ввода сотрудников
        emp_input_group = QGroupBox("Редактирование сотрудника")
        emp_input_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #794E2B;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
                color: #25170B;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
                color: #25170B;
            }
        """)
        emp_input_layout = QVBoxLayout()
        emp_input_layout.setSpacing(10)

        # Поля ввода
        self.emp_login_edit = QtWidgets.QLineEdit()
        self.emp_pass_edit = QtWidgets.QLineEdit()
        self.emp_admin_check = QtWidgets.QCheckBox("Администратор")

        for edit in [self.emp_login_edit, self.emp_pass_edit]:
            edit.setStyleSheet("""
                QLineEdit {
                    background-color: #F5F0E1;
                    border: 1px solid #794E2B;
                    border-radius: 3px;
                    padding: 8px;
                    color: #25170B;
                }
            """)

        self.emp_admin_check.setStyleSheet("""
            QCheckBox {
                color: #25170B;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:checked {
                background-color: #794E2B;
                border: 1px solid #25170B;
            }
            QCheckBox::indicator:unchecked {
                background-color: #F5F0E1;
                border: 1px solid #794E2B;
            }
        """)

        # Кнопки для сотрудников
        self.emp_create_btn = QtWidgets.QPushButton("Создать сотрудника")
        self.emp_save_btn = QtWidgets.QPushButton("Сохранить изменения")
        self.emp_delete_btn = QtWidgets.QPushButton("Удалить сотрудника")

        for btn in [self.emp_create_btn, self.emp_save_btn, self.emp_delete_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #794E2B;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #B0884C;
                }
                QPushButton:disabled {
                    background-color: #D6D1B0;
                    color: #7A7A7A;
                }
            """)

        # Добавляем элементы
        emp_fields = QHBoxLayout()
        emp_fields.setSpacing(10)

        login_label = QtWidgets.QLabel("Логин:")
        pass_label = QtWidgets.QLabel("Пароль:")
        for label in [login_label, pass_label]:
            label.setStyleSheet("color: #25170B;")

        emp_fields.addWidget(login_label)
        emp_fields.addWidget(self.emp_login_edit)
        emp_fields.addWidget(pass_label)
        emp_fields.addWidget(self.emp_pass_edit)
        emp_fields.addWidget(self.emp_admin_check)

        emp_buttons = QHBoxLayout()
        emp_buttons.setSpacing(10)
        emp_buttons.addWidget(self.emp_create_btn)
        emp_buttons.addWidget(self.emp_save_btn)
        emp_buttons.addWidget(self.emp_delete_btn)

        emp_input_layout.addLayout(emp_fields)
        emp_input_layout.addLayout(emp_buttons)
        emp_input_group.setLayout(emp_input_layout)

        # Таблица сотрудников
        self.employees_table = QtWidgets.QTableWidget()
        self.employees_table.setColumnCount(4)
        self.employees_table.setHorizontalHeaderLabels(["ID", "Логин", "Пароль", "Админ"])
        self.employees_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.employees_table.cellClicked.connect(self.load_employee_data)
        self.employees_table.setStyleSheet("""
            QTableWidget {
                background-color: #F5F0E1;
                border: 1px solid #794E2B;
                gridline-color: #D6D1B0;
                color: #25170B;
            }
            QHeaderView::section {
                background-color: #B0884C;
                color: white;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #794E2B;
                color: white;
            }
        """)

        # Добавляем в layout
        layout.addWidget(emp_input_group)
        layout.addWidget(self.employees_table)

        # Подключение сигналов
        self.emp_create_btn.clicked.connect(self.create_employee)
        self.emp_save_btn.clicked.connect(self.save_employee_changes)
        self.emp_delete_btn.clicked.connect(self.delete_employee)

    def load_user_data(self, row, column):
        """Загрузка данных пользователя в поля ввода"""
        self.current_id = self.users_table.item(row, 0).text()
        self.current_table = 'users'

        self.user_login_edit.setText(self.users_table.item(row, 1).text())
        self.user_pass_edit.setText(self.users_table.item(row, 2).text())

    def load_employee_data(self, row, column):
        """Загрузка данных сотрудника в поля ввода"""
        self.current_id = self.employees_table.item(row, 0).text()
        self.current_table = 'employees'

        self.emp_login_edit.setText(self.employees_table.item(row, 1).text())
        self.emp_pass_edit.setText(self.employees_table.item(row, 2).text())
        self.emp_admin_check.setChecked(self.employees_table.item(row, 3).text() == '1')

    def create_user(self):
        """Создание нового пользователя"""
        login = self.user_login_edit.text().strip()
        password = self.user_pass_edit.text().strip()

        if not login or not password:
            self.show_error_message("Логин и пароль должны быть заполнены!")
            return

        try:
            success = db.create_user_admin(login, password)
            if success:
                self.update_users_table()
                self.clear_user_inputs()
                self.show_success_message("Пользователь успешно создан!")
            else:
                self.show_error_message("Пользователь с таким логином уже существует!")
        except Exception as e:
            print(f"Ошибка при создании пользователя: {e}")
            self.show_error_message("Ошибка при создании пользователя")

    def create_employee(self):
        """Создание нового сотрудника"""
        login = self.emp_login_edit.text().strip()
        password = self.emp_pass_edit.text().strip()
        is_admin = self.emp_admin_check.isChecked()

        if not login or not password:
            self.show_error_message("Логин и пароль обязательны!")
            return

        try:
            connection = db.get_db_connection()
            cursor = connection.cursor()

            # Проверяем, существует ли уже такой сотрудник
            cursor.execute("SELECT id FROM employees WHERE login = %s", (login,))
            if cursor.fetchone():
                self.show_error_message("Сотрудник с таким логином уже существует!")
                return

            # Создаем нового сотрудника
            cursor.execute(
                f"INSERT INTO employees (login, password, is_admin) VALUES ('{login}', md5('{password}'), {is_admin});"
            )
            connection.commit()

            self.update_employees_table()
            self.clear_employee_inputs()
            self.show_success_message("Сотрудник успешно создан!")
        except Exception as e:
            print(f"Ошибка при создании сотрудника: {e}")
            self.show_error_message("Ошибка при создании сотрудника")
        finally:
            if 'connection' in locals():
                connection.close()

    def save_user_changes(self):
        """Сохранение изменений пользователя"""
        if not self.current_id or self.current_table != 'users':
            self.show_error_message("Не выбран пользователь для редактирования!")
            return

        login = self.user_login_edit.text().strip()
        password = self.user_pass_edit.text().strip()

        if not login or not password:
            self.show_error_message("Логин и пароль должны быть заполнены!")
            return

        try:
            success = db.update_user(self.current_id, login, password)
            if success:
                self.update_users_table()
                self.clear_user_inputs()
                self.show_success_message("Изменения сохранены успешно!")
            else:
                self.show_error_message("Ошибка при сохранении изменений")
        except Exception as e:
            print(f"Ошибка при обновлении пользователя: {e}")
            self.show_error_message("Ошибка при сохранении изменений")

    def save_employee_changes(self):
        """Сохранение изменений сотрудника"""
        if not self.current_id or self.current_table != 'employees':
            self.show_error_message("Не выбран сотрудник для редактирования!")
            return

        login = self.emp_login_edit.text().strip()
        password = self.emp_pass_edit.text().strip()
        is_admin = self.emp_admin_check.isChecked()

        if not login or not password:
            self.show_error_message("Логин и пароль обязательны!")
            return

        try:
            success = db.update_employee(self.current_id, login, password, is_admin)
            if success:
                self.update_employees_table()
                self.clear_employee_inputs()
                self.show_success_message("Изменения сохранены успешно!")
            else:
                self.show_error_message("Ошибка при сохранении изменений")
        except Exception as e:
            print(f"Ошибка при обновлении сотрудника: {e}")
            self.show_error_message("Ошибка при сохранении изменений")

    def delete_user(self):
        """Удаление пользователя"""
        selected_row = self.users_table.currentRow()
        if selected_row == -1:
            self.show_error_message("Выберите пользователя для удаления!")
            return

        user_id = self.users_table.item(selected_row, 0).text()
        login = self.users_table.item(selected_row, 1).text()

        reply = self.show_confirm_message(f"Вы уверены, что хотите удалить пользователя {login}?")
        if reply == QMessageBox.StandardButton.Yes:
            try:
                db.delete_user(login)
                self.update_users_table()
                self.clear_user_inputs()
                self.show_success_message("Пользователь удален успешно!")
            except Exception as e:
                print(f"Ошибка при удалении пользователя: {e}")
                self.show_error_message("Ошибка при удалении пользователя")

    def delete_employee(self):
        """Удаление сотрудника"""
        selected_row = self.employees_table.currentRow()
        if selected_row == -1:
            self.show_error_message("Выберите сотрудника для удаления!")
            return

        emp_id = self.employees_table.item(selected_row, 0).text()
        login = self.employees_table.item(selected_row, 1).text()

        reply = self.show_confirm_message(f"Вы уверены, что хотите удалить сотрудника {login}?")
        if reply == QMessageBox.StandardButton.Yes:
            try:
                connection = db.get_db_connection()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
                connection.commit()

                self.update_employees_table()
                self.clear_employee_inputs()
                self.show_success_message("Сотрудник удален успешно!")
            except Exception as e:
                print(f"Ошибка при удалении сотрудника: {e}")
                self.show_error_message("Ошибка при удалении сотрудника")
            finally:
                if 'connection' in locals():
                    connection.close()

    def update_users_table(self):
        """Обновление таблицы пользователей из БД"""
        try:
            users = db.get_all_users()  # Получаем данные из БД
            self.users_table.setRowCount(len(users))

            for row, user in enumerate(users):
                for col in range(3):  # Только 3 колонки: id, login, password
                    self.users_table.setItem(row, col, QTableWidgetItem(str(user[col])))
        except Exception as e:
            print(f"Ошибка при загрузке пользователей: {e}")

    def update_employees_table(self):
        """Обновление таблицы сотрудников из БД"""
        try:
            employees = db.get_all_employees()  # Получаем данные из БД
            self.employees_table.setRowCount(len(employees))

            for row, emp in enumerate(employees):
                # Отображаем только нужные колонки: id, login, password, is_admin
                self.employees_table.setItem(row, 0, QTableWidgetItem(str(emp[0])))  # id
                self.employees_table.setItem(row, 1, QTableWidgetItem(str(emp[1])))  # login
                self.employees_table.setItem(row, 2, QTableWidgetItem(str(emp[2])))  # password
                self.employees_table.setItem(row, 3, QTableWidgetItem('1' if emp[3] else '0'))  # is_admin
        except Exception as e:
            print(f"Ошибка при загрузке сотрудников: {e}")

    def clear_user_inputs(self):
        """Очистка полей ввода пользователей"""
        self.user_login_edit.clear()
        self.user_pass_edit.clear()
        self.current_id = None
        self.current_table = None

    def clear_employee_inputs(self):
        """Очистка полей ввода сотрудников"""
        self.emp_login_edit.clear()
        self.emp_pass_edit.clear()
        self.emp_admin_check.setChecked(False)
        self.current_id = None
        self.current_table = None

    def show_error_message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(text)
        msg.setWindowTitle("Ошибка")
        msg.setStyleSheet(self.get_message_box_style())
        msg.exec()

    def show_success_message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(text)
        msg.setWindowTitle("Успех")
        msg.setStyleSheet(self.get_message_box_style())
        msg.exec()

    def show_confirm_message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Подтверждение")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setStyleSheet(self.get_message_box_style())
        return msg.exec()

    def get_message_box_style(self):
        return """
            QMessageBox {
                background-color: #F5F0E1;
            }
            QLabel {
                color: #25170B;
            }
            QPushButton {
                background-color: #794E2B;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #B0884C;
            }
        """


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec())

#commitnula