
from app.graf.answer_to_ticket_graf import *
from database.db import get_answer, show_ticket_description


class Answer_Window(Answer_Ui_Form, QtWidgets.QWidget):
    def __init__(self, parent=None, employee_id=None, ticket_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.employee_id = employee_id
        self.ticket_id = ticket_id
        self.answer = None
        self.desc_ticket = None

        self.desc_ticket = show_ticket_description(self.ticket_id)
        self.ticket_desc_lb.setText(f'{self.desc_ticket}')

        self.pushButton_2.clicked.connect(self.send_answer)

    def send_answer(self):
        self.answer = self.answer_line_edit.toPlainText().strip()

        print(self.answer)


        if not self.answer:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите текст ответа")
            return
        try:
            get_answer(self.ticket_id, self.answer)
            QtWidgets.QMessageBox.information(self, "Успех", "Ответ отправлен")
            self.close()
            self.answer_line_edit.clear()  # Очищаем поле ввода

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось отправить ответ: {str(e)}")


