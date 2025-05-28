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
        for category in categories:
            self.cbBox_upt.addItem(category[1], category[0])

        ticket_data = select_ticket(self.id_ticket)

        if ticket_data:
            category_name, description = ticket_data
            index = self.cbBox_upt.findText(category_name)
            if index >= 0:
                self.cbBox_upt.setCurrentIndex(index)
                self.select_categ_id = self.cbBox_upt.currentData()

            self.desc_lineEdit.setPlainText(description)
        else:
            self.close()
            return

        self.cbBox_upt.currentIndexChanged.connect(self.update_selection)
        self.btn_update.clicked.connect(self.send_ticket)

    def update_selection(self, index):
        """Обновляем выбранные данные при изменении выбора"""
        if index > 0:
            self.selected_categ = self.cbBox_upt.currentText()
            self.select_categ_id = self.cbBox_upt.currentData()
        else:
            self.selected_categ = None
            self.select_categ_id = None
        print(f"Выбрано: {self.selected_categ} (ID: {self.select_categ_id})")

    def send_ticket(self):
        """Обновление заявки при нажатии на кнопку"""
        ticket_text = self.desc_lineEdit.toPlainText().strip()

        if self.cbBox_upt.currentIndex() <= 0:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию")
            return

        if not ticket_text:
            QMessageBox.warning(self, "Ошибка", "Введите текст заявки")
            return

        if update_ticket(self.id_ticket, self.select_categ_id, ticket_text):
            QMessageBox.information(self, "Успех", "Заявка успешно обновлена!")
            self.close()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить заявку")

        print(f"Категория: {self.select_categ_id}")
        print(f"Текст заявки: {ticket_text}")


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     wind = Update_Window()
#     wind.show()
#     sys.exit(app.exec())