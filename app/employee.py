from PyQt6 import QtWidgets, QtCore
from app.graf.employees_graf import *
import database.db as db


class Employee_Window(QtWidgets.QWidget, Employee_Ui_Form):
    def __init__(self, parent=None, employee_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.employee_id = employee_id

        # Инициализация layout для типов
        self.scroll_widget_types = QtWidgets.QWidget()
        self.layout_types = QtWidgets.QVBoxLayout(self.scroll_widget_types)
        self.scrollArea_types.setWidget(self.scroll_widget_types)

        # Инициализация layout для статусов
        self.scroll_widget_status = QtWidgets.QWidget()
        self.layout_status = QtWidgets.QVBoxLayout(self.scroll_widget_status)
        self.scrollArea_status.setWidget(self.scroll_widget_status)

        # Инициализация layout для тикетов
        self.scroll_widget_tickets = QtWidgets.QWidget()
        self.layout_tickets = QtWidgets.QVBoxLayout(self.scroll_widget_tickets)
        self.scrollArea_tickets.setWidget(self.scroll_widget_tickets)

        # Загрузка типов
        self.load_types()

        # Загрузка статусов
        self.load_statuses()

        # Загрузка тикетов
        self.load_tickets()

        # Подключаем кнопку take_tickets
        self.take_ticket_bt.clicked.connect(self.on_take_ticket_clicked)

    def load_types(self):
        types = db.get_types()
        self.radios_types = []
        if not types:
            print("No types returned from database!")
        else:
            for type_data in types:
                radio = QtWidgets.QRadioButton(type_data[0])
                self.layout_types.addWidget(radio)
                self.radios_types.append(radio)

    def load_statuses(self):
        statuses = db.get_statuses()
        self.radios_statuses = []
        if not statuses:
            print("No statuses returned from database!")
        else:
            for status in statuses:
                radio = QtWidgets.QRadioButton(status[0])
                self.layout_status.addWidget(radio)
                self.radios_statuses.append(radio)

    def load_tickets(self):
        tickets = db.get_active_tickets_except_done()
        if not tickets:
            print("No active tickets returned from database!")
            return

        # Создаем таблицу
        self.tickets_table = QtWidgets.QTableWidget()
        self.tickets_table.setColumnCount(7)
        self.tickets_table.setHorizontalHeaderLabels([
            "ID", "User ID", "Category", "Description",
            "Status", "Creation Date", "Employee"
        ])

        # Настройки таблицы
        self.tickets_table.setRowCount(len(tickets))
        self.tickets_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tickets_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        # Уменьшаем шрифт
        font = self.tickets_table.font()
        font.setPointSize(8)
        self.tickets_table.setFont(font)
        self.tickets_table.horizontalHeader().setFont(font)

        # Заполняем данные
        for row_idx, ticket in enumerate(tickets):
            for col_idx, value in enumerate(ticket):
                item = QtWidgets.QTableWidgetItem(str(value) if value is not None else "")
                item.setFont(font)

                # Включаем перенос текста для столбца Description (индекс 3)
                if col_idx == 3:  # description
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
                    item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsAutoTristate)
                self.tickets_table.setItem(row_idx, col_idx, item)

        # Настраиваем поведение столбцов
        self.tickets_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tickets_table.setWordWrap(True)
        self.tickets_table.resizeRowsToContents()

        # Остальные столбцы подгоняем по содержимому
        for col in [0, 1, 2, 4, 5, 6]:
            self.tickets_table.horizontalHeader().setSectionResizeMode(col,
                                                                       QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        # Добавляем таблицу в layout
        self.layout_tickets.addWidget(self.tickets_table)

    def on_take_ticket_clicked(self):
        """Обработчик нажатия кнопки взять заявку"""
        selected_items = self.tickets_table.selectedItems()

        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите заявку из таблицы!")
            return

        # Получаем ID выбранного тикета (первый столбец в строке)
        selected_row = selected_items[0].row()
        ticket_id_item = self.tickets_table.item(selected_row, 0)  # столбец ID
        ticket_id = int(ticket_id_item.text())

        # Получаем текущий статус заявки
        status_item = self.tickets_table.item(selected_row, 4)  # столбец Status
        current_status = status_item.text().lower()

        if current_status != 'в ожидании':
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Можно брать только заявки со статусом 'В ожидании'!")
            return

        # Вызываем функцию take_ticket
        if db.take_ticket(ticket_id, self.employee_id):
            # Обновляем статус в таблице
            status_item.setText("в работе")

            # Обновляем информацию о сотруднике (если есть соответствующий столбец)
            employee_item = self.tickets_table.item(selected_row, 6)  # столбец Employee
            if employee_item:
                # Здесь нужно получить ФИО текущего сотрудника (добавьте соответствующий метод в db)
                employee_name = db.get_employee_name(self.employee_id)
                if employee_name:
                    employee_item.setText(employee_name)

            QtWidgets.QMessageBox.information(self, "Успех", "Заявка успешно взята в работу!")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Не удалось взять заявку!")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = Employee_Window()
    win.show()
    sys.exit(app.exec())