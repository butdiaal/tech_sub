"""Изменение заявки если статус = в ожидании"""
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6 import QtWidgets

from app.graf.update_ticket_graf import Ui_Update_Form
from database.db import select_categories, select_ticket, update_ticket


class Update_Window(QWidget, Ui_Update_Form):
    def __init__(self, parent=None, id_ticket=None):
        super().__init__(parent)
        self.setupUi(self)
        self.id_ticket = id_ticket
        self.selected_categ = None
        self.select_categ_id = None
        self.insert_text = None

        categories = select_categories()
        self.cbBox_upt.clear()

        self.cbBox_upt.addItem("")
        for i in categories:
            self.cbBox_upt.addItem(i[1], i[0])

        ticket = select_ticket(self.id_ticket)

        if ticket:
            for i in ticket:
                self.cbBox_upt.setCurrentText(i[0])
                self.desc_lineEdit.setPlainText(i[1])
        else:
            QMessageBox.warning(self, "Ошибка", "Изменить заявку если ее статус = 'в ожидании'")

        self.cbBox_upt.currentIndexChanged.connect(self.update_selection)
        self.btn_update.clicked.connect(self.send_ticket)

    def update_selection(self, index):
        """Обновляем выбранные данные при изменении выбора"""
        if index > 0:  # Игнорируем первый пустой элемент
            self.selected_categ = self.cbBox_upt.currentText()
            self.select_categ_id = self.cbBox_upt.currentData()
        else:
            self.selected_categ = None
            self.select_categ_id = None
        print(f"Выбрано: {self.selected_categ} (ID: {self.select_categ_id})")

    def send_ticket(self):
        """Добавление новой заявки при нажатии на кнопку"""
        ticket_text = self.desc_lineEdit.toPlainText().strip()

        if self.cbBox_upt.currentIndex() <= 0:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию")
            return

        if not ticket_text:
            QMessageBox.warning(self, "Ошибка", "Введите текст заявки")
            return

        if update_ticket(self.select_categ_id, ticket_text, self.id_ticket):
            QMessageBox.information(self, "Успех", "Заявка успешно создана!")
            self.close()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать заявку")

        print(f"Категория: {self.select_categ_id}")
        print(f"Текст заявки: {ticket_text}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = Update_Window()
    wind.show()
    sys.exit(app.exec())