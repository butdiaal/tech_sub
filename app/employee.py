import os

import openpyxl
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt

from app.answer_to_ticket import Answer_Window
from app.graf.employees_graf import *
import database.db as db
import pandas as pd


class Employee_Window(QtWidgets.QWidget, Employee_Ui_Form):
    def __init__(self, parent=None, employee_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.employee_id = employee_id
        self.current_status_filter = None  # Текущий выбранный статус
        self.ticket_id = None
        self.init_ui()

    def init_ui(self):

        self.scroll_widget_status = QtWidgets.QWidget()
        self.layout_status = QtWidgets.QVBoxLayout(self.scroll_widget_status)
        self.scrollArea_status.setWidget(self.scroll_widget_status)

        self.scroll_widget_tickets = QtWidgets.QWidget()
        self.layout_tickets = QtWidgets.QVBoxLayout(self.scroll_widget_tickets)
        self.scrollArea_tickets.setWidget(self.scroll_widget_tickets)

        # Загрузка данных
        self.load_statuses()
        self.load_tickets()

        self.tickets_table.itemSelectionChanged.connect(self.update_selected_ticket)

        # Подключение кнопок
        self.take_ticket_bt.clicked.connect(self.take_selected_ticket)
        self.answer_bt.clicked.connect(self.answer_to_ticket)
        self.excel_export.clicked.connect(self.export_to_excel)

        # Подключение сигналов радио-кнопок статусов
        for radio in self.radios_statuses:
            radio.toggled.connect(self.filter_tickets_by_status)

    def load_statuses(self):
        statuses = db.get_statuses()
        self.radios_statuses = []
        if statuses:
            for status in statuses:
                radio = QtWidgets.QRadioButton(status[0])
                self.layout_status.addWidget(radio)
                self.radios_statuses.append(radio)
                # Первая кнопка выбрана по умолчанию
                if len(self.radios_statuses) == 1:
                    radio.setChecked(True)
                    self.current_status_filter = status[0]

    def filter_tickets_by_status(self):
        """Фильтрация заявок по выбранному статусу"""
        # Определяем выбранный статус
        for radio in self.radios_statuses:
            if radio.isChecked():
                self.current_status_filter = radio.text()
                break

        # Перезагружаем заявки с учетом фильтра
        self.load_tickets()

    def load_tickets(self):
        """Загрузка заявок с учетом текущего фильтра статуса"""
        if self.current_status_filter:
            # Если выбран конкретный статус
            tickets = db.get_tickets_by_status(self.current_status_filter)
        else:
            # Если фильтр не выбран (показываем все активные)
            tickets = db.get_active_tickets_except_done()

        # Очищаем таблицу перед загрузкой новых данных
        if hasattr(self, 'tickets_table'):
            self.layout_tickets.removeWidget(self.tickets_table)
            self.tickets_table.deleteLater()

        if not tickets:
            # Показываем сообщение, если нет заявок
            no_tickets_label = QtWidgets.QLabel("Нет заявок с выбранным статусом")
            self.layout_tickets.addWidget(no_tickets_label)
            return

        self.tickets_table = QtWidgets.QTableWidget()
        self.tickets_table.setColumnCount(7)
        self.tickets_table.setHorizontalHeaderLabels([
            "ID", "User ID", "Category", "Description",
            "Status", "Creation Date", "Employee ID"
        ])

        self.tickets_table.setRowCount(len(tickets))
        self.tickets_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tickets_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tickets_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

        # Установка минимальной высоты строк
        self.tickets_table.verticalHeader().setDefaultSectionSize(60)

        # Настройка столбцов
        self.tickets_table.setColumnWidth(0, 50)  # ID
        self.tickets_table.setColumnWidth(1, 70)  # User ID
        self.tickets_table.setColumnWidth(2, 100)  # Category
        self.tickets_table.setColumnWidth(4, 100)  # Status
        self.tickets_table.setColumnWidth(5, 120)  # Creation Date
        self.tickets_table.setColumnWidth(6, 80)  # Employee ID

        # Исправленная строка - правильный путь к Stretch
        self.tickets_table.horizontalHeader().setSectionResizeMode(
            3, QtWidgets.QHeaderView.ResizeMode.Stretch
        )

        # Настройка шрифта
        font = self.tickets_table.font()
        font.setPointSize(8)
        self.tickets_table.setFont(font)

        # Заполнение данных
        for row_idx, ticket in enumerate(tickets):
            for col_idx, value in enumerate(ticket):
                item = QtWidgets.QTableWidgetItem(str(value) if value is not None else "")
                item.setFont(font)
                if col_idx == 3:  # description
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
                self.tickets_table.setItem(row_idx, col_idx, item)

        # Настройка столбцов
        self.tickets_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tickets_table.setWordWrap(True)
        self.tickets_table.resizeRowsToContents()

        self.layout_tickets.addWidget(self.tickets_table)

    def take_selected_ticket(self):
        """Обработка взятия выбранной заявки"""
        if not hasattr(self, 'tickets_table'):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Нет заявок для выбора!")
            return

        selected = self.tickets_table.selectedItems()

        if not selected:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите заявку!")
            return

        row = selected[0].row()
        self.ticket_id = int(self.tickets_table.item(row, 0).text())
        current_status = self.tickets_table.item(row, 4).text().lower()

        if current_status != 'в ожидании':
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                                          "Можно брать только заявки со статусом 'В ожидании'")
            return

        # Обновление в базе данных
        if db.take_ticket(self.ticket_id, self.employee_id):
            # Обновление интерфейса
            self.tickets_table.item(row, 4).setText("в работе")
            self.tickets_table.item(row, 6).setText(str(self.employee_id))

            # Визуальное выделение
            for col in range(self.tickets_table.columnCount()):
                self.tickets_table.item(row, col).setBackground(QtGui.QColor(220, 255, 220))

            QtWidgets.QMessageBox.information(self, "Успех", "Заявка взята в работу!")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Ошибка при обновлении заявки")

    def answer_to_ticket(self):
        """Обработка ответа на заявку"""
        if not hasattr(self, 'tickets_table'):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Нет доступных заявок")
            return

        selected = self.tickets_table.selectedItems()
        if not selected:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите заявку из таблицы!")
            return

        row = selected[0].row()
        ticket_id = int(self.tickets_table.item(row, 0).text())
        employee_id_in_ticket = self.tickets_table.item(row, 6).text()

        # Проверяем, что заявка взята текущим сотрудником
        if employee_id_in_ticket != str(self.employee_id):
            QtWidgets.QMessageBox.warning(
                self,
                "Ошибка",
                "Вы можете отвечать только на заявки, взятые вами в работу!"
            )
            return

        # Проверяем статус заявки
        status = self.tickets_table.item(row, 4).text().lower()
        if status not in ['в работе', 'на проверке']:
            QtWidgets.QMessageBox.warning(
                self,
                "Ошибка",
                "Ответ можно давать только на заявки со статусом 'В работе' или 'На проверке'"
            )
            return

        # Открываем окно ответа
        self.ticket_window = Answer_Window(
            employee_id=self.employee_id,
            ticket_id=ticket_id
        )
        self.ticket_window.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.ticket_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.ticket_window.show()

    def update_selected_ticket(self):
        """Обновляет self.ticket_id при выборе строки в таблице"""
        selected = self.tickets_table.selectedItems()
        if selected:
            row = selected[0].row()
            self.ticket_id = int(self.tickets_table.item(row, 0).text())

    def export_to_excel(self):
        data = db.get_all_from_reports()
        if not data:
            QtWidgets.QMessageBox.information(self, "Информация",
                                              "Нет данных для экспорта")
            return
        report = pd.DataFrame(data, columns=['ID', 'ID заявки', 'Категория', 'Дата и время создания заявки',
                                             'Дата и время решения заявки', 'Описание заявки', 'Сотрудник',
                                             'Ответ на заявку'])

        report.to_excel("Report.xlsx", index=False, engine='openpyxl')
        QtWidgets.QMessageBox.information(self, "Выполнено успешно",
                                          f"Данные экспортированы в Report.xlsx")
        self.startfile = os.startfile("Report.xlsx")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = Employee_Window(employee_id=2)
    win.show()
    sys.exit(app.exec())
