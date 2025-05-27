"""Создание новой заявки"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from app.graf.new_ticket_graf import *
from database.db import select_categories, add_new_ticket


class Supp_Window(NewUi_Form, QtWidgets.QWidget):
    def __init__(self, parent=None, user_id=1):
        super().__init__(parent)
        self.setupUi(self)
        self.user_id = user_id
        self.selected_categ = None
        self.select_categ_id = None
        self.insert_text = None

        categories = select_categories()
        self.cbBox_new.clear()

        self.cbBox_new.addItem("")
        for i in categories:
            self.cbBox_new.addItem(i[1], i[0])
        self.cbBox_new.setCurrentIndex(0)

        self.cbBox_new.currentIndexChanged.connect(self.update_selection)
        self.btn_save.clicked.connect(self.send_ticket)


    def update_selection(self, index):
        """Обновляем выбранные данные при изменении выбора"""
        if index > 0:  # Игнорируем первый пустой элемент
            self.selected_categ = self.cbBox_new.currentText()
            self.select_categ_id = self.cbBox_new.currentData()
        else:
            self.selected_categ = None
            self.select_categ_id = None
        print(f"Выбрано: {self.selected_categ} (ID: {self.select_categ_id})")


    def send_ticket(self):
        """Добавление новой заявки при нажатии на кнопку"""
        ticket_text = self.desc_textEdit.toPlainText().strip()

        if self.cbBox_new.currentIndex() <= 0:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию")
            return

        if not ticket_text:
            QMessageBox.warning(self, "Ошибка", "Введите текст заявки")
            return

        if add_new_ticket(self.user_id, self.select_categ_id, ticket_text):
            QMessageBox.information(self, "Успех", "Заявка успешно создана!")
            self.close()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать заявку")

        print(f"Категория: {self.select_categ_id}")
        print(f"Текст заявки: {ticket_text}")

#
# if __name__ == '__main__':
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     wind = Supp_Window()
#     wind.show()
#     sys.exit(app.exec())