from PyQt6 import QtWidgets
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

        # Создаем таблицу для отображения тикетов
        self.tickets_table = QtWidgets.QTableWidget()
        self.tickets_table.setColumnCount(7)
        self.tickets_table.setHorizontalHeaderLabels([
            "ID", "User ID", "Category", "Description",
            "Status", "Creation Date", "Employee"
        ])

        # Настройки таблицы
        self.tickets_table.setRowCount(len(tickets))
        self.tickets_table.horizontalHeader().setStretchLastSection(True)
        self.tickets_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        # Создаем шрифт меньшего размера
        font = self.tickets_table.font()
        font.setPointSize(8)  # Уменьшаем размер шрифта (стандартный обычно 9-12)
        self.tickets_table.setFont(font)

        # Также уменьшаем шрифт в заголовках
        header = self.tickets_table.horizontalHeader()
        header.setFont(font)

        # Заполняем таблицу данными
        for row_idx, ticket in enumerate(tickets):
            for col_idx, value in enumerate(ticket):
                item = QtWidgets.QTableWidgetItem(str(value) if value is not None else "")
                item.setFont(font)  # Устанавливаем шрифт для каждой ячейки
                self.tickets_table.setItem(row_idx, col_idx, item)

        # Добавляем таблицу в layout
        self.layout_tickets.addWidget(self.tickets_table)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = Employee_Window()
    win.show()
    sys.exit(app.exec())