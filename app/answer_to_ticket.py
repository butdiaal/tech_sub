from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from app.graf.answer_to_ticket_graf import *
from database.db import select_categories, add_new_ticket


class Answer_Window(Answer_Ui_Form, QtWidgets.QWidget):
    def __init__(self, parent=None, employee_id=1):
        super().__init__(parent)
        self.setupUi(self)
        self.employee_id = employee_id



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = Answer_Window()
    win.show()
    sys.exit(app.exec())
