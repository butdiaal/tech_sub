"""Лист заявок, Создание заявки,
Удаление заявки(если статус = В ОЖИДАНИИ),
Редактирование заявки(если статус = В ОЖИДАНИИ),
Просмотр заявки(В ОТДЕЛЬНОМ ОКНЕ)"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QScrollArea, QButtonGroup

from app.graf.user_graf import *
from database.db import select_tickets_user, delete_ticket


class MainWindow(Ui_Form, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.selected_ticket = None
        self.selected_ticket_id = None
        data_tickets = select_tickets_user('1')  # ПЕРЕДАТЬ СЮДА АЙДИ ЮЗЕРА ВМЕСТО 1
        self.content_widget = QtWidgets.QWidget(parent=self.groupBox)
        self.ticket_frames = []

        scroll = QtWidgets.QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.content_widget)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: #D6D1B2;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #B0884C;
                min-height: 20px;
                border-radius: 6px;
            }
        """)

        self.groupBox.setLayout(QtWidgets.QVBoxLayout())
        self.groupBox.layout().addWidget(scroll)

        layout = QtWidgets.QVBoxLayout(self.content_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)

        for i in data_tickets:
            ticket_frame = QtWidgets.QFrame(self.content_widget)
            ticket_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            ticket_frame.setStyleSheet("""
                QFrame {
                    background: #D6D1B2;
                    border: none;  
                    border-radius: 5px;
                    padding: 5px;
                }
            """)
            self.ticket_frames.append(ticket_frame)

            ticket_frame.setProperty('ticket_id', i[0])
            ticket_frame.setObjectName(str(i[0]))

            ticket_frame.setCursor(Qt.CursorShape.PointingHandCursor)
            ticket_frame.mousePressEvent = lambda event, f=ticket_frame, id=i[0]: self.select_ticket(f, id)

            frame_layout = QtWidgets.QVBoxLayout(ticket_frame)
            frame_layout.setContentsMargins(5, 5, 5, 5)

            lb_info = QtWidgets.QLabel(ticket_frame)
            lb_info.setWordWrap(True)
            lb_info.setText(f'Текст заявки: {i[3]}\nСтатус заявки: {i[4]}\nДата и время заявки: {i[5]}')

            frame_layout.addWidget(lb_info)
            layout.addWidget(ticket_frame)

        self.content_widget.setMinimumWidth(620)

        self.btn_insert.clicked.connect(self.add_ticket)
        self.btn_watch.clicked.connect(self.watch_ticket)
        self.btn_delete.clicked.connect(self.delete_ticket)
        self.btn_update.clicked.connect(self.update_ticket)
        self.btn_exit.clicked.connect(self.exit_window)

    def select_ticket(self, frame, ticket_id):
        """Выбор заявки по клику на фрейм, доб обводку"""
        for f in self.ticket_frames:
            f.setStyleSheet("""
                QFrame {
                    background: #D6D1B2;
                    border: none;
                    border-radius: 5px;
                    padding: 5px;
                }
            """)

        frame.setStyleSheet("""
            QFrame {
                background: #D6D1B2;
                border: 2px solid #794E28;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        self.selected_ticket = frame
        self.selected_ticket_id = ticket_id
        print("Selected ticket ID:", self.selected_ticket_id)


    def add_ticket(self):
        """Добавление заявки при нажатии на кнопку написать в поддержку"""
        pass


    def watch_ticket(self):
        """Просмотр заявки, открывается дополнительное окно"""
        if self.selected_ticket_id:
            print(f"Выбрана заявка с ID: {self.selected_ticket_id}")
            id = self.selected_ticket_id.objectName()


    def delete_ticket(self):
        """Удаление заявки, если статус != решено или в работе"""
        if self.selected_ticket_id:
            print(f"Выбрана заявка с ID: {self.selected_ticket_id}")
            id = self.selected_ticket_id.objectName()
            message = delete_ticket(id)
            print(f'Удалена заявки с id: {message}')


    def update_ticket(self):
        """Изменение заявки, если статус != решено или в работе"""
        if self.selected_ticket_id:
            print(f"Выбрана заявка с ID: {self.selected_ticket_id}")
            id = self.selected_ticket_id.objectName()


    def exit_window(self):
        """Закрытие окна"""
        self.close()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wind = MainWindow()
    wind.show()
    sys.exit(app.exec())