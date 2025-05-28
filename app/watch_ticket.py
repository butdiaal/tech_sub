"""Просмотр заявки"""
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from app.graf.watch_ticket_graf import Ui_Wch_Form
from database.db import select_for_watch


class Watch_Window(QWidget, Ui_Wch_Form):
    def __init__(self, parent=None, id_ticket=None):
        super().__init__(parent)
        self.setupUi(self)
        self.id_ticket = id_ticket

        self.load_ticket_data()
        self.btn_exit.clicked.connect(self.close)

    def load_ticket_data(self):
        """Загрузка данных заявки"""
        data = select_for_watch(self.id_ticket)

        if not data:
            QMessageBox.warning(self, "Ошибка", "Заявка не найдена")
            self.close()
            return

        ticket_data = data[0]

        if ticket_data:
            self.lb_categ.setText(str(ticket_data[0]))
            self.lb_desc.setText(str(ticket_data[1]))
            self.lb_status.setText(str(ticket_data[2]))
            self.lb_startdt.setText(str(ticket_data[3]))
            self.lb_enddt.setText(str(ticket_data[4]))
            self.lb_answer.setText(str(ticket_data[5]))

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     wind = Watch_Window()
#     wind.show()
#     sys.exit(app.exec())