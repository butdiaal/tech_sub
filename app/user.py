"""Лист заявок, Создание заявки,
Удаление заявки(если статус = В ОЖИДАНИИ),
Редактирование заявки(если статус = В ОЖИДАНИИ)"""
from app.graf.user_graf import *
from database.db import select_tickets_user


class MainWindow(Ui_Form, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.windowTitle('Technical Support')

        data_tickets = select_tickets_user('1') #ДОБАВИТЬ СЮДА ПЕРЕДАЧУ ID ВМЕСТО 1
        height = 20

        for i in data_tickets:
            lb_info = QtWidgets.QLabel(i)
            lb_info.setGeometry(100, height, 20, 20)
            lb_info.setText(f'{i[3],}')


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    wind = MainWindow()
    wind.show()
    sys.exit(app.exec())