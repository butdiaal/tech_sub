import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMessageBox, QTabWidget, QVBoxLayout, QHBoxLayout, QGroupBox

from graf.admin_graf import Ui_admin_wind
from database.db import create_user, get_all_users, delete_user, update_user, get_all_employees, update_employee


class AdminWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_admin_wind()
        self.ui.setupUi(self)

        # Текущий выбранный пользователь/сотрудник
        self.current_id = None
        self.current_table = None

        # Основной layout
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # Группа для полей ввода и кнопок
        input_group = QGroupBox("Редактирование пользователя")
        input_layout = QVBoxLayout()
        input_group.setLayout(input_layout)

        # Поля ввода
        fields_layout = QHBoxLayout()
        fields_layout.addWidget(self.ui.label_log_adm)
        fields_layout.addWidget(self.ui.lineEdit_log_adm)
        fields_layout.addWidget(self.ui.label_pass_adm)
        fields_layout.addWidget(self.ui.lineEdit_pass_adm)
        fields_layout.addWidget(self.ui.label_role_adm)
        fields_layout.addWidget(self.ui.lineEdit_3)

        # Кнопки
        buttons_layout = QHBoxLayout()
        self.ui.btn_create_user_adm.setText("Создать нового")
        buttons_layout.addWidget(self.ui.btn_create_user_adm)
        self.btn_save = QtWidgets.QPushButton("Сохранить изменения")
        buttons_layout.addWidget(self.btn_save)
        buttons_layout.addWidget(self.ui.btn_del_user_adm)

        # Объединяем все в группе
        input_layout.addLayout(fields_layout)
        input_layout.addLayout(buttons_layout)
        main_layout.addWidget(input_group)

        # Создаем вкладки
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self.tab_users = QtWidgets.QWidget()
        self.tab_employees = QtWidgets.QWidget()

        # Добавляем вкладки
        self.tab_widget.addTab(self.tab_users, "Пользователи")
        self.tab_widget.addTab(self.tab_employees, "Сотрудники")

        # Настройка таблиц для обеих вкладок
        self.setup_users_table()
        self.setup_employees_table()

        # Подключение сигналов кнопок
        self.ui.btn_create_user_adm.clicked.connect(self.create_user)
        self.btn_save.clicked.connect(self.save_changes)
        self.ui.btn_del_user_adm.clicked.connect(self.delete_user)

        # Обновление списков при открытии
        self.update_users_list()
        self.update_employees_list()

    def setup_users_table(self):
        """Настройка таблицы пользователей"""
        layout = QVBoxLayout(self.tab_users)
        self.users_table = QtWidgets.QTableWidget()
        self.users_table.setColumnCount(4)
        self.users_table.setHorizontalHeaderLabels(["ID", "Логин", "Пароль", "Роль"])
        self.users_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.users_table.cellClicked.connect(lambda row, col: self.load_selected_row(row, 'users'))
        layout.addWidget(self.users_table)

    def setup_employees_table(self):
        """Настройка таблицы сотрудников"""
        layout = QVBoxLayout(self.tab_employees)
        self.employees_table = QtWidgets.QTableWidget()
        self.employees_table.setColumnCount(4)
        self.employees_table.setHorizontalHeaderLabels(["ID", "Логин", "Пароль", "Админ"])
        self.employees_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.employees_table.cellClicked.connect(lambda row, col: self.load_selected_row(row, 'employees'))
        layout.addWidget(self.employees_table)

    def load_selected_row(self, row, table_type):
        """Загрузка выбранной строки в поля редактирования"""
        if table_type == 'users':
            table = self.users_table
        else:
            table = self.employees_table

        self.current_id = table.item(row, 0).text()
        self.current_table = table_type

        # Заполняем поля ввода данными из выбранной строки
        self.ui.lineEdit_log_adm.setText(table.item(row, 1).text())
        self.ui.lineEdit_pass_adm.setText(table.item(row, 2).text())
        self.ui.lineEdit_3.setText(table.item(row, 3).text())

    def create_user(self):
        """Создание нового пользователя"""
        login = self.ui.lineEdit_log_adm.text().strip()
        password = self.ui.lineEdit_pass_adm.text().strip()
        role = self.ui.lineEdit_3.text().strip().lower()

        if not login or not password or not role:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        if role not in ['admin', 'user']:
            QMessageBox.warning(self, "Ошибка", "Роль может быть только 'admin' или 'user'")
            return

        try:
            create_user(login, password, role)
            QMessageBox.information(self, "Успех", "Пользователь успешно создан!")
            self.update_users_list()
            self.clear_inputs()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать пользователя: {str(e)}")

    def save_changes(self):
        """Сохранение изменений в выбранной записи"""
        if not self.current_id:
            QMessageBox.warning(self, "Ошибка", "Не выбрана запись для редактирования!")
            return

        login = self.ui.lineEdit_log_adm.text().strip()
        password = self.ui.lineEdit_pass_adm.text().strip()
        role_or_admin = self.ui.lineEdit_3.text().strip().lower()

        if not login or not password or not role_or_admin:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            if self.current_table == 'users':
                if role_or_admin not in ['admin', 'user']:
                    QMessageBox.warning(self, "Ошибка", "Роль может быть только 'admin' или 'user'")
                    return
                update_user(self.current_id, login, password, role_or_admin)
            else:
                update_employee(self.current_id, login, password, role_or_admin)

            QMessageBox.information(self, "Успех", "Изменения успешно сохранены!")
            self.update_users_list()
            self.update_employees_list()
            self.clear_inputs()
            self.current_id = None
            self.current_table = None

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить изменения: {str(e)}")

    def delete_user(self):
        """Удаление выбранного пользователя"""
        current_tab = self.tab_widget.currentIndex()

        if current_tab == 0:  # Вкладка пользователей
            table = self.users_table
            delete_func = delete_user
            entity_name = "пользователя"
        else:  # Вкладка сотрудников
            table = self.employees_table
            delete_func = lambda x: delete_user(x, table='employees')
            entity_name = "сотрудника"

        selected_row = table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", f"Выберите {entity_name} для удаления!")
            return

        login = table.item(selected_row, 1).text()

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Вы уверены, что хотите удалить {entity_name} {login}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_func(login)
                QMessageBox.information(self, "Успех", f"{entity_name.capitalize()} успешно удален!")
                if current_tab == 0:
                    self.update_users_list()
                else:
                    self.update_employees_list()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить {entity_name}: {str(e)}")

    def update_users_list(self):
        """Обновление списка пользователей"""
        users = get_all_users()
        self.users_table.setRowCount(len(users))

        for row, user in enumerate(users):
            for col, data in enumerate(user[:4]):  # Берем первые 4 поля
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                self.users_table.setItem(row, col, item)

    def update_employees_list(self):
        """Обновление списка сотрудников"""
        employees = get_all_employees()
        self.employees_table.setRowCount(len(employees))

        for row, employee in enumerate(employees):
            for col, data in enumerate(employee):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                self.employees_table.setItem(row, col, item)

    def clear_inputs(self):
        """Очистка полей ввода"""
        self.ui.lineEdit_log_adm.clear()
        self.ui.lineEdit_pass_adm.clear()
        self.ui.lineEdit_3.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(214, 209, 179))
    palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(0, 0, 0))
    palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor(121, 78, 40))
    palette.setColor(QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(255, 255, 255))
    app.setPalette(palette)

    window = AdminWindow()
    window.setWindowTitle("Административная панель")
    window.resize(900, 600)
    window.show()
    sys.exit(app.exec())