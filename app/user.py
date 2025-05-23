"""Лист заявок, Создание заявки,
Удаление заявки(если статус = В ОЖИДАНИИ),
Редактирование заявки(если статус = В ОЖИДАНИИ),
Просмотр заявки(В ОТДЕЛЬНОМ ОКНЕ)"""
from PyQt6.QtWidgets import QWidget

from app.graf.user_graf import *
from database.db import select_tickets_user


class MainWindow(Ui_Form, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.windowTitle('Technical Support')

        data_tickets = select_tickets_user('1') #ДОБАВИТЬ СЮДА ПЕРЕДАЧУ ID ВМЕСТО 1
        height = 30
        self.content_widget = QtWidgets.QWidget(parent=self.groupBox)
        self.radio_group = QtWidgets.QButtonGroup(self)


        for i in data_tickets:

            ticket_frame = QtWidgets.QFrame(self.content_widget)
            ticket_frame.setGeometry(10, height, 780, 1000)

            rb = QtWidgets.QRadioButton(ticket_frame)
            rb.setStyleSheet("""
                QRadioButton {
                    border: 5px;
                    padding: 5px;}
                QRadioButton::indicator {
                    width: 0px;
                    height: 0px;}
                QRadioButton:checked {
                    border: 1px solid #250F0B;  
                    border-radius: 3px;}""")
            rb.setGeometry(10, 30, 600, 80)

            lb_info = QtWidgets.QLabel(rb)
            lb_info.setWordWrap(True)
            lb_info.setFixedWidth(580)
            font = QtGui.QFont()
            font.setPixelSize(11)
            lb_info.setFont(font)
            lb_info.setText(f'Текст заявки: {i[3]}, \nСтатус заявки: {i[4]} \nДата и время заявки: {i[5]}')
            lb_info.adjustSize()

            rb.resize(lb_info.width() + 10, lb_info.height() + 10)


    def add_ticket(self):
        ...

    def watch_ticket(self):
        ...

    def delete_ticket(self):
        ...

    def update_ticket(self):
        ...

    def exit_window(self):
        ...

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wind = MainWindow()
    wind.show()
    sys.exit(app.exec())