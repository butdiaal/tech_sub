
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

    def ger_answ(self):
        self.answer_line_edit.setText(f'{self.desc_ticket}')

        self.answer = self.answer_line_edit.text.strip()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = Answer_Window()
    win.show()
    sys.exit(app.exec())
